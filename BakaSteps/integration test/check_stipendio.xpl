//dipendente[@grado = "dirigente"]->$D//stipendio/@importo_mensile->$DW,
$D/../dipendente[@grado != "dirigente"]->$O//stipendio/@importo_mensile->$DO,
$DO >= $DW
