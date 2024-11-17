//Ex 1
// • Modifiez la couleur du titre de la page
let titre = document.querySelector('h1')
titre.style.color = "blue"

// • Modifiez le texte du titre de la page
titre.textContent = "Bleu"

// • Modifiez le style des toutes les span de classe « orange »
let spanOrange = document.querySelectorAll('span.orange')
spanOrange.forEach(span => span.style.fontWeight = 'bold')

// • Changez la couleur du fond (main) toutes les 2 secondes de manière aléatoire
setInterval(() => {
    document.querySelector('main').style.backgroundColor = `#${Math.floor(Math.random()*16777215).toString(16)}`;
}, 2000)

// • Changez la couleur des span de class « orange » toutes les 1 seconde
setInterval(() => {
    spanOrange.forEach(span => {
        span.style.color = `#${Math.floor(Math.random()*16777215).toString(16)}`;
    })
}, 1000)

// • Dans le tableau des couleurs, faites en sorte que la couleur soit en fond de la dernière case. Suggestion : récupération et réutilisation de la première case avec innerText
let rows = document.querySelectorAll('table tr')

rows.forEach(row => {
    let case1 = row.querySelector('td:first-child')
    let case2 = row.querySelector('td:last-child')
    
    if (case1 && case2) {
        const color = case1.innerText.trim()
        case2.style.backgroundColor = color
    }
})

// • Supprimez la ligne « purple » qui n’a rien à faire là !
let purpleRow = [...document.querySelectorAll('table tr')].find(row => 
    row.textContent.includes('Purple')
)

if (purpleRow) 
    purpleRow.remove()

// • L’article ne contient qu’une image. Faites en sorte qu’elle soit remplacée toutes les 3 secondes par une nouvelle image, de manière cyclique (voir la liste des images dans le dossier « Images »)
const images = ['abstract.jpg', 'beer.jpg', 'chair.jpg', 'fruit.jpg', 'pen.jpg', 'redhead.jpg', 'stairs.jpg', 'van.jpg']
let index = 0

setInterval(() => {
    const imgElement = document.querySelector('#img img')
    if (imgElement) {
        console.log(`images/${images[index]}`)
        imgElement.src = `images/${images[index]}`
        index = (index + 1) % images.length
    } else {
        console.error("L'élément <img> à l'intérieur de l'article avec l'ID 'img' n'existe pas !");
    }
}, 3000);

// • Modifiez le titre de l’article « image » → « Images »
let titre2 = document.querySelector('#img h2')
titre2.textContent = "Images"

// • Le menu (en haut à droite) doit pouvoir être caché/montré quand on clique dessus. à vous de choisir ce que veulent dire « caché » et « montré » !
let menu = document.querySelector('nav')
menu.addEventListener('click', () => {
    menu.classList.toggle('visible')
    if (menu.classList.contains('visible')) {
        console.log("Le menu est maintenant montré.")
    } else {
        console.log("Le menu est maintenant caché.")
    }
})

// • Lâchez vous !! Il faut que ça pique les yeux !