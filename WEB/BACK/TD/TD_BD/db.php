<?php

$db = new PDO("pgsql:host=srv-peda.iut-acy.local;dbname=db_php_vehicules;port=5433", "cetinkam", "7jhqDh");
$db->query("SET search_path TO db_php_vehicules");