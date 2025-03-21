<?php

class DB {
    private static $instance = null;
    
    public static function getInstance() {
        if (self::$instance === null) {
            try {
                self::$instance = new PDO("pgsql:host=srv-peda.iut-acy.local;dbname=db_php_vehicules;port=5433", "cetinkam", "7jhqDh");
                self::$instance->query("SET search_path TO db_php_vehicules");
            } catch (PDOException $e) {
                die("Connection failed: " . $e->getMessage());
            }
        }
        return self::$instance;
    }
}