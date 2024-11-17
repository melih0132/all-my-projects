<?php
session_start();

$likes = (isset($_SESSION["likes"]) ? $_SESSION["likes"] : 0);

if(isset($_GET['likes'])) {
    $likes += $_GET['likes'];
}
$_SESSION["likes"] = $likes;

echo json_encode($_SESSION["likes"]);

?>