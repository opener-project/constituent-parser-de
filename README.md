Constituent Parser German
=========================

Introduction
------------

This is a parser for German text using the Stanford parser
(<http://nlp.stanford.edu/software/lex-parser.shtml>). The input for this module
has to be a valid KAF file with at least the text layer. The output will be the
constituent trees in pennTreebank format for each of the sentences in the input
KAF.

The tokenization and sentence splitting is taken from the input KAF file, so if
your input file has a wrong tokenization/splitting, the output could contain
errors. The number of output constituent trees will be exactly the same as the
number of sentences in your input KAF

Requirements
-----------

* VUKafParserPy: parser in python for KAF files
  (<https://github.com/opener-project/VU-kaf-parser>)
* lxml: library for processing xml in python
* Stanford parser: http://nlp.stanford.edu/software/lex-parser.shtml

How to run the module with Python
---------------------------------

You can run this module from the command line using Python. The main script is
core/stanford_parser_de.py. This script reads the KAF from the standard input
and writes the output to the standard output, generating some log information
in the standard error output. To process one file just run:

    cat input.kaf | core/stanford_parser_de.py > input.tree

This will read the KAF file in "input.kaf" and will store the constituent trees
in "input.tree".

Contact
------

* Ruben Izquierdo
* Vrije University of Amsterdam
* ruben.izquierdobevia@vu.nl