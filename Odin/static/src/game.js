
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
        this.image = GAME_CANVAS.cardImages[url];
    }
}

class Game {
    constructor() {
        this.yourCards = [];
        this.topCards = [];
        this.yourPlayedCards = [];//TODO implement this
        this.yourTurn = false;
        this.yourId = 0;
        this.players = [];
        this.pickupAmount = 0;
        this.turn = 0;
        this.turnString = "";
    }

    update(update) {
        console.log(update);
        this.yourCards.length = 0;
    
        //update the cards in your hand
        for(let card of update['your cards']) {
            this.yourCards.push(new Card(card['card id'],card['card image url'],card['can be played']));
        }
    
        //update cards at the top
        this.topCards.length = 0;
        for(let card of update['cards on deck']) {
            this.topCards.push(GAME_CANVAS.cardImages[card['card image url']]);
        }
        //update pickup
        this.pickupAmount = update['pickup size'];
    
        //update players
        this.players.length = 0;
        for(let player of update['players']) {
            if(player['is you']) {
                this.yourId = this.players.length;
            }
            if(player['is turn']) {
                this.turn = this.players.length;
                if(player['is you']) {
                    this.turnString = "Your Turn";
                    this.yourTurn = true;
                }else {
                    this.turnString = player['name'] + "'s Turn";
                    this.yourTurn = false;
                }
            }
            this.players.push(new Player(player['name']));
        }
    }

    playCard(cardId, picked_option){
        // leave picked_option as null unless needed
        socket.emit("game message", GAME_ID, "play card", [cardId, picked_option]);
    }

    /*sayUno(){
        socket.emit("game message", GAME_ID, "uno", null);
    }*/

    pickup(){
        socket.emit("game message", GAME_ID, "pickup", null);
    }

    finishTurn(){
        // not currently working!
        socket.emit("game message", GAME_ID, "finished turn", null);
    }
}

function sayUno(){
    socket.emit("game message", GAME_ID, "uno", null);
}

function pickup(){
    socket.emit("game message", GAME_ID, "pickup", null);
}

function finishTurn(){
    socket.emit("game message", GAME_ID, "finished turn", null);
}

function undo(){
    socket.emit("game message", GAME_ID, "undo", null);
}
/*




        MAIN FUNCTION




 */
$(document).ready(function() {
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

    backImage = new Image;
    backImage.src = '/static/cards/back.png';
    transparentImage = new Image;
    transparentImage.src = '/static/transparent.png';

    gameLoop(0);
});
