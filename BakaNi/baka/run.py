#!/usr/bin/env python2.4
# encoding: utf-8

# copyright (c) domenico carbotta <domenico.carbotta@gmail.com>, 2005
# code released under the gnu gpl, see license.txt


from baka.languages.xpathlog import *
from baka.languages.sdd import *
from baka.languages.locate import *
from baka.languages.xmltranslator.xmltranslator import *
from baka.postprocessor.expander import *
from baka.postprocessor.dlgenerator import *
from baka.postprocessor.hypgenerator import *
from baka.util.vargenerator import *
from baka.cli.options import get_options
from baka.classes.atom import *


def print_denials(denials, human_readable=True, prefix='\t'):
    if not human_readable:
        print render_denials(denials)
        return
    for denial in denials:
        print prefix, '<-',
        print (',\n\t' + prefix).join(
                [x.render() for x in denial])


def render_denials(denials):
    ds = []
    for denial in denials:
        ds.append('\t[' + ', '.join([x.render() for x in denial]) + ']')
    return '[\n' + ',\n'.join(ds) + '\n]'


def process_xpl_on_steroids(xpl_string, sdd_p):
    xpl_p = process_xpl(string=xpl_string)
    xpl_nf = expand(xpl_p, sdd_p)
    xpl_dl = generate_datalog(xpl_nf, sdd_p)
    return xpl_dl


def process_loc_on_steroids(loc_string, sdd_p):
    loc_res = process_loc(string=loc_string)
    loc_p = loc_res.atoms
    loc_nf = expand(loc_p, sdd_p, var_format='?pp')
    loc_datalog = generate_datalog(loc_nf, sdd_p)
    
    loc_denials = []
    for loc_atoms in loc_datalog:
        loc_denials.extend(generate_hypotheses(loc_atoms))
    return loc_denials, loc_res


def main(human_readable=False):
    
    from baka.usecases import case_zero as case
    
    sdd_p = process_sdd(string=case.sdd)
    
    xpl_dl = process_xpl_on_steroids(case.xpl, sdd_p)
    loc_denials, loc_res = process_loc_on_steroids(case.loc, sdd_p)
    
    xml_translator = XMLTranslator(sdd_p)
    
    xml_p = xml_translator.translate(case.fragment, loc_res.doctype,
            loc_res.ip_type, loc_res.ip)
    xml_denials = xml_translator.create_append_hyp(xml_p, loc_res.doctype,
            loc_res.ip_type, loc_res.ip)
    
    cmp_denials = [
        [AuxAtom('<', ('X', 'X'))],
        [AuxAtom('<', ('X', 'Y')), AuxAtom('<', ('Y', 'X'))],
        [AuxAtom('<', ('X', 'Y')), AuxAtom('<', ('Y', 'Z')),
                AuxAtom('<', ('Z', 'X'))],
        [AuxAtom('<', ('X', 'Y')), AuxAtom('<', ('Y', 'Z')),
                AuxAtom('=', ('Z', 'X'))]
        ]
    
    print
    print '-' * 60
    print 'vincoli:'
    print_denials(xpl_dl, human_readable)
    
    print
    print 'descrizione del frammento xml:'
    print '[', ','.join(map(str, xml_p)), ']'
    
    print
    print 'ipotesi aggiuntive dell\'operazione di append:'
    print_denials(xml_denials, human_readable)
    
    print
    print 'ipotesi aggiuntive dalla localizzazione dell\'append:'
    print_denials(loc_denials, human_readable)
    
    print
    print '-' * 80
    print '[simp].   simp('
    print '[', ', '.join(map(str, xml_p)), '],'
    print_denials(xml_denials + loc_denials + cmp_denials, False, '')
    print ','
    print_denials(xpl_dl, False, '')
    print ', S).'


if __name__ == '__main__':
    main()
