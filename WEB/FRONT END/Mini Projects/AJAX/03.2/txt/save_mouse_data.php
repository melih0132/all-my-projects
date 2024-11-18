<?php
// Recevoir les données JSON du client
$data = file_get_contents('php://input');
$mouseData = json_decode($data, true);

// Formatage des données pour le fichier texte
$logEntry = date('Y-m-d H:i:s') . " - Type: " . $mouseData['type'] . ", X: " . $mouseData['x'] . ", Y: " . $mouseData['y'] . "\n";

// Enregistrer les données dans un fichier texte
$file = 'mouse_data.txt';
file_put_contents($file, $logEntry, FILE_APPEND | LOCK_EX);

echo "Données enregistrées avec succès !";
?>