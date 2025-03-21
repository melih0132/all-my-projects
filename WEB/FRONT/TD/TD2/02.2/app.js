const h1 = document.createElement("h1");
h1.textContent = "Mes Bookmarks";
document.body.appendChild(h1);

const form = document.createElement("form");
form.id = "bookmarkForm";

const titleInput = document.createElement("input");
titleInput.type = "text";
titleInput.id = "title";
titleInput.placeholder = "Titre du site";
titleInput.required = true;
form.appendChild(titleInput);

const urlInput = document.createElement("input");
urlInput.type = "url";
urlInput.id = "url";
urlInput.placeholder = "URL du site";
urlInput.required = true;
form.appendChild(urlInput);

const categoryInput = document.createElement("input");
categoryInput.type = "text";
categoryInput.id = "category";
categoryInput.placeholder = "Catégorie";
categoryInput.required = true;
form.appendChild(categoryInput);

const submitButton = document.createElement("button");
submitButton.type = "submit";
submitButton.textContent = "Ajouter";
form.appendChild(submitButton);

document.body.appendChild(form);

const filterInput = document.createElement("input");
filterInput.type = "text";
filterInput.id = "filter";
filterInput.placeholder = "Filtrer par catégorie";
document.body.appendChild(filterInput);

const h2 = document.createElement("h2");
h2.textContent = "Liste des bookmarks";
document.body.appendChild(h2);

const bookmarkList = document.createElement("ul");
bookmarkList.id = "bookmarkList";
document.body.appendChild(bookmarkList);

const bookmarks = [
    {
        title: "USMB",
        url: "https://univ-smb.fr/",
        category: "taf"
    },
    {
        title: "Useless Web",
        url: "https://theuselessweb.com/",
        category: "wtf"
    }
];

console.table(bookmarks)

//affichage
function displayBookmarks(list) {
    bookmarkList.innerHTML = "";

    list.forEach((bookmark, index) => {
        const li = document.createElement("li");
        li.classList.add("bookmark-item");
        li.innerHTML = `
      <a href="${bookmark.url}" target="_blank">${bookmark.title}</a>
      (${bookmark.category})
      <button onclick="deleteBookmark(${index})">Supprimer</button>
      <button onclick="editBookmark(${index})">Modifier</button>
    `; //cela permet le fait que ce soit cliquable
        bookmarkList.appendChild(li);
    });
}

displayBookmarks(bookmarks);

//ajout
function addBookmark(favoris) {
    favoris.preventDefault(); //hehehe pas faille avec moi

    const title = titleInput.value;
    const url = urlInput.value;
    const category = categoryInput.value;

    const newBookmark = { title, url, category };
    bookmarks.push(newBookmark);
    displayBookmarks(bookmarks);

    //reset le forumlaire
    form.reset();
}

//supp
function deleteBookmark(index) {
    bookmarks.splice(index, 1);

    /** fonction splice
     * Supprime des éléments d'un tableau et, si nécessaire, insère de nouveaux éléments à leur place, en renvoyant les éléments supprimés.
     * @param start L'emplacement à zéro dans le tableau à partir duquel les éléments doivent être supprimés.
     * @param deleteCount Nombre d'éléments à supprimer.
     * @param items Éléments à insérer dans le tableau à la place des éléments supprimés.
     * @returns Un tableau contenant les éléments qui ont été supprimés.
     */

    displayBookmarks(bookmarks);
}

//modif
function editBookmark(index) {
    const bookmark = bookmarks[index];
    titleInput.value = bookmark.title;
    urlInput.value = bookmark.url;
    categoryInput.value = bookmark.category;

    form.onsubmit = function (favoris) {
        favoris.preventDefault();
        bookmarks[index] = {
            title: titleInput.value,
            url: urlInput.value,
            category: categoryInput.value
        };
        displayBookmarks(bookmarks);
        form.reset();
        form.onsubmit = addBookmark;
    };
}

form.onsubmit = addBookmark;

//filtre
filterInput.addEventListener("input", () => {
    const filterValue = filterInput.value.toLowerCase();
    const filteredBookmarks = bookmarks.filter(bookmark =>
        bookmark.category.toLowerCase().includes(filterValue)
    );//merci python
    displayBookmarks(filteredBookmarks);//raffichage hehehe
});