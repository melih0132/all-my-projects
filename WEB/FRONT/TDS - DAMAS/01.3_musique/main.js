
const musics = [
	{
		band: "Deep Purple",
		title: "Smoke on the water",
		year: 1972
	},
	{
		band: "Metallica",
		title: "My friend of misery",
		year: 1991
	},
	{
		band: "Nirvana",
		title: "Something in the way",
		year: 1991
	}
]


const body = document.querySelector("body")

// tag : nom du tag (string)
// container : élément DOM
// text : contenu (string)
function create(tag, container, text = null) {
	let element = document.createElement(tag)
	if (text) {
		element.innerText = text
		// element.appendChild(document.createTextNode(text))
	}
	container.appendChild(element)
	return element
}

create("h1", body, "Musique")

for (let music of musics) {

	let article = create("article", body)
	create("h2", article, music.band)
	create("p", article, music.title)
	create("p", article, music.year)

}
