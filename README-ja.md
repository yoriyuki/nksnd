# nksnd: オープンソースかな漢字変換

Copyright (C) 2016, 2017: National Institute of Advanced Industrial Science and Technology (AIST)

Copyright (C) 2016: Yoh Okuno

BCCWJパーサーは奥野陽さんの[neural_ime](https://github.com/yohokuno/neural_ime/blob/master/LICENSE)に由来します。ライセンスは同じです。

Pythonでフルスクラッチで書かれています。

## インストール

```shell
$ tar -xzvf nksnd-<version>.tar.gz
$ cd nksnd-<version>
$ python setup.py build
$ python setup.py install
```

## 使い方

`nksndconv`というコマンドがインストールされます。

平文による入出力
```shell
$ nksndconv
きょうはいいてんき
今日はいい天気
```

S式による入出力
```shell
$ nksndconv -m sexp
("best-path" "きょうはいいてんき")
(("今日" "きょう") ("は" "は") ("言" "い") ("い" "い") ("天気" "てんき"))
("list-candidates" (("今日" "きょう") ("は" "は")) "いい" 0)
(("唯々" "いい") ("井伊" "いい"))
```
