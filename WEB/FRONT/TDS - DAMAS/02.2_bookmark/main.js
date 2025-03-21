function create(tag, container, text = null) {
	let element = document.createElement(tag)
	if (text)
		element.innerText = text
	container.appendChild(element)
	return element
}

const links = [
	{
		"title": "USMB",
		"url": "https://univ-smb.fr/",
		"category": "taf"
	},
	{
		"title": "Useless Web",
		"url": "https://theuselessweb.com/",
		"category": "wtf"
	}
]


const table = document.querySelector("table#bookmark")

links.forEach(link => {

	let tr = create("tr", table)
	create("td", tr, link.title)
	let linkTD = create("td", tr)
	let anchor = create("a", linkTD, link.url)
	anchor.href = link.url

})

