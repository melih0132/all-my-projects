@extends('layouts.app')

@section('title', 'LeBonCoin')



@section('content')
	<h2>Ajouter une annonce</h2>

	<form method="post" action="{{ url("/post/save") }}">
	  @csrf
	  <p>{{ session()->get("errors") }}</p>

	  <div>
	  	<label>Titre</label>
	  	<input type="text" name="title" value='{{ old("title") }}'/>
	  </div>
	  <div>
	  	<label>Description</label>
	  	<input type="text" name="descr" value='{{ old("descr") }}'/>
	  </div>
	  <div>
	  	<label>Prix</label>
	  	<input type="number" name="price" value='{{ old("price") }}'/> €
	  </div>
	  <div>
	  	<label>Nombre de pièces</label>
	  	<input type="number" name="nbrooms" value='{{ old("nbrooms") }}'/>
	  </div>
	  <div>
	  	<label></label>
	  	<input type="submit" value="Ajouter"/>
	  </div>
	</form>

@endsection

