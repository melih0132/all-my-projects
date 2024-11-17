function afficherPopup() {
    let popupBackground = document.querySelector(".popupBackground");
    popupBackground.classList.add("active");
}

function cacherPopup() {
    let popupBackground = document.querySelector(".popupBackground");
    popupBackground.classList.remove("active");
}

function initAddEventListenerPopup() {
    // Sélectionner le bouton "Partager" dans la zonePartage
    let btnPartage = document.querySelector(".zonePartage button");
    let btnAnnuler = document.getElementById("btnAnnuler");
    let popupBackground = document.querySelector(".popupBackground");

    btnPartage.addEventListener("click", afficherPopup);

    popupBackground.addEventListener("click", (event) => {
        if (event.target === popupBackground) {
            cacherPopup();
        }
    });

    btnAnnuler.addEventListener("click", (event) => {
        event.preventDefault(); // Empêcher le comportement par défaut pour un bouton de type "cancel"
        cacherPopup();
    });
}

// Ajouter les écouteurs d'événements après que le DOM soit chargé
document.addEventListener("DOMContentLoaded", initAddEventListenerPopup);