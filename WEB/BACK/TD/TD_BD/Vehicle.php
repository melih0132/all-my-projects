<?php

class Vehicle {
    private $idvehicle;
    private $model;
    private $brand;
    private $power;
    private $color;
    private $energy;
    private $price;
    
    public function __construct($data) {
        foreach ($data as $key => $value) {
            $this->$key = $value;
        }
    }
    
    public static function load($id) {
        $stmt = DB::getInstance()->prepare("SELECT * FROM vehicle WHERE idvehicle = ?");
        $stmt->execute([$id]);
        $data = $stmt->fetch(PDO::FETCH_ASSOC);
        return $data ? new Vehicle($data) : null;
    }

    public function __set($name, $value) {
        $this->$name = $value;
        $stmt = DB::getInstance()->prepare("UPDATE vehicle SET $name = ? WHERE idvehicle = ?");
        $stmt->execute([$value, $this->idvehicle]);
    }
    
    public function __get($name) {
        return $this->$name;
    }
}

?>