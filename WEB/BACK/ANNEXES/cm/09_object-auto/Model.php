<?php


class Model {

	public static function load($id) {
		// à ranger ailleurs
		$db = new PDO("pgsql:host=localhost;dbname=r205", "ldama","hop");
		$db->query("SET search_path TO games;");

		$class = get_called_class();  // $class="Game"
		$table = strtolower($class);  // $table="game"
		
		$stm = $db->prepare("select * from $table where id$table=:id");
		$stm->bindValue(":id", $id);
		$stm->execute();

		$result = $stm->fetch(PDO::FETCH_ASSOC);

		$object = new $class();
		forEach($result as $attr => $value)
			$object->$attr = $value;

		return $object;

	}

}