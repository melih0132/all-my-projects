<?php

spl_autoload_register(function ($class_name) {
    include $class_name . '.php';
});

$batman = new SuperHero(
    "Batman", 
    "Bruce Wayne", 
    ["black"]
);

$batman->name = "Dark Knight";
$batman->colors = ["black", "gray"];

echo $batman;

var_dump($batman);