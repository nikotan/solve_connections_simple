### Connections を大規模言語モデルと数理最適化で解く

### 参考
- Connections
  - [Connections: Group words by topic. New puzzles daily. - The New York Times](https://www.nytimes.com/games/connections)
  - [Connections – Archive](https://connections.swellgarfo.com/archive)
  - [Today’s NYT Connections Answers - Word Tips](https://word.tips/todays-nyt-connections-answers/)
- 数理最適化ソルバー
  - 主に使用
    - [SCIP](https://www.scipopt.org/) : 混合整数非線形計画問題
  - その他
    - [Ipopt](https://github.com/coin-or/Ipopt) : 連続非線形計画問題
      - https://www.coin-or.org/Bonmin/options_set.html#sec:opt%CB%99nonconv
      - `ThirdParty/Mumps/Makefile` の `FFLAGS` に `-fallow-argument-mismatch`を追加
    - [Bonmin](https://github.com/coin-or/Bonmin) : 凸混合整数非線形計画問題
    - [Couenne](https://github.com/coin-or/Couenne) : 非凸混合整数非線形計画問題
    - [Cbc](https://github.com/coin-or/Cbc) : 混合整数線形計画法(MILP)
    - [OpenMP](https://www.open-mpi.org/)
- docker
  - [suzuki-shm/PyomoContainer: Docker container for optimization with pyomo and some of MINLP solvers.](https://github.com/suzuki-shm/PyomoContainer)
  - [Docker で JupyterLab を起動し、token 入力なしでアクセスする #Python - Qiita](https://qiita.com/ao_log/items/5438f2aaf5c2b46d2ccb)
- その他参考
  - [Pyomo](https://www.pyomo.org/)
  - [Python + Pyomoによる(非線形)数値最適化 - Easy to type](https://ajhjhaf.hatenablog.com/entry/2018/02/12/235015)
  - [PyomoとCouenneで非凸の混合整数非線形計画問題(MINLP)を解く – Helve Tech Blog](https://helve-blog.com/posts/python/pyomo-couenne-nonconvex-minlp/)
  - [整数計画法による定式化入門, 藤江哲也, オペレーションズ・リサーチ 2012年4月号](https://web.tuat.ac.jp/~miya/fujie_ORSJ.pdf)
  - [BLASとLAPACKとIpOptのインストール - adragoonaの日記](https://adragoona.hatenablog.com/entry/20121215/1355585428)
  - [Linux RHEL｜blas-devel と lapack-devel のパッケージが yum install コマンドでインストールできない｜インストールする方法 - Technology.com](https://www.lifestyle12345.com/2022/12/linux-rhelblas-devel-lapack-devel-yum.html)
