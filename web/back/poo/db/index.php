<!DOCTYPE html>
<html lang="fr">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>BD</title>
</head>

<body>
    <?php

    include_once "Vehicule.php";

    try {
        $v = Vehicule::load(1);
        echo "Prix initial : " . $v->price . "\n";
    
        $v->price = 100000;
        echo "Prix après modification : " . $v->price . "\n";
    
        $v = Vehicule::load(1);
        echo "Prix après rechargement : " . $v->price . "\n";
    
    } catch (Exception $e) {
        echo "Erreur : " . $e->getMessage();
    }

    ?>

</body>

</html>