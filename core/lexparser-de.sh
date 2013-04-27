#!/usr/bin/env bash

# Memory limit
mem=3g

# Language-specific configuration
tlp=edu.stanford.nlp.parser.lexparser.NegraPennTreebankParserParams
de_opts="-hMarkov 1 -vMarkov 2 -vSelSplitCutOff 300 -uwm 1 -unknownSuffixSize 2 -nodeCleanup 2 -encoding UTF-8"
parse_opts='-tokenized'
grammar=edu/stanford/nlp/models/lexparser/germanPCFG.ser.gz
len=1000


tmp_file=`mktemp tmpStanford.XXXXXX`
cat /dev/stdin > $tmp_file

# Run the Stanford parser
java -Xmx"$mem" -cp "$STANFORD_HOME/*:" edu.stanford.nlp.parser.lexparser.LexicalizedParser -maxLength "$len" \
-tLPP "$tlp" $de_opts $parse_opts -outputFormat "oneline" -outputFormatOptions "markHeadNodes" -sentences newline -loadFromSerializedFile $grammar $tmp_file

rm $tmp_file
