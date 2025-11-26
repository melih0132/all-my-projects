var body = document.querySelector("body")
console.log(body)

//playlist
let titre = document.createElement("h1")
titre.textContent = "Playlist"
console.log(titre)

body.appendChild(titre)

var playlist = [
    {
      "groupe": "Deep Purple",
      "titre": "Smoke on the water",
      "année": 1972
    },
    {
      "groupe": "Metallica",
      "titre": "My friend of misery",
      "année": 1991
    },
    {
      "groupe": "Nirvana",
      "titre": "Something in the way",
      "année": 1991
    }
];

//tableau
let table = document.createElement("table")
let thead = document.createElement("thead")
let tbody = document.createElement("tbody")

function createTableRow(data) {
    let row = document.createElement("tr");
    data.forEach(text => {
        let cellule = document.createElement(data === headers ? "th" : "td")
        cellule.textContent = text
        row.appendChild(cellule)
    })
    return row
}

let headers = ["Groupe", "Titre", "Année"]
thead.appendChild(createTableRow(headers))

playlist.forEach(item => {
    let rowData = Object.values(item)
    tbody.appendChild(createTableRow(rowData))
})

table.appendChild(thead)
table.appendChild(tbody)
body.appendChild(table)

//formulaire ajout
let inputGrp = document.createElement("input")
inputGrp.placeholder = "Groupe"
let inputTitre = document.createElement("input")
inputTitre.placeholder = "Titre"
let inputAnnee = document.createElement("input")
inputAnnee.placeholder = "Année"
let inputBtn = document.createElement("button")
inputBtn.textContent = "Ajouter"

body.appendChild(inputGrp)
body.appendChild(inputTitre)
body.appendChild(inputAnnee)
body.appendChild(inputBtn)

console.log(inputBtn)

inputBtn.addEventListener("click", () => {
    let nouveau = {
        "groupe": inputGrp.value,
        "titre": inputTitre.value,
        "année": parseInt(inputAnnee.value)
    }

    playlist.push(nouveau)
    tbody.appendChild(createTableRow(Object.values(nouveau)))

    inputGrp.value = ""
    inputTitre.value = ""
    inputAnnee.value = ""
})