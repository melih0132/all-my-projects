

const body = document.querySelector("body")
const scoreDiv = document.querySelector("#score")

let score = 0


setInterval(function () {

	let div = document.createElement("div")
	body.appendChild(div)

	div.classList.add("bubble")
	div.style.top = (Math.random() * window.innerHeight) + "px"
	div.style.left = (Math.random() * window.innerWidth) + "px"
	let diameter = Math.random() * 50 + 50
	div.style.width = diameter + "px"
	div.style.height = diameter + "px"
	div.style.backgroundColor =
		'#' + (Math.floor(Math.random() * 0xFFFFFF)).toString(16)


	let plop = document.createElement("audio")
	plop.src = "plop.wav"
	plop.addEventListener("canplaythrough", function () { plop.play() })


	div.addEventListener("mouseenter", function () {
		div.classList.add("inflate")
	})
	div.addEventListener("mouseleave", function () {
		div.classList.remove("inflate")
	})
	div.addEventListener("click", function (event) {
		event.stopPropagation()
		div.remove()

		score++
		scoreDiv.innerText = score + " points"
		scoreDiv.style.fontSize = (15 + score * 2) + "px"

		let pan = document.createElement("audio")
		pan.src = "pan.flac"
		pan.addEventListener("canplaythrough", function () { pan.play() })
	})


}, 1000)





