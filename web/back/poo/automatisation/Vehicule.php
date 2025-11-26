<?php

class Vehicule extends Model {
    protected static $table = 'vehicule';
    protected $idvehicule;
    protected $model;
    protected $brand;
    protected $power;
    protected $color;
    protected $energy;
    protected $price;
    
    public function getIdVehicule() { return $this->idvehicule; }
    public function getModel() { return $this->model; }
    public function getBrand() { return $this->brand; }
    public function getPower() { return $this->power; }
    public function getColor() {
        $colors = unserialize($this->color);
        if (is_array($colors)) {
            return implode(', ', array_map('ucfirst', $colors));
        }
        return $this->color;
    }    
    public function getEnergy() { return $this->energy; }
    public function getPrice() { return $this->price; }
}