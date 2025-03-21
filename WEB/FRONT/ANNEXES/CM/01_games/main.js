
// debug
console.log("HOP")

// Accès DOM lecture
// DOM = Document Object Model&

const h1 = document.querySelector("h1")
h1.style.backgroundColor = "purple"
h1.innerText = "Quelques jeux vidéo"

const games = document.querySelectorAll("li")
games[1].remove()
games[2].style.fontWeight = "bold"
// console.log(games)


// Accès DOM en écriture
const ul = document.querySelector("ul")
const li = document.createElement("li")
li.innerText = "Tiny glades"
ul.appendChild(li)

