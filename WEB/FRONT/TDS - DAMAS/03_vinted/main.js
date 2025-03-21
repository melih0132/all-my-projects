
function create(tag, container, text = null) {
	let element = document.createElement(tag)
	if (text)
		element.innerText = text
	container.appendChild(element)
	return element
}

let categories
let colors

function display(shoe) {
	let article = create("article", shoesContainer)

	let brandP = create("p", article, shoe.brand)
	brandP.classList.add("brand")

	let descrP = create("p", article, shoe.descr)
	descrP.classList.add("descr")

	let sizeP = create("p", article, shoe.size)
	sizeP.classList.add("size")

	let priceP = create("p", article, shoe.price + "€")
	priceP.classList.add("price")

	let sellerP = create("p", article, shoe.seller)
	sellerP.classList.add("seller")

	let categoryP = create("p", article, categories[shoe.category].name)
	categoryP.classList.add("category")

	article.style.backgroundColor = "#" + colors[shoe.color].hex
}


const shoesContainer = document.querySelector("#shoes")

axios.get("http://51.83.36.122:8080/categories").then(responseCategories => {
	categories = responseCategories.data

	let categoriesSelect = document.querySelector("#form select[name=category]")
	categories.forEach(category => {
		let option = create("option", categoriesSelect, category.name)
		option.value = category.id
	})

	axios.get("http://51.83.36.122:8080/colors").then(responseColors => {
		colors = responseColors.data

		let colorsSelect = document.querySelector("#form select[name=color]")
		colors.forEach(color => {
			let option = create("option", colorsSelect, color.name)
			option.value = color.id
		})

		axios.get("http://51.83.36.122:8080/shoes").then(responseShoes => {
			responseShoes.data.forEach(display)
		})
	})
})



const addForm = document.querySelector("#form")

addForm.querySelector("button").addEventListener("click", event => {

	let brand = addForm.querySelector("input[name=brand]").value
	let descr = addForm.querySelector("input[name=descr]").value
	let seller = addForm.querySelector("input[name=seller]").value
	let price = addForm.querySelector("input[name=price]").value
	let category = addForm.querySelector("select[name=category]").value
	let color = addForm.querySelector("select[name=color]").value
	let size = addForm.querySelector("input[name=size]").value

	axios.post("http://51.83.36.122:8080/add", {
		brand: brand,
		descr: descr,
		seller: seller,
		price: price,
		category: category,
		color: color,
		size: size
	}).then(response => {
		if (!response.data.errors)
			display(response.data)
		else
			console.log(response.data.errors)
	})


})


