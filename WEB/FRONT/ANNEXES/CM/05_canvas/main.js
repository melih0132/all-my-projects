


const canvas = document.querySelector("canvas")
const w = window.innerWidth
const h = window.innerHeight
canvas.width = w
canvas.height = h


const c = canvas.getContext("2d")


// c.beginPath()
// c.moveTo(200,300)
// c.lineTo(500,700)
// c.lineTo(1000,100)
// c.stroke()

// c.beginPath()
// c.fillStyle = "orange"
// c.arc(100,200,50,0, Math.PI*2)
// c.fill()

const inter = { r: 200, a: 0 }
const ball = { r: 100, a: 0 }

setInterval(function() {
	c.clearRect(0,0,w,h)

	let xi = w/2 + inter.r*Math.cos(inter.a)
	let yi = h/2 + inter.r*Math.sin(inter.a)

	let xb = xi + ball.r*Math.cos(ball.a)
	let yb = yi + ball.r*Math.sin(ball.a)

	// c.beginPath()
	// c.moveTo(w/2,h/2)
	// c.lineTo(xi,yi)
	// c.lineTo(xb,yb)
	// c.stroke()

	c.beginPath()
	c.fillStyle = "orange"
	c.arc(xb,yb,20,0, Math.PI*2)
	c.fill()

	inter.a += Math.PI/180
	ball.a -= Math.PI/300

}, 1)

