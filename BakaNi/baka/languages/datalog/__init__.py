#!/usr/bin/env python2.4
# encoding: utf-8

# copyright (c) domenico carbotta <domenico.carbotta@gmail.com>, 2005
# code released under the gnu gpl, see license.txt


__all__ = ['process_dlg', 'dltest']


from dlgparser import DatalogParser
from dlgscanner import DatalogScanner
from baka.languages.toolchain import processor


process_dlg = processor(DatalogScanner, DatalogParser)


def dltest():    
    from baka.languages.sdd import process_sdd
    
    from baka.usecases.azienda import sdd
    
    test_datalog = '''[[
    'dipendente@azienda'('Auto_Step1', 'Auto_X68', 'Auto_Step0', 'Auto_X69',
            'Auto_Step3', 'Auto_Step2'),
    'reparto@azienda'('Auto_Step0', 'Auto_X70', 'Auto_Post1', 'Auto_Step6',
            'Auto_X71'),
    'sede@azienda'('Auto_Post1', 'Auto_X72', 'Auto_Post0', 'Auto_X73'),
    'azienda@azienda'('Auto_Post0', 'Auto_X74', 'x_doc0', 'Auto_X75'),
    'dipendente@azienda'('Auto_Step4', 'Auto_X76', 'Auto_Step0', 'Auto_X77',
            'Var_L', 'Auto_Step5'),
    '!document'('x_doc0', 'x_!default'),
    '='('Var_W', 'Auto_Step5'),
    '<'('Auto_Step2', 'Var_W'),
    '<'('Var_L', 'Auto_Step3'),
    '<'('10000', 'Auto_Step5'),
    '~='('Auto_Step6', 's_ricerca e sviluppo')
    ]]'''    
    DatalogParser.dtcollection = process_sdd(string=sdd)
    rv = process_dlg(string=test_datalog, debug=True)
    print '---'
    return rv


if __name__ == '__main__':
    print dltest()