

const body = document.querySelector("body")

body.addEventListener("click", event => {
	let div = document.createElement("div")
	div.style.top = event.pageY + "px"
	div.style.left = event.pageX + "px"
	div.textContent = Math.floor(Math.random() * 20)
	body.appendChild(div)
})