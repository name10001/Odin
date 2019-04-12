class Player {
    constructor(name, nCards) {
        this.name = name;
        this.nCards = nCards;
    }
}

class CardStack {
    constructor(id, url, allowedToPlay, options) {
        this.allowedToPlay = allowedToPlay;
        this.options = options;
        this.url = url;
        this.image = gui.cardImages[url];
        this.optionStrings = [];
        this.optionIds = [];
        this.cardIds = [id];
        if(options!=null) {
            for(let id of Object.keys(options)) {
                this.optionIds.push(id);
                this.optionStrings.push(options[id]);
            }
        }
    }

    addCard(id) {
        this.cardIds.push(id);
    }

    playAll(options) {
        let card_array = [];
        for(let id of this.cardIds) {
            card_array.push([id,options]);
        }
        game.playCard(card_array);
    }

    playSingle(options) {
        let id = this.cardIds.pop();
        game.playCard([[id,options]]);
    }

    size() {
        return this.cardIds.length;
    }

}

class Game {
    constructor() {
        //this.yourCards = [];
        this.yourStacks = [];
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
        //this.yourCards.length = 0;
        

        this.yourStacks.length = 0;

        let cardStackPanels = [];
        let lastStack = null;
        //update the cards in your hand
        for(let card of update['your cards']) {
            //this.yourCards.push(new CardStack(card['card id'], card['card image url'], card['can be played'], card['options']));
            if(lastStack != null) {
                if(lastStack.url == card['card image url']) {
                    lastStack.addCard(card['card id']);
                    continue;
                }
            }
            lastStack = new CardStack(card['card id'], card['card image url'], card['can be played'], card['options']);
            this.yourStacks.push(lastStack);
            cardStackPanels.push(new CardStackPanel(lastStack));
        }
        gui.updateCards(cardStackPanels);

        //update cards at the top
        this.topCards.length = 0;
        for(let card of update['cards on deck']) {
            this.topCards.push(gui.cardImages[card['card image url']]);
        }
        //update planning cards
        this.planningCards.length = 0;
        for(let card of update['planning pile']) {
            this.planningCards.push(new CardStack(card['card id'], card['card image url'], true,null));
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

    playCard(card_array){
        // leave picked_option as null unless needed
        socket.emit("game message", GAME_ID, "play card", card_array);
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
