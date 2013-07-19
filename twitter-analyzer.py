from __future__ import division
from collections import defaultdict
from pylab import barh,show,yticks
import pycurl
import simplejson
import sys
import nltk
import re
import signal

def plot_histogram(freq, mean):
   # using dict comprehensions to remove not frequent words
   topwords = {word : count
      for word,count in freq.items()
      if count > round(2*mean)}
   # plotting
   y = topwords.values()
   x = range(len(y))
   labels = topwords.keys()
   barh(x,y,align='center')
   yticks(x,labels)
   show()


class TwitterAnalyzer:
   def __init__(self):
      self.freq = defaultdict(int)
      self.cnt = 0
      self.mean = 0.0
      # composing the twitter stream url
      nyc_area = 'locations=-74,40,-73,41'
      self.url = "https://stream.twitter.com/1.1/statuses/filter.json?"+nyc_area

   def begin(self,usr,pws):
      """
      init and start the connection with twitter using pycurl
      usr and pws must be valid twitter credentials
      """
      self.conn = pycurl.Curl()
      # we use the basic authentication,
      # in future oauth2 could be required
      self.conn.setopt(pycurl.USERPWD, "%s:%s" % (usr, pws))
      self.conn.setopt(pycurl.URL, self.url)
      self.conn.setopt(pycurl.WRITEFUNCTION, self.on_receive)
      self.conn.perform()

   def on_receive(self,data):
      """ Handles the arrive of a single tweet """
      self.cnt += 1
      tweet = simplejson.loads(data)
      # a little bit of natural language processing
      tokens = nltk.word_tokenize(tweet['text']) # tokenize
      tagged_sent = nltk.pos_tag(tokens) # Part Of Speech tagging
      for word,tag in tagged_sent:
         # filter sigle chars words and symbols
         if len(word) > 1 and re.match('[A-Za-z0-9 ]+',word):
            # consider only adjectives and nouns
            if tag == 'JJ' or tag == 'NN':
               self.freq[word] += 1 # keep the count
      
      # print the statistics every 50 tweets
      if self.cnt % 50 == 0:
         self.print_stats()


   def print_stats(self):
      maxc = 0
      sumc = 0
      for word,count in self.freq.items():
         if maxc < count:
            maxc = count
            sumc += count
      self.mean = sumc/len(self.freq)
      print '-------------------------------'
      print ' tweets analyzed:', self.cnt
      print ' words extracted:', len(self.freq)
      print '  max frequency:', maxc
      print ' mean frequency:', self.mean


   def close_and_plot(self,signal,frame):
      print ' Plotting...'
      plot_histogram(self.freq,self.mean)
      sys.exit(0)

      
usr ='supersexytwitteruser'
pws ="yessosexyiam"

ta = TwitterAnalyzer()# invoke the close_and_plot() method when a Ctrl-D arrives
signal.signal(signal.SIGINT, ta.close_and_plot)
ta.begin(usr,pws)# run the analysis
