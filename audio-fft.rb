#!/usr/bin/env ruby
require "ruby-audio"
require "fftw3" #http://www.rubydoc.info/gems/fftw3/frames
require 'opencv'


include OpenCV

@window = GUI::Window.new('Spectogram') # Create a window for display.
`/usr/bin/osascript -e 'tell app "Finder" to set frontmost of process "ruby" to true'`

require 'ffi'

# module MyLib
#   extend FFI::Library
#   ffi_lib 'c'
#   attach_function :puts, [ :string ], :int
# end
# 
# MyLib.puts 'Hello, World using libc!'
# exit


#'sound.wav'
# AUDIO: 22050 Hz, 1 ch, s16be, 352.8 kbit/100.00% (ratio: 44100->44100)
# Selected audio codec: [pcm] afm: pcm (Uncompressed PCM)
# file=ARGV[0]||"/me/ai/phonemes/spoken_numbers/6_Steffi_220.wav"
file=ARGV[0]||"/me/ai/phonemes/spoken_numbers/6_Steffi_100.wav"
dir="/me/ai/phonemes/"
file="record-audio.wav"
file="/me/ai/phonemes/spoken_words/Zurich_Vicki_160.wav"
# info = RubyAudio::SoundInfo.new :channels => 1, :samplerate => 22050, :format => RubyAudio::FORMAT_AIFF|RubyAudio::FORMAT_PCM_16
# snd = RubyAudio::Sound.new "new.wav", 'r', info
def zeros len
  x=[]
  for i in 0...len
    x[i]=0
  end
  x
end

def randomm len
  x=[]
  for i in 0...len
    x[i]=rand(255)
  end
  x
end



# dir="/me/ai/phonemes/spoken_numbers/"
# files=Dir.entries(dir)
# for file in files
  # next if not file.to_s.match(/\.wav$/)
  # next if file.to_i<8
  file=dir+file if not file.match("/")
  puts file
  snd=RubyAudio::Sound.open(file) 
  buf = snd.read(:float,100000000)#, 100
  real_size=buf.real_size
  puts buf.real_size                         #=> 100

  
  # puts buf.methods-Object.methods
  # puts buf.entries
  #  chunk 
  # image=CvMat::new(100,100, CV_8U,  1) #CV_32F
  # image=CvMat::new(100,100, CV_32F,  1) #

  ab=buf.to_a

  # len=500
  len=1024
  # len=2048
  # step=256
  # step=128
  # step=32
  step=16
  height=len/2
  width=height
  zeross=zeros(height)
  for i in 0..len
    ab[real_size+i]=0 # fill for sliding fft (?)
  end
  
  as=[]
  # as=NArray.float(8,6)
  # as=CvMat::new(height,width, CV_8U,  1) 
  as[0]=zeross
  as[1]=zeross
  as[2]=zeross
  i=3      
  while i*step+len<buf.real_size #and i<width
    arr=ab[i*step..i*step+len];
    fc = FFTW3.fft(arr)
    arr=(fc.abs*80).to_a
    arr=arr.map{|x|x=x[0]if x.is_a?Array; (x>255 ? 255 : x)}
    shift=0#rand(10) # increase by an octave or so LOOKS WRONG!!
    as[i]=arr[height-shift...-1-shift] #Drop redundant symmetry
    i=i+1
  end
  as=as[0..width] if(i>width) #HACK!
    
  
  # fill with black
  while i<width
    # as[i]=randomm(height)# zeross
      as[i]=zeross
    i=i+1
  end
  
    # puts as.size
    # puts as[0].size
    # puts as[5]
  #   puts as.flatten.size
    # image=CvMat::new(width,height,CV_32F,  1)
    image=CvMat::new(width,height,CV_8U,  1)
    image.set_data(as)
  # image.set_data(as[0..128].flatten)
   # image=as
  out=file+".spec.png"
    # out=file+".spec.bmp"

  # image=image.resize(CvSize.new(len,as.size*4)) #better?
  image=image.t
  image.save(out)
  puts out
    
  # image[0]=as.flatten
  # puts image
  # image=image.resize(CvSize.new(len,2000))
  image=image.resize(CvSize.new(width/2,height/2))
  # image=image.resize(CvSize.new(len,as.size*4))
  # image=image.resize(CvSize.new(len,as.size*4))
  # image=image.resize(CvSize.new(height,as.size*4))
  @window.show(image) 
  exit if GUI::wait_key(1)
  GUI::wait_key
# end

#  record see PortAudio OR
# sox -d --norm -t .wav - silence -l 1 0 1% 1 6.0 1% rate 16k | lame -V2 - out.mp3


# Writing Example:
# buf = RubyAudio::Buffer.float(1000)
# out = RubyAudio::Sound.open('out.wav', 'w', snd.info.clone) if out.nil?
# while snd.read(buf) != 0
#   out.write(buf)
# end


# na = NArray.float(8,6)   # float -> will be corced to complex
# fc = FFTW3.fft(na)/na.length  # forward 2D FFT and normalization

# NArray: shape sizes size total length rank dim dimension typecode element_size empty? coerce reshape reshape! shape= newdim newrank newdim! newdim= newrank! newrank= flatten flatten! fill! fill indgen! indgen where where2 each collect collect! map map! to_f to_i to_type to_binary to_type_as_binary to_string refer original to_a [] []= slice count_false count_true mask + - * / % mod & | ^ ** add! sbt! mul! div! mod! imag= swap_byte hton ntoh htov vtoh -@ recip abs real imag image angle arg conj conjugate conj! conjugate! im floor ceil round ~ not eq ne gt ge lt le and or xor mul_add mul_accum sum accum prod min max cumsum! cumsum cumprod! cumprod sort sort! sort_index transpose random! random integer? complex? all? any? none? rank_total delete_at mean stddev rms rmsdev median randomn randomn! reverse rot90

=begin BUFFER channels size real_size real_size= type each [] []= to_a entries sort sort_by grep count find detect find_index find_all select reject collect map flat_map collect_concat inject reduce partition group_by first all? any? one? none? min max minmax min_by max_by minmax_by member? each_with_index reverse_each each_entry each_slice each_cons each_with_object zip take take_while drop drop_while cycle chunk slice_before lazy */ 
=end