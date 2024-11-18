<?php

class Human extends Model {
    protected static $table = 'human';
    protected $idhuman;
    protected $name;
    protected $firstname;
    
    public function getIdHuman() { return $this->idhuman; }
    public function getName() { return $this->name; }
    public function getFirstname() { return $this->firstname; }
}