<?php

// Fichier d'exemple - Copiez vers db.php et configurez vos identifiants
// ATTENTION: Ne commitez JAMAIS db.php avec de vrais identifiants!

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

