function create(tag, container, text = null) {
	let element = document.createElement(tag)
	if (text)
		element.innerText = text
	container.appendChild(element)
	return element
}

const body = document.querySelector("body")

document.querySelectorAll(".lightbox").forEach(function (image) {

	image.addEventListener("click", function () {
		let bg = create("div", body)
		bg.id = "bg"

		let box = create("div", bg)
		box.id = "box"

		let newImage = create("img", box)
		newImage.src = image.src

		let closeButton = create("div", box, "X")
		closeButton.id = "close"
		box.addEventListener("click", function (event) {
			event.stopPropagation()
		})

		function remove() {
			box.classList.add("out")
			setTimeout(function () {
				bg.remove()
			}, 800)
		}

		closeButton.addEventListener("click", function () {
			remove()
		})
		bg.addEventListener("click", function (event) {
			remove()
		})
		body.addEventListener("keyup", function (event) {
			if (event.key == "Escape")
				remove()
		})
	})

})