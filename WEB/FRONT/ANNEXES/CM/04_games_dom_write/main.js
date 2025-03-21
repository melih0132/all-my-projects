

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


function create(tag, container, text) {
	let element = document.createElement(tag)
	element.innerText = text
	container.appendChild(element)
	return element
}

const body = document.querySelector("body")

const h1 = create("h1", body, "Jeux vidéo")

const gamesTable = create("table",body,"")

for(let game of games) {

	let tr = create("tr",gamesTable, "")

	create("td", tr, game.name)
	create("td", tr, game.categories)
	create("td", tr, game.note)

}
