<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use App\Models\Post;

class PostController extends Controller
{
    public function index() {
        return view ("post-list", ['posts'=>Post::all() ]);
    }

    public function one($id) {
        return view ("one-post", ['post'=>Post::find($id) ]);
    }

    public function addForm() {
        return view("add-form");
    }

    public function save(Request $request) {

      if ($request->input("title") == "")  {
        return redirect('post/add')->withInput()->with("errors","Oups !");


      } else {
        $b = new Post();
        $b->title = $request->input("title");
        $b->descr = $request->input("descr");
        $b->price = $request->input("price");
        $b->nbrooms = $request->input("nbrooms");
        $b->save();

        return redirect('posts');
      
      } 
    }

}
