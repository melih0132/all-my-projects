<?php
session_start();

// var_dump($_POST);
// var_dump($_GET);


$_SESSION["age"] = $_POST["age"]*365*24*60;

// Erreur 500 : pas d'espace avec ":"
header("Location: .");

