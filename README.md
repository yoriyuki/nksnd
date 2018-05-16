# nksnd: Kana-kanji conversion engine

Copyright (C) 2016, 2017: National Institute of Advanced Industrial Science and Technology (AIST)

Copyright (C) 2016: Yoh Okuno

Partially based on [neural_ime](https://github.com/yohokuno/neural_ime/blob/master/LICENSE) by Yoh Okuno licensed under the same license.

## Installation

```shell
$ tar -xzvf nksnd-<version>.tar.gz
$ cd nksnd-<version>
$ python setup.py build
$ python setup.py install
```

## Usage

the program called `nksndconv` is installed.

For one-line-per-sentence inputs
```shell
$ nksndconv
```

For S-expression API
```shell
$ nksndconv -m sexp
("best-path" "きょうはいいてんき")
(("今日" "きょう") ("は" "は") ("言" "い") ("い" "い") ("天気" "てんき"))
("list-candidates" (("今日" "きょう") ("は" "は")) "いい" 0)
(("唯々" "いい") ("井伊" "いい"))
```
