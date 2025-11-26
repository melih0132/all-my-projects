function afficherResultat(score, nbMotsProposes) {
    let spanScore = document.querySelector(".zoneScore span");
    let affichageScore = `${score} / ${nbMotsProposes}`;
    spanScore.innerText = affichageScore;
}

function afficherProposition(proposition) {
    let zoneProposition = document.querySelector(".zoneProposition");
    zoneProposition.innerText = proposition;
}

function afficherEmail(nom, email, score) {
    let mailto = `mailto:${email}?subject=Partage du score Azertype&body=Wesh téma, chui ${nom}, j'viens d'avoir ${score} sur le site Azertype !`;
    location.href = mailto;
}

function validerNom(nom) {
    if (nom.length < 2) {
        throw new Error("Le nom est trop court.");
    }
}

function validerEmail(email) {
    let emailRegExp = new RegExp("[a-z0-9._-]+@[a-z0-9._-]+\\.[a-z0-9._-]+");
    if (!emailRegExp.test(email)) {
        throw new Error("L'email n'est pas valide.");
    }
}

function afficherMessageErreur(message) {
    let spanErreurMessage = document.getElementById("erreurMessage");
    if (!spanErreurMessage) {
        let popup = document.querySelector(".popup");
        spanErreurMessage = document.createElement("span");
        spanErreurMessage.id = "erreurMessage";
        popup.append(spanErreurMessage);
    }
    spanErreurMessage.innerText = message;
}

function gererFormulaire(scoreEmail) {
    try {
        let baliseNom = document.getElementById("nom");
        let nom = baliseNom.value;
        validerNom(nom);

        let baliseEmail = document.getElementById("email");
        let email = baliseEmail.value;
        validerEmail(email);
        afficherMessageErreur("");
        afficherEmail(nom, email, scoreEmail);

    } catch(erreur) {
        afficherMessageErreur(erreur.message);
    }
}

function initAddEventListenerPopup() {
    let btnPartage = document.querySelector(".zonePartage button");
    let btnAnnuler = document.getElementById("btnAnnuler");
    let popupBackground = document.querySelector(".popupBackground");

    btnPartage.addEventListener("click", () => {
        let popupBackground = document.querySelector(".popupBackground");
        popupBackground.classList.add("active");
    });

    popupBackground.addEventListener("click", (event) => {
        if (event.target === popupBackground) {
            popupBackground.classList.remove("active");
        }
    });

    btnAnnuler.addEventListener("click", (event) => {
        event.preventDefault();
        popupBackground.classList.remove("active");
    });
}

function lancerJeu() {
    initAddEventListenerPopup();
    let score = 0;
    let i = 0;
    let listeProposition = listeMots;

    let btnValiderMot = document.getElementById("btnValiderMot");
    let inputEcriture = document.getElementById("inputEcriture");

    afficherProposition(listeProposition[i]);

    btnValiderMot.addEventListener("click", validerProposition);
    inputEcriture.addEventListener("keypress", function(event) {
        if (event.keyCode === 13) {
            event.preventDefault();
            validerProposition();
        }
    });

    let listeBtnRadio = document.querySelectorAll(".optionSource input");
    listeBtnRadio.forEach(btnRadio => {
        btnRadio.addEventListener("change", (event) => {
            listeProposition = event.target.value === "1" ? listeMots : listePhrases;
            afficherProposition(listeProposition[i]);
        });
    });

    let form = document.querySelector("form");
    form.addEventListener("submit", (event) => {
        event.preventDefault();
        let scoreEmail = `${score} / ${i}`;
        gererFormulaire(scoreEmail);
    });

    afficherResultat(score, i);

    function validerProposition() {
        if (inputEcriture.value === listeProposition[i]) {
            score++;
        }
        i++;
        afficherResultat(score, i);
        inputEcriture.value = '';
        if (listeProposition[i] === undefined) {
            afficherProposition("Le jeu est fini");
            btnValiderMot.disabled = true;
        } else {
            afficherProposition(listeProposition[i]);
        }
    }
}