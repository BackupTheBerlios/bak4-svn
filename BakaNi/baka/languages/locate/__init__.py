#!/usr/bin/env python2.4
# encoding: utf-8

# copyright (c) domenico carbotta <domenico.carbotta@gmail.com>, 2005
# code released under the gnu gpl, see license.txt


__all__ = ['process_loc']


from locparser import LocParser
from baka.languages.xpathlog.xplscanner import XPLScanner
from baka.languages.toolchain import processor


process_loc = processor(XPLScanner, LocParser)
