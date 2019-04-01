/**
 * Player represents each of your opponents and how many cards they have
 */
class Player {
    constructor(name, nCards) {
        this.name = name;
        this.nCards = nCards;
    }
}

/**
 * Main game loop, updates the screen constantly.
 * @param timestamp current timestamp to calculate how much time has passed
 */
function gameLoop(timestamp) {
    let dt = timestamp-lastTime;
    lastTime = timestamp;

    ctx.clearRect(0,0,canvas.width,canvas.height);

    requestAnimationFrame(gameLoop);
}



/*




        *****  Setup code below  *****



 */

let mousePosition = {
    x:0,y:0
}
let mousePressed = false;
let players = [];
let currentPlayer = 0;
let direction = 'Right';
let lastTime = 0;


//Canvas load
let canvas = document.getElementById('canvas');
let ctx = canvas.getContext('2d');

//Listeners
canvas.addEventListener('mousedown', (event) => {
    if(event.button==0) {
        mousePressed = true;
    }
});
//update mouse pos
canvas.addEventListener('mousemove',(event) => {
    mousePosition.x = event.offsetX;
    mousePosition.y = event.offsetY;
});
canvas.addEventListener('mouseup', (event) => {
    if(event.button==0) {
        mousePressed = false;
    }
});

//TEST CODE - ASSUME THE SERVER SENDS YOU THIS PLAYER INFO
players.push([new Player("me",10), new Player("daddy",10), new Player("Mummy",10)]);

//This is your player id - so you know who is next
let id = 0;

//run gameloop
gameLoop(0);
