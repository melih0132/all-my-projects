<?php

function loadMyClass($className) {
    include_once $className . ".php";
}

spl_autoload_register('loadMyClass');
include_once "db.php";
include_once "controller.php";
include_once "view.php";