Speech Recognition with BVLC caffe
==================================

Speech Recognition with the [caffe](https://github.com/BVLC/caffe) deep learning framework

Caution: This project is very fresh and only the first of three milestones is accomplished: 
Even now it might be useful if you just want to train a handful of commands/options (1,2,3..yes/no/cancel/...)

1)  training spoken **numbers**:
  * get spectograph training images from http://pannous.net/spoken_numbers.tar (470 MB)
  * start ./train.sh
  * test with `ipython notebook test-speech-recognition.ipynb`
    or `caffe test ...` or `<caffe-root>/python/classify.py`
  * online recognition with `./recognition-server.py` and `./record.py` script 
  needs "Build Python wrapper" in CMakeLists.txt and PYTHON_PATH environment variable  
  * todo: add extra categories for a) silence b) common noises like typing, achoo c) ALL other noises


2) training **words**:
 * 4GB of training [data](https://www.dropbox.com/s/eb5zqskvnuj0r78/spoken_words.tar?dl=0) [*](http://pannous.net/spoken_words.tar)
 * net topology: work in progress ...
 * todo: use new caffe LSTM layers etc


3) training **speech**:
 * todo!
 * 100GB of training data here: http://www.openslr.org/12/
 * [TIMIT dataset](https://catalog.ldc.upenn.edu/memberships) $27,000.00 membership fee?
 * combine with google n-grams


Theoretical background: **papers**

A. Graves and N. Jaitly. Towards end-to-end speech recognition with recurrent neural networks. [In ICML, 2014](https://duckduckgo.com/l/?kh=-1&uddg=http%3A%2F%2Fjmlr.org%2Fproceedings%2Fpapers%2Fv32%2Fgraves14.pdf)

O. Vinyals, S. V. Ravuri, and D. Povey. Revisiting recurrent neural networks for robust ASR. [In ICASSP, 2012](http://research.microsoft.com/pubs/164627/4085.pdf)

[Ng et al / Baidu](http://arxiv.org/abs/1412.5567)

[Hinton et al / Toronto](http://www.cs.toronto.edu/~hinton/absps/RNN13.pdf)

[good old Hinton](http://psych.stanford.edu/~jlm/pdfs/Hinton12IEEE_SignalProcessingMagazine.pdf)


Also see the [Kaldi](http://kaldi.sourceforge.net/about.html) project, which seems a bit messy but already uses deep learning with LSTM 
