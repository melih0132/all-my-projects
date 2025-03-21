

const button = document.querySelector("#hopButton")

let angle = 0

button.addEventListener("click", function() {
	button.style.top = 
		(Math.random()*window.innerHeight)+"px"
	button.style.left = 
		(Math.random()*window.innerWidth)+"px"

	angle = Math.random()*360
	button.style.transform = "rotate("+angle+"deg)"
})

const ballDiv = document.querySelector("#ball")

const ball = {
	x: 0,
	y: 0,
	vx: 1,
	vy: 0
}

setInterval(function() {
	ballDiv.style.top = ball.y+"px"
	ballDiv.style.left = ball.x+"px"

	ball.x += ball.vx
	ball.y += ball.vy

	ball.vy += 0.01
	if (ball.y+100 > window.innerHeight) {
		ball.y -= ball.vy
		ball.vy *= -1
	}
	if (ball.x < 0 || ball.x+100 > window.innerWidth) {
		ball.x -= ball.vx
		ball.vx *= -1
	}

}, 1)



