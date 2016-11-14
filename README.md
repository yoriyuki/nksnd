# nksnd: Kana-kanji conversion engine

Copyright (C) 2016: National Institute of Advanced Industrial Science and Technology (AIST)

## Status
Currently, nksnd is under development. It can learn a language model from corpus and convert hiragana inputs to kanjis.  But (in particular) learning is very slow.  The converter converts hiragana inputs to kanjis per line, but no IME server is provided.  Curretly, the supposed user of nksnd is a developer who want to develop a new kana-kanji or similar conversion engine.

## Download
Clone from github.  There is no master branch.  Currently there are two integration branches:

- nksnd-okegawa
- nksnd-ageo

nksnd-ageo is python version while nksnd-okegawa is (to be) a C++ implementation.

To train the engine, you also need a corpus which consists of morphemes which are represented as \<surface form\>/\<reading\> separated by white spaces.

## Installation
No installation procedure is provided yet.  nksnd depends on maxent (https://github.com/yoriyuki/maxent)

## Usage
To train the engine:
Go to nksnd directory and
```shell
python build_lm.py ../../corpus/*.wordkkci
```
This assumes that corpuses are located in ../../corpus/\*.wordkkci files.
```shell
python build_lm.py --help
```
shows the help for detailed options.

```shell
python converter.py < sample.txt
```
It is assumed that samples.txt contains a sentence in hiraganas in each line.  Then, the command outputs a converted result in each line.
