<?php

// ATTENTION: Ne commitez JAMAIS ce fichier avec de vrais identifiants!
// Utilisez des variables d'environnement ou un fichier config.php non versionné

// Utilisez des variables d'environnement ou un fichier config.php non versionné
$host = getenv('DB_HOST') ?: 'your-host';
$dbname = getenv('DB_NAME') ?: 'your-database';
$port = getenv('DB_PORT') ?: '5433';
$username = getenv('DB_USER') ?: 'your-username';
$password = getenv('DB_PASSWORD') ?: 'your-password';

$db = new PDO("pgsql:host=$host;dbname=$dbname;port=$port", $username, $password);
$db->query("SET search_path TO $dbname");