<?php

$table = [];

$table = isset($_GET['table']) ? $_GET['table'] : 'vehicule'; //TODO : Faire en sorte qu'il récupère toutes les tables de la db
$id = isset($_GET['id']) ? $_GET['id'] : null;
$class = ucfirst($table);

var_dump($table);

try {
    if ($id) {
        $data = $class::find($id);
    } else {
        $data = $class::all();
    }
} catch (Exception $e) {
    die("Error: " . $e->getMessage());
}