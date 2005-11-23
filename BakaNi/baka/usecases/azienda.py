# encoding: utf-8

xpl = '''
    //reparto[@nome ~= "ricerca e sviluppo",
            dipendente[@livello->$L, @stipendio->$W, @stipendio > 10000],
            dipendente[@livello > $L, @stipendio < $W]]
'''

sdd = '''
    !doctype azienda ("!default", "rossi.xml") {
        azienda -> (nome) sede, amministrazione;
        amministrazione -> (budget) dipendente;
        sede -> (citta) reparto;
        reparto -> (nome, budget) dipendente;
        dipendente -> (nome, livello, stipendio) incarico;
        incarico -> !PCDATA;
    }
'''

loc = '''
    //reparto[@nome="ricerca e sviluppo"]
'''

fragment = '''
    <dipendente nome="?n" livello="liv_1" stipendio="?w">
        <incarico>?i</incarico>
    </dipendente>
'''
