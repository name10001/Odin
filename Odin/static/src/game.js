class Player {
    constructor(name, nCards) {
        this.name = name;
        this.nCards = nCards;
    }
}

/**
 * A stack of cards in your hand
 */
class CardStack {
    constructor(id, url, allowedToPlay, options) {
        this.allowedToPlay = allowedToPlay;
        this.options = options;
        this.url = url;
        this.card = game.allCards[url];
        this.image = game.allCards[url].image;
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

/**
 * Represents a card type. Has a name, image and some info to be used for its description
 */
class Card {
    constructor(card) {
        this.name = card["name"];
        this.colour = card["colour"];
        this.type = card["type"];
        this.compatiblePickup = card["can be on pickup"];
        this.compatibilityDescription = card["compatibility description"];
        this.effectDescription = card["effect description"];
        this.image = new Image;
        this.image.src = card["url"];
    }
}

/**
 * Class representing all the current game objects
 */
class Game {
    constructor() {
        this.yourStacks = [];
        this.topCards = [];
        this.planningCards = [];
        this.yourTurn = false;
        this.direction = 1;
        this.yourId = 0;
        this.players = [];
        this.pickupAmount = 0;
        this.turn = 0;
        this.turnsLeft = 1;
        this.skip = 0;
        this.turnString = "";
        this.cantPlayReason = null;  // is null if you are allowed to have your turn with the cards you have played

        //build a list of all cards - use the url as the key
        this.allCards = [];
        for(let card of ALL_CARDS) {
            this.allCards[card["url"]] = new Card(card); 
        }
    }

    update(update) {

        this.yourStacks.length = 0;

        let canPlay = 0;

        let cardStackPanels = [];
        let lastStack = null;
        //update the cards in your hand
        for(let card of update['your cards']) {
            if(card['can be played']) canPlay++;
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
            this.topCards.push(this.allCards[card['card image url']].image);
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

        //can't play reason
        this.cantPlayReason = update['cant play reason'];
        
    
        //update players
        this.players.length = 0;
        for(let player of update['players']) {
            if(player['is you']) {
                this.yourId = this.players.length;
            }
            if(player['is turn']) {
                this.turn = this.players.length;
                this.turnsLeft = player['turns left'];
                if(player['is you']) {
                    this.turnString = "Your Turn! Cards Avaliable: " + canPlay + "/" + player['number of cards'];
                    this.yourTurn = true;
                }else {
                    this.turnString = player['name'] + "'s Turn";
                    this.yourTurn = false;
                }
            }
            this.players.push(new Player(player['name'],player['number of cards']));
        }

        
        this.skip = (update['iteration']-1) % this.players.length; //tells you how many players will be skipped
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

    undoAll() {
        socket.emit("game message", GAME_ID, "undo all", null);
    }

    pickup(){
        socket.emit("game message", GAME_ID, "pickup", null);
    }

    finishTurn(){
        // not currently working!
        socket.emit("game message", GAME_ID, "finished turn", null);
    }
}
