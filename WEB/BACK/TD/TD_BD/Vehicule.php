<?php

class Vehicule {
    private $idVehicule;
    private $model;
    private $brand;
    private $power;
    private $color;
    private $energy;
    private $price;
    private static $pdo;

    public function __construct() {
        if (!self::$pdo) {
            self::$pdo = new PDO("pgsql:host=srv-peda.iut-acy.local;dbname=db_php_vehicules;port=5433", "cetinkam", "7jhqDh");
            self::$pdo->exec("SET search_path TO db_php_vehicules");
        }
    }

    public function __get($name) {
        if (property_exists($this, $name)) {
            return $this->$name;
        }
        throw new Exception("La propriété $name n'existe pas");
    }

    public function __set($name, $value) {
        if (property_exists($this, $name) && $name !== 'idvehicule') {
            $this->$name = $value;
            
            $stmt = self::$pdo->prepare("UPDATE vehicule SET $name = :value WHERE idvehicule = :id");
            try {
                $result = $stmt->execute([
                    ':value' => $value,
                    ':id' => $this->idvehicule
                ]);
                if (!$result) {
                    throw new Exception("Échec de la mise à jour dans la base de données");
                }
            } catch (PDOException $e) {
                throw new Exception("Erreur lors de la mise à jour : " . $e->getMessage());
            }
        } else {
            if ($name === 'idvehicule') {
                throw new Exception("Impossible de modifier l'identifiant du véhicule");
            } else {
                throw new Exception("La propriété $name n'existe pas");
            }
        }
    }

    public static function load($id) {
        if (!self::$pdo) {
            new self();
        }

        $stmt = self::$pdo->prepare("SELECT * FROM vehicule WHERE idvehicule = :id");
        $stmt->execute([':id' => $id]);
        $data = $stmt->fetch(PDO::FETCH_ASSOC);

        if (!$data) {
            throw new Exception("Aucun véhicule trouvé avec l'ID $id");
        }

        $Vehicule = new self();
        
        foreach ($data as $key => $value) {
            $Vehicule->$key = $value;
        }

        return $Vehicule;
    }
}