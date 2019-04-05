
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
        this.players = [];
        this.pickupAmount = 0;
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
        this.yourTurn = update['your turn'];
    
        //update players
        
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