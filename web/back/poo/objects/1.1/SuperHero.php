<?php

class SuperHero {
    private $name;
    private $identity;
    private $colors;

    public function __construct($name, $identity, array $colors) {
        $this->name = $name;
        $this->identity = $identity;
        $this->colors = $colors;
    }

    public function __get($property) {
        if (property_exists($this, $property)) {
            return $this->$property;
        }
        else {
            return "Propriété introuvable";
        }
    }

    public function __set($property, $value) {
        if (property_exists($this, $property)) {
            $this->$property = $value;
        }
    }

    public function __toString() {
        return "SuperHero: {$this->name}<br> Identity: {$this->identity}<br> Colors: " . implode(", ", $this->colors);
    }
}

?>