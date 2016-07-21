# nksnd: Kana-kanji conversion engine

Copyright (C) 2016: National Institute of Advanced Industrial Science and Technology (AIST)

## Status
Currently, nksnd is under development and not usable as a conversion engine.  The supposed user is a developer who want to develop a new kana-kanji or similar conversion engine.

## Download
Clone from github.  There is no master branch.  Currently there is only one integration branch:

- nksnd-warabi

To train the engine, you also need a corpus which consists of morphemes separated by white spaces.

## Installation
No installation procedure is provided yet.  nksnd depends on several packages.  If you use Anaconda, you can create the environment for nksnd by loading environment.yml at the top directory.

## Usage
To train the engine:
Go to nksnd directory and
```shell
python build_lm.py ../../corpus/*.word
```
This assumes that corpuses are located in ../../corpus/\*.word files.  
```shell
python build_lm.py --help
```
shows the help for detailed options.

To put the score to the Japanese sentence, use
```shell
python calculate_score.py < samples.txt
```
It is assumed that samples.txt contains a sentence in each line.  A sentence is a sequence of morphemes, which are separated by white spaces.  Then, the command above outputs csv format of sentences and probabilities to stdout.
