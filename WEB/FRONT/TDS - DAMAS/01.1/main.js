

const h1 = document.querySelector("header h1")
console.log(h1)
h1.style.color = "orange"
// h1.innerText = "Orange, <i>c'est beau</i>"
h1.innerHTML = "Orange, <i>c'est beau</i>"



const spans = document.querySelectorAll("span.orange")
for(let span of spans) {
	span.style.color = "magenta"
	span.style.fontWeight = "bold"
}




const main = document.querySelector("main")

setInterval(function() {

	let r = Math.floor(Math.random() * 200)  // MAX 255
	let g = Math.floor(Math.random() * 100)
	let b = Math.floor(Math.random() * 0)

	let color = "rgb("+r+","+g+","+b+")"

	main.style.backgroundColor = color

}, 1000)



const trs = document.querySelectorAll("#examples tr")
for(let tr of trs) {

	let color = tr.querySelector(".hexa").innerText
	tr.querySelector(".visu").style.backgroundColor = color

}

trs[8].remove()



const images = ["abstract.jpg","beer.jpg","chair.jpg","fruit.jpg","pen.jpg","redhead.jpg","stairs.jpg","van.jpg",]

const image = document.querySelector("#img img")

let i = 0
setInterval(function() {
	image.src = "./images/"+images[i]
	i++
	if (i>=images.length)
		i = 0
}, 300)


// Ajouter le "s" à images car il y en a plusieurs
document.querySelector("#img h2").innerText += "s"


const menu = document.querySelector("header nav")
menu.addEventListener("click", function() {
	menu.classList.toggle("visible")
})

