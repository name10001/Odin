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
 * Draws the cards in your hand
 */
function drawCards() {
    let player = players[id];
    let beginOffset = (CARD_WIDTH + 20)*player.nCards/2-10;
    let offset = CARD_WIDTH + 20;
    for(let i = 0; i<player.nCards;i++) {
        ctx.drawImage(testImage,canvas.width/2-beginOffset+i*offset,canvas.height-50-CARD_HEIGHT,CARD_WIDTH,CARD_HEIGHT);
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

    ctx.fillStyle = "#222";
    ctx.globalAlpha = 0.6;
    ctx.fillRect(0,0,canvas.width,canvas.height);
    ctx.globalAlpha = 1;

    drawCards();


    requestAnimationFrame(gameLoop);
}



/*




        *****  Setup code below  *****



 */

const CARD_WIDTH = 134;
const CARD_HEIGHT = 209;


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

canvas.width = window.innerWidth;
canvas.height = window.innerHeight;
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
//update size
window.addEventListener('resize',function() {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
},false);

//TEST CODE - ASSUME THE SERVER SENDS YOU THIS PLAYER INFO
players.push(new Player("me",10));

//This is your player id - so you know who is next
let id = 0;

let testImage = new Image;
testImage.src = '/static/cards/back.png';
testImage.addEventListener('load',function() {
    gameLoop(0);
},false);

