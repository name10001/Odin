class Player {
    constructor(name, nCards) {
        this.name = name;
        this.nCards = nCards;
    }
}

class Card {
    constructor(id, url, allowedToPlay, options) {
        this.id = id;
        this.allowedToPlay = allowedToPlay;
        this.image = GAME_CANVAS.cardImages[url];
        this.optionStrings = [];
        this.optionIds = [];
        if(options!=null) {
            for(let id of Object.keys(options)) {
                this.optionIds.push(id);
                this.optionStrings.push(options[id]);
            }
        }
    }
}

class Game {
    constructor() {
        this.yourCards = [];
        this.topCards = [];
        this.planningCards = [];
        this.yourTurn = false;
        this.direction = 1;
        this.yourId = 0;
        this.players = [];
        this.pickupAmount = 0;
        this.turn = 0;
        this.turnString = "";
    }

    update(update) {
        //console.log(update);
        this.yourCards.length = 0;
    
        //update the cards in your hand
        for(let card of update['your cards']) {
            this.yourCards.push(new Card(card['card id'],card['card image url'],card['can be played'],card['options']));
        }
    
        //update cards at the top
        this.topCards.length = 0;
        for(let card of update['cards on deck']) {
            this.topCards.push(GAME_CANVAS.cardImages[card['card image url']]);
        }
        //update planning cards
        this.planningCards.length = 0;
        for(let card of update['planning pile']) {
            this.planningCards.push(new Card(card['card id'], card['card image url'], true,null));
        }

        //update pickup
        this.pickupAmount = update['pickup size'];

        //update direction
        this.direction = update['direction'];
    
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
            this.players.push(new Player(player['name'],player['number of cards']));
        }
    }

    playCard(cardId, picked_option){
        // leave picked_option as null unless needed
        socket.emit("game message", GAME_ID, "play card", [cardId, picked_option]);
    }

    /*sayUno(){
        socket.emit("game message", GAME_ID, "uno", null);
    }*/

    undo() {
        socket.emit("game message", GAME_ID, "undo", null);
    }


    pickup(){
        socket.emit("game message", GAME_ID, "pickup", null);
    }

    finishTurn(){
        // not currently working!
        socket.emit("game message", GAME_ID, "finished turn", null);
    }
}
