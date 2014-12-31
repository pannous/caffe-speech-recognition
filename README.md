Speech Recognition with BVLC caffe
==================================

Speech Recognition with the [caffe](https://github.com/BVLC/caffe) deep learning framework

1)  training digits:

  *) get spectograph training images from http://pannous.net/spoken_numbers.tar (470 MB)
  
  *) start train.sh
  
  *) test with record.py script


2) training words:

 *) 4GB of training [data](https://www.dropbox.com/s/eb5zqskvnuj0r78/spoken_words.tar?dl=0) [*](http://pannous.net/spoken_words.tar)

 *) net topology: work in progress ...

 *) todo: link TIMIT dataset, use new caffe LSTM layers etc

Theoretical background: papers

O. Vinyals, S. V. Ravuri, and D. Povey. Revisiting recurrent neural networks for robust ASR. In ICASSP, 2012

[Ng et al / Baidu](http://arxiv.org/abs/1412.5567)

[Hinton et al / Toronto](http://www.cs.toronto.edu/~hinton/absps/RNN13.pdf)

[good old Hinton](http://psych.stanford.edu/~jlm/pdfs/Hinton12IEEE_SignalProcessingMagazine.pdf)
