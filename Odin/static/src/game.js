$(document).ready(function() {
                /*

                SOCKET STUFF


                 */
                // SocketIO
                socket = io.connect(document.domain, {
                    'reconnection': true,
                    'reconnectionDelay': 500,
                    'maxReconnectionAttempts': Infinity
                });

                socket.on('connect', function () {
                    socket.emit("initial game connection", GAME_ID);
                    console.log('test');
                });

                socket.on('message for player', function (message) {
                    $("#message-from-server").html(message);
                    $('.modal').modal("show");

                });

                socket.on('card update', cardUpdate);
                socket.on('player update', playerUpdate);
});



/*




        VARIABLES



 */
const CARD_WIDTH = 134;
const CARD_HEIGHT = 209;


let mousePosition = {//mouse position
    x:0,y:0
}
let mouseMove = {//change in mouse position
    x:0,y:0
}
let mousePressed = false;//if the mouse is pressed

//DRAGGING - 0 = none, 1 = "click" or undetermined, 2 = scroll, 3 = move card
let dragType = 0;
let clickPosition = {
    x:0,y:0
}

//scrolling
let scrollOffset = -CARD_WIDTH/2;
let scrollSpeed = 0;

//time keeping
let lastTime = 0;


//canvas objects
let canvas, ctx, testImage;


//gameplay (from server)
let yourCards = [];
let id = 0;
let players = [];
let currentPlayer = 0;
let direction = 'Right';

/**
 * Player represents each of your opponents and how many cards they have
 */
class Player {
    constructor(name, nCards) {
        this.name = name;
        this.nCards = nCards;
    }
}

class Card {
    constructor(id, url, allowedToPlay) {
        this.id = id;
        this.allowedToPlay = allowedToPlay;
        this.image = new Image;
        this.image.src = url;
    }
}

/**
 * Function for updating your scroll speed through the list of cards
 */
function scroll(dt) {
    //accelerate based on your dragging speed
    if(scrollSpeed > 0) {
        scrollSpeed-=dt;
        if(scrollSpeed<0) scrollSpeed = 0;
    }
    else if(scrollSpeed < 0) {
        scrollSpeed+=dt;
        if(scrollSpeed>0) scrollSpeed = 0;
    }

    scrollOffset+=scrollSpeed;
    if(scrollOffset < -yourCards.length*(CARD_WIDTH+20)-canvas.width/4) {
        scrollOffset = -yourCards.length*(CARD_WIDTH+20)-canvas.width/4;
    }
    else if(scrollOffset > canvas.width/4+20) {
        scrollOffset = canvas.width/4+20;
    }

}

/**
 * Draws the cards in your hand
 */
