

const games = [
	{
		name: "Terra Nil",
		categories: "Stratégie, Chill",
		note: 7
	},
	{
		name: "Tiny Glades",
		categories: "Construction, Chill",
		note: 10
	},
	{
		name: "Space Marine",
		categories: "Combat",
		note: 6
	}
]


const body = document.querySelector("body")

const h1 = document.createElement("h1")
h1.innerText = "Jeux vidéo"
body.appendChild(h1)


const gamesTable = document.createElement("table")
body.appendChild(gamesTable)

for(let game of games) {

	let tr = document.createElement("tr")
	gamesTable.appendChild(tr)

	let td = document.createElement("td")
	td.innerText = game.name
	tr.appendChild(td)

	td = document.createElement("td")
	td.innerText = game.categories
	tr.appendChild(td)

	td = document.createElement("td")
	td.innerText = game.note
	tr.appendChild(td)

}
