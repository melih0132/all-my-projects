<?php

abstract class Model {
    protected static $table;
    
    public static function all() {
        $db = DB::getInstance();
        $table = static::$table;
        $query = $db->query("SELECT * FROM $table");
        return $query->fetchAll(PDO::FETCH_CLASS, get_called_class());
    }
    
    public static function find($id) {
        $db = DB::getInstance();
        $table = static::$table;
        $stmt = $db->prepare("SELECT * FROM $table WHERE id_{$table} = ?");
        $stmt->execute([$id]);
        $stmt->setFetchMode(PDO::FETCH_CLASS, get_called_class());
        return $stmt->fetch();
    }
}