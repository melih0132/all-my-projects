
@extends('layouts.app')

@section('title', 'LeBonCoin')



@section('content')
<h2>Les locations</h2>
<ul>
   @foreach ($posts as $post)
       <li>
       	<a href="{{ url("/post/".$post->idpost) }}">       		
       		{{ $post->title }}
       	</a>
       </li>
  @endforeach
</ul>
@endsection

