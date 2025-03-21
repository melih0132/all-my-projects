<?php
class Model {

	function __construct($name, $category="RPG") {
		$this->name = $name;
		$this->category = $category;
	}

	function __get($attr) {
		return $this->$attr;
	}
	function __set($attr, $value) {
		if (property_exists("Game", $attr))
			$this->$attr = $value;
		else
			Throw(new Exception("T'as pas le droit !! Tu utilises '".$attr."' alors que ça n'existe pas dans la classe que tu es toi même en train de définir, boulet !"));
	}

	function __toString() {
		return $this->name." ".$this->category;
	}
}


class Game extends Model {
	protected $name;
	protected $category;
}

class User extends Model {
	protected $login;
	protected $passwd;
}

$worms = new Game("Worms", "BGE");
echo $worms->name;
echo $worms;
// $worms->year = 1995;
$worms->category = "BGE !!";
var_dump($worms);







// $z = 42;
// $x = "z";
// $y = "x";

// echo $$$y;
