
@extends('layouts.app')

@section('title', 'LeBonCoin')



@section('content')
   <h2>Location : {{ $post->title }}</h2>

   <p>{{ $post->descr }}</p>
   <p>{{ $post->price }}€</p>
   <p>{{ $post->nbrooms }}</p>

   <p><a href="{{ url("/posts") }}">Retour...</a></p>


@endsection

