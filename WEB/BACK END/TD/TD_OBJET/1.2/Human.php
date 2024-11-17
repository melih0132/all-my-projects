<?php

class Human {
    private $name;
    private $genre;

    public function __construct($name, $genre) {
        $this->name = $name;
        $this->genre = $genre;
    }

    public function __get($property) {
        if (property_exists($this, $property)) {
            return $this->$property;
        } else {
            return "Propriété introuvable";
        }
    }

    public function __set($property, $value) {
        if (property_exists($this, $property)) {
            $this->$property = $value;
        }
    }

    public function __toString() {
        return "Identity: {$this->name}<br>Genre: {$this->genre}<br>";
    }
}

?>