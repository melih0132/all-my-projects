var canvas = document.createElement("canvas")
canvas.width = 800
canvas.height = 600
console.log(canvas)
document.body.appendChild(canvas)

const context = canvas.getContext("2d")

//3 boules
const boules = [
    { x: 200, y: 200, vx: 2, vy: 6, r: 30, color: "red" },
    { x: 400, y: 300, vx: 4, vy: 3, r: 30, color: "blue" },
    { x: 600, y: 400, vx: 6, vy: 8, r: 30, color: "white" }
]

//enorme pif
const friction = 0.9

function dessinerBoules() {
    boules.forEach(boule => {
        context.beginPath()
        context.arc(boule.x, boule.y, boule.r, 0, Math.PI * 2)
        context.fillStyle = boule.color
        context.fill()
    })
}

function miseAJourPosition() {
    boules.forEach(boule => {
        boule.x += boule.vx
        boule.y += boule.vy

        if (boule.x + boule.r > canvas.width || boule.x - boule.r < 0) {
            boule.vx = -boule.vx * friction
        }
        if (boule.y + boule.r > canvas.height || boule.y - boule.r < 0) {
            boule.vy = -boule.vy * friction
        }
    })
}

function colisionBoules() {
    for (let i = 0; i < boules.length; i++) {
        for (let j = i + 1; j < boules.length; j++) {
            const boule1 = boules[i];
            const boule2 = boules[j];
            const dx = boule1.x - boule2.x;
            const dy = boule1.y - boule2.y;
            const distance = Math.sqrt(dx * dx + dy * dy);
    
            if (distance < boule1.r + boule2.r) {
                const tempVx = boule1.vx;
                const tempVy = boule1.vy;
                boule1.vx = boule2.vx;
                boule1.vy = boule2.vy;
                boule2.vx = tempVx;
                boule2.vy = tempVy;
            }
        }
    }
}

function boucle() {
    context.clearRect(0, 0, canvas.width, canvas.height);
    dessinerBoules();
    miseAJourPosition();
    colisionBoules();
}

setInterval(boucle, 10);

canvas.addEventListener("click", (event) => {
    const rect = canvas.getBoundingClientRect()
    const x = event.clientX - rect.left
    const y = event.clientY - rect.top

    boules.forEach(boule => {
        const dx = x - boule.x
        const dy = y - boule.y
        const distance = Math.sqrt(dx * dx + dy * dy)

        if (distance < boule.r) {
            const angle = Math.atan2(dy, dx)
            boule.vx = Math.cos(angle) * 2
            boule.vy = Math.sin(angle) * 2
        }
    })
})