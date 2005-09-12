# encoding: latin-1

xpl = '''
    //reparto[@nome ~= "ricerca e sviluppo",
            dipendente[@livello->$L, @stipendio->$W],
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
    <dipendente nome="?n" livello="1" stipendio="?w">
        <incarico>?i</incarico>
    </dipendente>
'''
