<?php

// ATTENTION: Ne commitez JAMAIS ce fichier avec de vrais identifiants!
// Utilisez des variables d'environnement ou un fichier config.php non versionné

class DB {
    private static $instance = null;
    
    public static function getInstance() {
        if (self::$instance === null) {
            try {
                // Utilisez des variables d'environnement ou un fichier config.php non versionné
                $host = getenv('DB_HOST') ?: 'your-host';
                $dbname = getenv('DB_NAME') ?: 'your-database';
                $port = getenv('DB_PORT') ?: '5433';
                $username = getenv('DB_USER') ?: 'your-username';
                $password = getenv('DB_PASSWORD') ?: 'your-password';
                
                self::$instance = new PDO("pgsql:host=$host;dbname=$dbname;port=$port", $username, $password);
                self::$instance->query("SET search_path TO $dbname");
            } catch (PDOException $e) {
                die("Connection failed: " . $e->getMessage());
            }
        }
        return self::$instance;
    }
}