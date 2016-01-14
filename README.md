Speech Recognition with BVLC caffe
==================================

Speech Recognition with the [caffe](https://github.com/BVLC/caffe) deep learning framework

UPDATE: We are migrating to [tensorflow](https://github.com/pannous/tensorflow-speech-recognition/)

This project is quite fresh and only the first of three milestones is accomplished: 
Even now it might be useful if you just want to train a handful of commands/options (1,2,3..yes/no/cancel/...)

1)  training spoken **numbers**:
  * get spectogram training images from http://pannous.net/spoken_numbers.tar (470 MB)
  * start ./train.sh
  * test with `ipython notebook test-speech-recognition.ipynb`
    or `caffe test ...` or `<caffe-root>/python/classify.py`
  * 99% accuracy, nice!
  * online recognition and learning with `./recognition-server.py` and `./record.py` scripts

![Sample spectrogram, That's what she said, too laid?](https://raw.githubusercontent.com/pannous/caffe-speech-recognition/master/0_Karen_160.png)

Sample spectrogram, Karen uttering 'zero' with 160 words per minute.


2) training **words**:
 * 4GB of training [data](https://www.dropbox.com/s/eb5zqskvnuj0r78/spoken_words.tar?dl=0) [*](http://pannous.net/spoken_words.tar)
 * net topology: work in progress ...
 * todo: use [upcoming new](https://github.com/BVLC/caffe/issues/1653) caffe [LSTM](https://en.wikipedia.org/wiki/Long_short_term_memory) layers etc
 * UPDATE [LSTMs get rolling](https://github.com/BVLC/caffe/pull/1873), [still not merged](https://github.com/BVLC/caffe/pull/2033)
 * UPDATE since the caffe project leaders have a hindering merging policy and this pull request was shifted many times without ever being merged, we migrated to [tensorflow](https://github.com/pannous/tensorflow-speech-recognition)
 * todo: add extra categories for a) silence b) common noises like typing, achoo c) ALL other noises


3) training **speech**:
 * todo!
 * 100GB of training data here: http://www.openslr.org/12/
 * [TIMIT dataset](https://catalog.ldc.upenn.edu/memberships) $27,000.00 membership fee or [$250 for non-members](https://catalog.ldc.upenn.edu/LDC93S1)+[$2400 under research-only license](https://catalog.ldc.upenn.edu/LDC2016MNP)?
 * combine with google n-grams


Theoretical background: **papers**

A. Graves and N. Jaitly. Towards end-to-end speech recognition with recurrent neural networks. [In ICML, 2014](https://duckduckgo.com/l/?kh=-1&uddg=http%3A%2F%2Fjmlr.org%2Fproceedings%2Fpapers%2Fv32%2Fgraves14.pdf)

O. Vinyals, S. V. Ravuri, and D. Povey. Revisiting recurrent neural networks for robust ASR. [In ICASSP, 2012](http://research.microsoft.com/pubs/164627/4085.pdf)

[Andrew Ng et al](http://arxiv.org/pdf/1406.7806.pdf) / [Baidu](http://arxiv.org/abs/1412.5567)

[Hinton et al / Toronto](http://www.cs.toronto.edu/~hinton/absps/RNN13.pdf)

[good old Hinton](http://psych.stanford.edu/~jlm/pdfs/Hinton12IEEE_SignalProcessingMagazine.pdf)

[Schmidhuber et al](http://arxiv.org/pdf/1402.3511v1.pdf) using new 'ClockWork-RNNs'

The **book**:
[Automatic Speech Recognition: A Deep Learning Approach](http://www.amazon.com/Automatic-Speech-Recognition-Communication-Technology/dp/1447157788/ref=sr_1_1?ie=UTF8&qid=1422013427&sr=8-1&keywords=speech+recognition)  (Signals and Communication Technology) Hardcover – November 11, 2014 by Dong Yu (Author) and Li Deng (Author) 


**Related work**

Also see the [Kaldi](http://kaldi.sourceforge.net/about.html) project, which seems a bit messy but already uses deep learning with [LSTM](https://en.wikipedia.org/wiki/Long_short_term_memory)
Another experimental LSTM network, which works out-of-the-box: [Currennt](http://sourceforge.net/projects/currennt/)
