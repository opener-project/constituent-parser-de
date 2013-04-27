#!/usr/bin/env python

import sys
import getopt
import codecs
import os
from VUKafParserPy import KafParser
from lxml import etree
import tempfile
from subprocess import Popen,PIPE
import shutil
import glob
import logging


logging.basicConfig(stream=sys.stderr,format='%(asctime)s - %(levelname)s - %(message)s',level=logging.DEBUG)

__module_dir = os.path.dirname(__file__)
STANFORD_HOME = '/Users/ruben/NLP_tools/stanford-parser-2013-04-05'
my_stanford_script = os.path.join(__module_dir,'lexparser-de.sh')


## MAIN ##

if not sys.stdin.isatty(): 
    ## READING FROM A PIPE
    pass
else:
    print>>sys.stderr,'Input stream required in KAF format at least with the text layer.'
    print>>sys.stderr,'The language encoded in the KAF has to be Dutch, otherwise it will raise an error.'
    print>>sys.stderr,'Example usage: cat myUTF8file.kaf.xml |',sys.argv[0]
    sys.exit(-1)

my_time_stamp = True
try:
  opts, args = getopt.getopt(sys.argv[1:],"",["no-time"])
  for opt, arg in opts:
    if opt == "--no-time":
      my_time_stamp = False
except getopt.GetoptError:
  pass
  
  
logging.debug('Starting stanford parser for German text')
logging.debug('Loading and parsing KAF file ...')
my_kaf = KafParser(sys.stdin)

lang = my_kaf.getLanguage()
if lang != 'de':
  print>>sys.stdout,'ERROR! Language is',lang,'and must be "de" (German)'
  sys.exit(-1)
  
logging.debug('Extracting sentences from the KAF')
sentences = []
current_sent = [] 
previous_sent = None
for token,sent,token_id in my_kaf.getTokens():
  if sent != previous_sent and previous_sent!=None:
    sentences.append(current_sent)
    current_sent = [token]
  else:
    current_sent.append(token)
  previous_sent = sent
  
if len(current_sent) !=0:
  sentences.append(current_sent)
  
 
logging.debug('Calling to Stanford parser for GERMAN in '+STANFORD_HOME)

## CALL TO STANFORD
os.environ['STANFORD_HOME'] = STANFORD_HOME
stanford_pro = Popen(my_stanford_script,stdin=PIPE,stdout=PIPE,stderr=PIPE,shell=True)

for sentence in sentences:
  for token in sentence:
    stanford_pro.stdin.write(token.encode('utf-8')+' ')
  stanford_pro.stdin.write('\n')
stanford_pro.stdin.close()

num_sents = 0
for line in stanford_pro.stdout:
  print line.strip()
  num_sents += 1
stanford_pro.terminate()
  
logging.debug('Number of sentences in the input KAF: '+str(len(sentences)))
logging.debug('Number of sentences generated (must be equal to num. sentences):'+str(num_sents))
logging.debug('PROCESS DONE')

sys.exit(0)