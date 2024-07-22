import boto3
import os
import json
import numpy as np
import pyomo.environ as pyo


# bedrockを使って文字列の埋込表現を取得
#   mode: "titan", "cohere"
def get_embeddings(texts, mode):
    embeddings = {}
    bedrock_client = boto3.client('bedrock-runtime', region_name="ap-northeast-1")

    # titan
    if mode=="titan":
        for text in texts:
            bedrock_body = {
                "inputText": text
            }
            body_bytes = json.dumps(bedrock_body).encode('utf-8')
            response = bedrock_client.invoke_model(
                accept="*/*",
                body=body_bytes,
                contentType="application/json",
                modelId="amazon.titan-embed-text-v1",
            )
            response_body = json.loads(response.get("body").read())
            embedding = response_body.get("embedding")
            embeddings[text] = embedding

    # cohere
    elif mode=="cohere":
        bedrock_body = {
            "texts": texts,
            "input_type": "clustering"
        }
        body_bytes = json.dumps(bedrock_body).encode('utf-8')
        response = bedrock_client.invoke_model(
            accept="*/*",
            body=body_bytes,
            contentType="application/json",
            modelId="cohere.embed-english-v3",
        )
        response_body = json.loads(response.get("body").read())
        for text, embedding in zip(
            response_body.get("texts"),
            response_body.get("embeddings")
        ):
            embeddings[text] = embedding

    return embeddings


# 埋込表現間の類似度(コサイン類似度)を評価
def similarity(embed1, embed2):
    return np.dot(embed1, embed2) / (np.linalg.norm(embed1) * np.linalg.norm(embed2))

# 類似度行列を取得
def similarities(words, embeds):
    sims = []
    for i, wi in enumerate(words):
        sims.append([
            similarity(embeds[wi], embeds[wj]) for j, wj in enumerate(words)
        ])
    return sims

# 単語を読み込んで、対応する埋込表現と類似度行列を取得
#   mode: "titan", "cohere"
def setup_dataset(words, mode):
    # 埋込表現を取得
    embeds = get_embeddings(words, mode)
    # 類似度行列を取得
    sims = similarities(words, embeds)
    return embeds, sims


# モデルを準備
def setup_model(sims, excludes, M, N):
    # 数理最適化
    model = pyo.ConcreteModel(name="ConnectionsSolver")
    
    # 変数を定義
    model.I = pyo.Set(initialize=(i for i in range(M*N)))
    model.N = pyo.Set(initialize=(n for n in range(N)))
    model.XI = model.I * model.N
    model.X = pyo.Var(model.XI, domain=pyo.Binary)
    
    # 制約条件を定義
    def const1_rule(model, i):
        return sum(model.X[i,:]) == 1
    def const2_rule(model, n):
        return sum(model.X[:,n]) == M
    def const3_rule(model, n, e):
        return sum([model.X[i,n] for i in excludes[e]]) <= M-1
    model.Const1 = pyo.Constraint(model.I, rule=const1_rule)
    model.Const2 = pyo.Constraint(model.N, rule=const2_rule)
    model.Const3 = pyo.Constraint(model.N, range(len(excludes)), rule=const3_rule)

    # 目的関数を定義
    def obj_rule(model):
        xx = np.array([[model.X[i, n] for i in range(M*N)] for n in range(N)])
        ss = np.array(sims)
        s_in  = (np.dot(xx.T, xx) * ss).sum()
        #s_out = ss.sum() - s_in
        return s_in
        #return s_in / s_out

    model.Obj = pyo.Objective(rule=obj_rule, sense=pyo.maximize)
    return model


# 最適化
def optimize(model, stallnodes):
    opt = pyo.SolverFactory('scip')
    opt.options["limits/stallnodes"] = stallnodes
    opt.options["display/freq"] = 1000
    res = opt.solve(model, tee=True)
    return res


# 結果を表示
def show_results(model, words, sims, M, N):
    def my_round_int(number):
        return int((number * 2 + 1) // 2)
    
    print(f"評価値: {model.Obj()}")
    scores = [{'words':[], 'score':0.0} for n in range(N)]
    
    xx = np.array([[model.X[i, n].value for i in range(M*N)] for n in range(N)])
    ss = np.array(sims)
    for n in range(N):
        scores[n]['score'] = (np.dot(xx[n,:].reshape(-1,1), xx[n,:].reshape(1,-1)) * ss).sum()

    for i in range(M*N):
        for n in range(N):
            if my_round_int(model.X[i, n].value) == 1:
                scores[n]['words'].append(words[i])

    scores = sorted(scores, key=lambda x: x['score'], reverse=True)
    for idx, s in enumerate(scores):
        print("{}: ({:8.2f}) {}".format(idx, s['score'], s['words']))

    return scores


def main():
    M = 4 #グループあたりの単語数
    N = 4 #グループ数

    wordsin = input('Enter words separated by commas: ')
    words = []
    for w in wordsin.split(','):
        words.append(w.strip().lower())
    if len(words) != M*N:
        print('num words is not M*N ({})'.format(M*N))

    # データセット準備
    embeds, sims = setup_dataset(words, "titan")
    print('words: {}'.format(words))
    print('shape of embeddings: {}'.format(np.array(embeds[words[0]]).shape))
    print('shape of similarities: {}'.format(np.array(sims).shape))

    # 正誤判定結果
    c_success = []
    c_fail = []

    finished = False
    while not finished:
        # 正解した単語を処理対象から除去
        words2 = []
        if len(c_success) > 0:
            for w in words:
                done = False
                for c in c_success:
                    if w in c:
                        done = True
                if not done:
                    words2.append(w)
        else:
            words2 = words

        # 失敗した単語の組み合わせを制約条件に追加
        excludes = []
        for c in c_fail:
            ex = []
            for i,w in enumerate(words2):
                for wc in c:
                    if wc == w:
                        ex.append(i)
            excludes.append(ex)
        
        print('words for optimization: {}'.format(words2))
        print('excluded combinations: {}'.format(excludes))

        # 最適化
        sims2  = similarities(words2, embeds)
        model  = setup_model(sims2, excludes, M, N-len(c_success))
        result = optimize(model, -1)
        #result = optimize(model, 10000)
        scores = show_results(model, words2, sims2, M, N-len(c_success))

        # 正誤を確認
        while True:
            print ('Proposed group is...: {}'.format(scores[0]['words']))
            ans = input('Was this group correct? (y/n): ')
            if ans == 'y':
                c_success.append(scores[0]['words'])
                scores.pop(0)
                if len(scores)==1:
                    c_success.append(scores[0]['words'])
                    scores.pop(0)
                    finished = True
                    break
            elif ans == 'n':
                c_fail.append(scores[0]['words'])
                print("The following groups were correct!")
                for idx,ws in enumerate(c_success):
                    print("{}: {}".format(idx, ws))
                print("But the following groups were not correct!")
                for idx,ws in enumerate(c_fail):
                    print("{}: {}".format(idx, ws))
                break

    print("All groups were correct, and the numbers of failures is '{}'".format(len(c_fail)))
    for idx,ws in enumerate(c_success):
        print("{}: {}".format(idx, ws))


if __name__ == "__main__":
    main()