<?php
$file = 'mouse_data.txt';

if (file_exists($file)) {
    $data = file($file, FILE_IGNORE_NEW_LINES | FILE_SKIP_EMPTY_LINES);
    $mouseData = [];

    foreach ($data as $line) {
        // Extraire les coordonnées et le type d'événement depuis chaque ligne du fichier texte
        if (preg_match('/Type: (\w+), X: (\d+), Y: (\d+)/', $line, $matches)) {
            $mouseData[] = [
                'type' => $matches[1],
                'x' => (int)$matches[2],
                'y' => (int)$matches[3]
            ];
        }
    }

    // Retourner les données sous forme de JSON
    header('Content-Type: application/json');
    echo json_encode($mouseData);
} else {
    echo json_encode([]);
}
?>
