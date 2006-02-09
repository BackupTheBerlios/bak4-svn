#!/usr/bin/env python2.4
# encoding: utf-8

# copyright (c) domenico carbotta <domenico.carbotta@gmail.com>, 2005
# code released under the gnu gpl, see license.txt


__all__ = ['process_sdd']


from sddparser import SDDParser
from sddscanner import SDDScanner
from ima.languages.toolchain import processor


process_sdd = processor(SDDScanner, SDDParser)
