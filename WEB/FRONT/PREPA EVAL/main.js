// Sélection d'un élément avec querySelector
const titre = document.querySelector("h1");
titre.innerText = "Titre changé avec querySelector";

// Sélection d'un élément par son ID avec getElementById
const bouton = document.getElementById("monBouton");
bouton.innerText = "Clique-moi pour ajouter du texte";

// Ajout d'un événement au clic avec addEventListener
bouton.addEventListener("click", function() {
    // Modifier le contenu d'un élément avec innerHTML
    const divContenu = document.getElementById("contenu");
    divContenu.innerHTML = "<p>Nouveau contenu ajouté avec innerHTML après un clic !</p>";
});

// Sélection d'un élément par sa classe avec querySelectorAll et ajout d'une classe CSS
const paragraphes = document.querySelectorAll(".texte");
paragraphes.forEach(paragraphe => {
    paragraphe.classList.add("nouvelle-classe");  // Ajouter une classe CSS
});

// Créer et ajouter dynamiquement un nouvel élément dans le DOM
const nouveauParagraphe = document.createElement("p");
nouveauParagraphe.innerText = "Paragraphe ajouté avec appendChild";
document.body.appendChild(nouveauParagraphe);

// Utilisation de setTimeout pour exécuter du code après un délai
setTimeout(function() {
    titre.innerText = "Changement de titre après 3 secondes";
}, 3000);

// Utilisation de setInterval pour exécuter du code à intervalles réguliers
let compteur = 0;
const intervalID = setInterval(function() {
    compteur++;
    console.log("Intervalle de 2 secondes. Compteur: " + compteur);
    
    // Arrêter l'intervalle après 5 itérations
    if (compteur >= 5) {
        clearInterval(intervalID);
        console.log("Intervalle arrêté.");
    }
}, 2000);

// Gestion du survol avec addEventListener (mouseenter et mouseleave)
const elementSurvole = document.getElementById("monElement");
elementSurvole.addEventListener("mouseenter", function() {
    elementSurvole.style.backgroundColor = "lightgreen";
    elementSurvole.innerText = "Tu me survoles !";
});

elementSurvole.addEventListener("mouseleave", function() {
    elementSurvole.style.backgroundColor = "";
    elementSurvole.innerText = "Survole-moi";
});

// Fonction personnalisée avec des paramètres
function changerCouleur(element, couleur) {
    element.style.color = couleur;
}

// Changer la couleur d'un élément au clic
document.getElementById("changerCouleur").addEventListener("click", function() {
    changerCouleur(titre, "red");
});

// Utilisation d'un tableau et d'une boucle forEach
const fruits = ["Pomme", "Banane", "Orange"];
fruits.forEach(fruit => {
    console.log("Fruit: " + fruit);  // Afficher chaque fruit dans la console
});

// Manipulation d'attributs HTML
const image = document.createElement("img");
image.src = "https://via.placeholder.com/150";
image.alt = "Image de test";
document.body.appendChild(image);

// Accès aux attributs d'un élément
console.log(image.src);  // Affiche l'URL de l'image
console.log(image.alt);  // Affiche le texte alternatif de l'image

// Formulaire et gestion des entrées utilisateur
const formulaire = document.createElement("form");
const inputNom = document.createElement("input");
inputNom.type = "text";
inputNom.placeholder = "Votre nom";
const boutonSubmit = document.createElement("button");
boutonSubmit.innerText = "Soumettre";
formulaire.appendChild(inputNom);
formulaire.appendChild(boutonSubmit);
document.body.appendChild(formulaire);

formulaire.addEventListener("submit", function(event) {
    event.preventDefault();  // Empêche l'envoi du formulaire
    alert("Nom soumis : " + inputNom.value);  // Affiche la valeur du champ de texte
});

// Suppression d'un élément du DOM
document.getElementById("supprimerParagraphe").addEventListener("click", function() {
    const dernierParagraphe = document.querySelector("p:last-child");
    if (dernierParagraphe) {
        dernierParagraphe.remove();
        console.log("Dernier paragraphe supprimé");
    }
});