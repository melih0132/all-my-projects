<?php

class SuperVilain extends Human {
    private $colors;

    public function __construct($name, $genre, array $colors) {
        parent::__construct($name, $genre);
        $this->colors = $colors;
    }

    public function __say($text) {
        $text = strrev($text);
        return "{$this->name}: {$text}";
    }

    public function __toString() {
        return parent::__toString() . "Colors: " . implode(", ", $this->colors) . "<br>";
    }
}

?>