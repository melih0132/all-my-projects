

const canvas = document.querySelector("canvas")

const w = window.innerWidth
const h = window.innerHeight
canvas.width = w
canvas.height = h
const c = canvas.getContext("2d")

const balls = []

for (let i = 0; i < 10; i++) {
	balls.push({
		x: 20 + Math.random() * (w - 40),
		y: 20 + Math.random() * (h - 40),
		r: 10 + Math.random() * 10,
		vx: Math.random() * 6 - 3,
		vy: Math.random() * 6 - 3,
	})
}


const points = []

document.querySelector("body").addEventListener("mousemove", function (event) {
	points.push({ x: event.pageX, y: event.pageY })
})



setInterval(function () {
	c.clearRect(0, 0, w, h)

	c.beginPath()
	c.moveTo(points[0].x, points[0].y)
	for (let point of points)
		c.lineTo(point.x, point.y)
	c.strokeStyle = "black"
	c.lineWidth = 2
	c.stroke()




	for (let ball of balls) {
		c.beginPath()
		c.arc(ball.x, ball.y, ball.r, 0, Math.PI * 2)
		c.fillStyle = "orange"
		c.strokeStyle = "indigo"
		c.lineWidth = 10
		c.fill()
		// c.stroke()

		ball.vy += 0.06 // Gravité
		ball.x += ball.vx
		ball.y += ball.vy

		if (ball.x - ball.r <= 0 || ball.x + ball.r > w) {
			ball.x -= ball.vx
			ball.vx *= -0.9 // Amorti
		}
		if (ball.y - ball.r <= 0 || ball.y + ball.r > h) {
			ball.y -= ball.vy
			ball.vy *= -0.9 // Amorti
		}
	}


}, 1)




