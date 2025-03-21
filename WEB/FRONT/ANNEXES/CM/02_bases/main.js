

// Variables : let, var, const

// let : variable locale -> à privilégier
// var : variable globale
// const : constante -> au max

// Tableau

const games = ["SC2", "LoL", "Tiny glades"]
console.log(games)
console.log(games[0])
games.push("Terra Nil")
console.log(games)

// 5 boucles

let i=0
while (i < games.length) {
	// do something
	i++
}

for(let i=0; i<games.length; i++) {
	// do something
}

// foreach

// IN : parcours des index. i=0,1,2
for(let i in games) {
	// do something
}

// OF : parcours des valeurs. games=SC2,LoL,TG
for(let game of games) {
	// do something
}

games.forEach(function(game) {
	// do something	
})
games.forEach(game => {
	// do something	
})


//-- Fonctions

function next(x) {
	return x+1
}

const next = x => x+1

const add = (x,y) => x+y

const random = _ => 42

const hop = _ => {
	console.log("HOP")
}





// defer : charger en dernier












