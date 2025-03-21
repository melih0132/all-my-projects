<!DOCTYPE html>
<html>
<head>
	<meta charset="utf-8">
	<meta name="viewport" content="width=device-width, initial-scale=1">
	<title></title>
</head>
<body>
	<h1>Jeux vidéo</h1>

	<?php
	function loadMyClass($className) {
		include_once $className.".php";
	}
	spl_autoload_register('loadMyClass');


	$game = Game::load(16);
	var_dump($game);

	$category = Category::load(1);
	var_dump($category);

	?>

</body>
</html>