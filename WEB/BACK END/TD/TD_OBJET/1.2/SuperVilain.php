<?php

class SuperVilain extends Human {
    private $colors;

    public function __construct($name, $genre, array $colors) {
        parent::__construct($name, $genre);
        $this->colors = $colors;
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
        return parent::__toString() .  "Colors : " . implode(", ", $this->colors);
    }
}

?>