function drawCards() {
    let offset = CARD_WIDTH + 20;
    for(let i = 0; i<yourCards.length;i++) {
        ctx.drawImage(yourCards[i].image,canvas.width/2+scrollOffset+i*offset,canvas.height-50-CARD_HEIGHT,CARD_WIDTH,CARD_HEIGHT);
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

    scroll(dt);
    drawCards();


    requestAnimationFrame(gameLoop);
}

function click(x,y) {
    mousePressed = true;
    mousePosition.x = x;
    mousePosition.y = y;
    if(mousePosition.y > canvas.height-100-CARD_HEIGHT) {
        //Clicked in card area
        clickPosition.x = mousePosition.x-scrollOffset;
        clickPosition.y = mousePosition.y;
        dragType = 1;
    }
}
function release() {
    if(dragType == 2) {
        scrollSpeed = mouseMove.x*20;
    }
    mousePressed = false;
    dragType = 0;
}
function drag() {
    if(dragType==2) {
        scrollOffset = mousePosition.x-clickPosition.x;
    }
    else if(dragType==3) {
        //TODO move the card around
    }
    //determine if you are dragging the mouse horizontally or vertically
    else {
        if(Math.abs(mousePosition.x-scrollOffset-clickPosition.x)>20) {

            dragType = 2;
        }
        else if(Math.abs(mousePosition.y-clickPosition.y)>20) {
            dragType = 3;
        }
    }
}

/*



            SOCKET FUNCTIONS



 */

/**
 * Is called when the server sends you a list of cards
 * @param cards
 */
function cardUpdate(cards) {
    yourCards.length = 0;
    for(let card of cards['your cards']) {
        yourCards.push(new Card(card['card id'],card['card image url'],card['can be played']));
    }
}

/**
 * Is called to update the player on how many cards each person now has
 * @param players
 */
function playerUpdate(players) {
    console.log("player update");
    console.log(players);
    // not currently working!
    // players example:
    // {
    //   "Players":
    //     [
    //       {
    //         "current turn": false,
    //         "number of cards": 15,
    //         "name": "Jeff"
    //       },
    //       {
    //         "current turn": true,
    //         "number of cards": 5,
    //         "name": "Bob"
    //       }
    //     ],
    //   "direction": "Left"
    // }
}


function playCard(cardId, picked_player, pick_type){
    // leave picked_player and pick_type as null unless needed
    // not currently working!
    socket.emit("play card", GAME_ID, cardId, picked_player, pick_type);
}

function sayUno(){
    socket.emit("game message", GAME_ID, "Uno");
}

function nextTurn(){
    // not currently working!
    socket.emit("game message", GAME_ID, "Next Turn");
}

/*




        MAIN FUNCTION




 */
$(document).ready(function() {
    // SocketIO
    socket = io.connect(document.domain, {'reconnection': true, 'reconnectionDelay': 500,'maxReconnectionAttempts':Infinity});
    socket.on('connect', function() {
        socket.emit("initial game connection", GAME_ID);
    });
    socket.on('message for player', function(message) {
        $("#message-from-server").html(message);
        $('.modal').modal("show");
    });
    function playCard(cardId, picked_player, pick_type){
        // leave picked_player and pick_type as null unless needed
        // not currently working!
        socket.emit("play card", GAME_ID, cardId, picked_player, pick_type);
    }
    function sayUno(){
        socket.emit("game message", GAME_ID, "Uno");
    }
    function nextTurn(){
        // not currently working!
        socket.emit("game message", GAME_ID, "Next Turn");
    }
    socket.on('card update', cardUpdate);
    socket.on('player update', playerUpdate);


    /*



    UI STUFF



     */

    //Canvas load
    canvas = document.getElementById('canvas');
    ctx = canvas.getContext('2d');

    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
    //Click listener
    canvas.addEventListener('mousedown', (event) => {
        if(event.button==0) {
            click(event.offsetX,event.offsetY);
        }
    },false);
    canvas.addEventListener('touchstart', (event) => {
        click(event.touches[0].clientX,event.touches[0].clientY);
    },false);

    canvas.addEventListener('mouseup', (event) => {
        if(event.button==0) {
            release();
        }
    },false);
    canvas.addEventListener('touchend', () => {
        release();
    },false);

    canvas.addEventListener('mouseleave', () => {
        if(mousePressed) release();
    },false);
    //Mouse wheel listener
    canvas.addEventListener('wheel',(event) => {
        scrollSpeed = -100*Math.sign(event.deltaY);
    },false);
    //update mouse pos
    canvas.addEventListener('mousemove',(event) => {
        mouseMove.x = event.offsetX-mousePosition.x;
        mouseMove.y = event.offsetY-mousePosition.y;
        mousePosition.x = event.offsetX;
        mousePosition.y = event.offsetY;
        if(mousePressed) drag();
    },false);
    canvas.addEventListener('touchmove',(event) => {
        mouseMove.x = event.touches[0].clientX-mousePosition.x;
        mouseMove.y = event.touches[0].clientY-mousePosition.y;
        mousePosition.x = event.touches[0].clientX;
        mousePosition.y = event.touches[0].clientY;
        if(mousePressed) drag();

    },false);
    //update size
    window.addEventListener('resize',() => {
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
    },false);

    testImage = new Image;
    testImage.src = '/static/cards/back.png';
    testImage.addEventListener('load',() => {
        gameLoop(0);
    },false);
});
