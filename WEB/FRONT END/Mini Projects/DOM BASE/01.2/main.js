var body = document.querySelector("body")
console.log(body)
var score = 0
var scoreTexte = document.createElement("h2")
scoreTexte.textContent = "Score: 0"
body.appendChild(scoreTexte)
console.log(scoreTexte)

setInterval(function() {
    var bulle = document.createElement("div")
    bulle.style.backgroundColor = `#${Math.floor(Math.random()*16777215).toString(16)}`

    bulle.classList.add('bulle')
    document.body.appendChild(bulle)

    bulle.style.top = Math.random() * (window.innerHeight - bulle.getBoundingClientRect().height) + "px"
    bulle.style.left = Math.random() * (window.innerWidth - bulle.getBoundingClientRect().width) + "px"

    bulle.addEventListener("click", function() {
        score += 1
        scoreTexte.textContent = ('Score: ' + score)

        bulle.remove()
    })
}, 1500)
