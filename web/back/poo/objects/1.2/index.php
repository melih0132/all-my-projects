<?php

spl_autoload_register(function ($class_name) {
    include $class_name . '.php';
});

$alfred = new Human(
    "Alfred",
    "Male"
);

echo $alfred . '<br>';

var_dump($alfred);

$batman = new SuperHero(
    "Bruce Wayne", 
    "Male", 
    "Batman", 
    ["Black"]
);

$batman->name = "Dark Knight";
$batman->colors = ["Black", "Gray"];

echo $batman . '<br>';

var_dump($batman);

$joker = new SuperVilain(
    "Joker", 
    "Male", 
    ["Yellow","Purple"]
);

echo $joker;

var_dump($joker);