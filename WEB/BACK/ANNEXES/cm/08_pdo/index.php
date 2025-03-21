<?php

// CONNEXION
$db = new PDO("pgsql:host=localhost;dbname=r205", "ldama","hop");
$db->query("SET search_path TO games;");


// REQUETE EN LECTURE
$st = $db->prepare("SELECT * from game");
$st->execute();

// TRAITEMENT (AFFICHAGE)
// while ($row = $st->fetch(PDO::FETCH_ASSOC)) {
// 	echo $row["name"];
// }
var_dump($st->fetchAll());

$st = $db->prepare("insert into game(name,category) values (:name,:category)");
$st->bindValue(":name", "Tiny Glade");
$st->bindValue(":category", "Too chilll!");
$st->execute();




