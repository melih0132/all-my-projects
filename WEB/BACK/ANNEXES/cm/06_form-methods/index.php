<?php session_start(); ?>
<!DOCTYPE html>
<html>
<head>
	<meta charset="utf-8">
	<meta name="viewport" content="width=device-width, initial-scale=1">
	<title></title>
</head>
<body>
	<h1>Quel est ton âge ?</h1>

	<form method="post" action="calc.php">
		<div>
			<label for="ageInput">Dis moi ton âge</label>
			<input type="number" name="age" value="19" id="ageInput">
		</div>
		<div>
			<label for="actionInput"></label>
			<input type="submit" name="action" id="actionInput" value="HOP">
		</div>
	</form>

	<h2>Ton âge en minutes</h2>
	<p>
	<?php
	if (isset($_SESSION["age"]))
		echo "Tu as ".$_SESSION["age"]." !";
	?>
	</p>


</body>
</html>