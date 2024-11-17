<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>OBJET</title>
</head>
<body>
  <?php
  spl_autoload_register(function ($class_name) {
    include $class_name . '.php';
});

$list = 
array(
  array("name" => "Batman", 
  "gender" => "Male", 
  "identity" => "Bruce Wayne", 
  "colors"   => array("black") 
),
  array("name" => "Superman", 
  "gender" => "Male", 
  "identity" => "clark Kent", 
  "colors" => array("red","blue") 
),
  array("name" => "Flash", 
  "gender" => "Male", 
  "identity" => "Barry Allen", 
  "colors" => array("Red","Yellow") 
  )
);

$superHeroes = SuperHero::__createSuperHero($list);

SuperHero::__renderTable($superHeroes);
  ?>
</body>
</html><?php

/* $alfred = new Human(
  "Alfred",
  "Male"
);

echo $alfred . '<br>';

echo $alfred->__say("ohoho");

var_dump($alfred);


$joker = new SuperVilain(
  "Joker", 
  "Male", 
  ["Yellow","Purple"]
);

echo $joker . '<br>';

echo $joker->__say("hilem");

var_dump($joker);

$batman = new SuperHero(
  "Bruce Wayne", 
  "Male", 
  "Batman", 
  ["Black"]
);

echo $batman . '<br>';

echo $batman->__say("ahhh");

var_dump($batman); */