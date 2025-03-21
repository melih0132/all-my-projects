<?php

use Illuminate\Support\Facades\Route;
use App\Http\Controllers\PostController;
use App\Http\Controllers\SiteController;

Route::get('/', [SiteController::class, "index" ]);

Route::get("/posts",[PostController::class, "index" ]);
Route::get("/post/{id}",[PostController::class, "one" ]);

Route::get("/post/add",[PostController::class, "addForm" ]);

Route::post("/post/save",[PostController::class, "save" ]);

