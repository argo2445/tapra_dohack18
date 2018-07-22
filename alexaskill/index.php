<?php
// Daten aus dem Request holen
$entityBody = file_get_contents ( 'php://input' );
 
// Datei namens echo.log öffen 
$datei_handle = fopen ( "echo.log", "w" );
 
// etwas validierung      
if (is_string($entityBody ) && json_decode ( $entityBody ) != null) {
// Request schoen formatieren
   fputs ( $datei_handle, "\n" );
   fputs ( $datei_handle, json_encode ( json_decode ( $entityBody ), JSON_PRETTY_PRINT ) );
   fputs ( $datei_handle, "\n" );
}
// alles speichern und beenden      
fclose ( $datei_handle );

?>

<?php
$ctr=0;
while (!file_exists('resp.txt') || filemtime('echo.log')>filemtime('resp.txt')){
  sleep(1);
  $ctr++;
  if($ctr>=6){
    break;
  }
}
if($ctr<6){
  $response=file_get_contents('resp.txt');

  $responseArray = [
            'version' => '1.0',
            'response' => [
                  'outputSpeech' => [
                        'type' => 'PlainText',
                        'text' => $response,
                        'ssml' => null
                  ],
                  'shouldEndSession' => true
            ]
      ];
  header ( 'Content-Type: application/json' );
  echo json_encode ( $responseArray );
}else{
  #$response=file_get_contents('resp.txt');

  $responseArray = [
            'version' => '1.0',
            'response' => [
                  'outputSpeech' => [
                        'type' => 'PlainText',
                        'text' => 'Bitte geben Sie einen Ort und einen Treibstoff an, um eine Tankempfehlung zu erhalten.',
                        'ssml' => null
                  ],
                  'shouldEndSession' => false
            ]
      ];
  header ( 'Content-Type: application/json' );
  echo json_encode ( $responseArray );
} 
?>
