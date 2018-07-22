<?php
// Daten aus dem Request holen
$entityBody = file_get_contents ( 'php://input' );
 
// Datei namens echo.log öffen 
$datei_handle = fopen ( "resp.txt", "a+" );
 
// etwas validierung      
if (is_string($entityBody )) {
// Request schoen formatieren
   fputs ( $datei_handle, $entityBody );
}
// alles speichern und beenden      
fclose ( $datei_handle );
echo $entityBody;
?>