#!/usr/bin/env python

import sys
import getopt
import codecs
import os
import tempfile
from subprocess import Popen,PIPE
import shutil
import glob
import logging


__module_folder__ = os.path.dirname(__file__)

# This updates the load path to ensure that the local site-packages directory
# can be used to load packages (e.g. a locally installed copy of lxml).
sys.path.append(os.path.join(__module_folder__, 'site-packages/pre_build'))
sys.path.append(os.path.join(__module_folder__, 'site-packages/pre_install'))

from VUKafParserPy import KafParser
from lxml import etree

## CONFIGURATION FOR THE STANFORD PARSER #

STANFORD_HOME=os.path.join(__module_folder__,'vendor','stanford-parser')
STANFORD_MEM="3g"
STANFORD_GERMAN_OPTS='-hMarkov 1 -vMarkov 2 -vSelSplitCutOff 300 -uwm 1 -unknownSuffixSize 2 -nodeCleanup 2 -encoding UTF-8'
STANFORD_PARSER_OPTS='-tokenized'
STANDFORD_GRAMMAR='edu/stanford/nlp/models/lexparser/germanPCFG.ser.gz'
##########################################

logging.basicConfig(stream=sys.stderr,format='%(asctime)s - %(levelname)s - %(message)s',level=logging.DEBUG)

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


# Creating a temp file with the input
tmp_file = tempfile.NamedTemporaryFile(mode='w', delete=False)
for sentence in sentences:
    for token in sentence:
        tmp_file.write(token.encode('utf-8')+' ')
    tmp_file.write('\n')
tmp_file.close()
######################################

cmd = 'java -Xmx"'+STANFORD_MEM+'" -cp "'+STANFORD_HOME+'/*:" edu.stanford.nlp.parser.lexparser.LexicalizedParser -maxLength "1000" '
cmd+= ' -tLPP "edu.stanford.nlp.parser.lexparser.NegraPennTreebankParserParams" '+STANFORD_GERMAN_OPTS+' '+STANFORD_PARSER_OPTS
cmd+= ' -outputFormat "oneline" -outputFormatOptions "markHeadNodes" -sentences newline -loadFromSerializedFile '+STANDFORD_GRAMMAR
cmd+=' '+tmp_file.name

stanford_process = Popen(cmd,stdout=PIPE,stderr=PIPE,shell=True)
code = stanford_process.wait()
logging.debug('Stanford parser finished with code:'+str(code))
stanford_output = stanford_process.stdout.read()
stanford_error = stanford_process.stderr.read()
logging.debug('STANFORD LOG: '+ stanford_error)
print stanford_output.strip()

os.remove(tmp_file.name)
sys.exit(0)

