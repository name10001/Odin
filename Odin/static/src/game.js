class Player {
    constructor(id, name, nCards, nPickup, isPossessed, effects) {
        this.id = id;
        this.name = name;
        this.nCards = nCards;
        this.nPickup = nPickup;
        this.isPossessed = isPossessed;
        this.effects = [];
        for(let effect of effects) {
            let image = game.allImages[effect["url"]];
            let amount = effect["amount left"];
            this.effects.push({"image": image, "amount left": amount});
        }
    }
}

class GameEvent {
    constructor(run) {
        this.run = run;
    }
}

/**
 * A stack of cards in your hand
 */
class CardStack {
    constructor(id, name, url, allowedToPlay) {
        this.allowedToPlay = allowedToPlay;
        this.url = url;
        this.name = name;
        this.card = game.allCards[name];
        this.image = game.allImages[url];

        if(id != undefined) {
            this.cardIds = [id];
        }
        else {
            this.cardIds = [];
        }
    }

    addCard(id) {
        this.cardIds.push(id);
    }

    playAll() {
        if(this.cardIds.length == 0) return;
        let card_array = [];
        for(let id of this.cardIds) {
            card_array.push(id);
        }
        game.playCard(card_array);
    }

    playSingle() {
        if(this.cardIds.length == 0) return;
        let id = this.cardIds[0];
        game.playCard([id]);
    }

    /**
     * Remove a card from the card stack
     */
    pop() {
        this.cardIds.splice(0, 1);
    }

    /**
     * Remove a card from the card stack by id
     */
    remove(id) {
        let index = this.cardIds.indexOf(id);
        this.cardIds.splice(index, 1);
    }

    size() {
        return this.cardIds.length;
    }
}

/**
 * Represents a card to be used for the help system. Has a name, image and some info to be used for its description
 */
class Card {
    constructor(card, image) {
        this.name = card["name"];
        this.colour = card["colour"];
        this.type = card["type"];
        this.compatiblePickup = card["can be on pickup"];
        this.compatibilityDescription = card["compatibility description"];
        this.effectDescription = card["effect description"];
        this.image = image;
    }
}

/**
 * Class representing all the current game objects
 */
class Game {
    constructor() {
        //your cards
        this.yourStacks = [];
        this.cardNameIndices = {};
        this.cardIndices = {};

        //top cards
        this.topCards = [];
        
        //planning cards
        this.planningCards = [];
        
        this.yourTurn = false;
        
        //players
        this.players = [];
        this.playerIndices = {};

        //some information about the current game/turn
        this.direction = 1;
        this.pickupAmount = 0;
        this.turn = 0;
        this.canPlay = 0;
        this.skip = 0;
        this.turnString = "";
        this.cantPlayReason = "";  // is empty if you are allowed to have your turn with the cards you have played
        this.playingAs = "";

        // chat messages
        this.chat = [];

        //event system
        this.events = [];

        //build a list of all cards - use the url as the key
        this.allImages = [];
        for(let url of ALL_URLS) {
            this.allImages[url] = new Image;
            this.allImages[url].src = url;
            this.allImages[url].onload = function() {
                gui.shouldDraw = true;
            }
        }
        this.allCards = [];
        for(let card of ALL_CARDS) {
            this.allCards[card["name"]] = new Card(card, this.allImages[card["url"]]); 
        }
    }

    /**
     * Add a new event to the queue, if the queue is empty, run the event.
     */
    addEvent(event) {
        this.events.push(event);
        if(this.events.length == 1) {
            event.run();
        }
    }

    /**
     * Finish the current event in the queue and move onto the next one if it exists
     */
    finishedEvent() {
        if(this.events.length == 0) return;

        this.events.splice(0, 1);

        if(this.events.length > 0) {
            this.events[0].run();
        }
    }

    getPlayerIndex(id=this.yourId) {
        return this.playerIndices[id];
    }

    /**
     * Get player object by id
     */
    getPlayer(id=this.yourId) {
        return this.players[this.getPlayerIndex(id)];
    }

    update(update) {
        if (DEBUG) {console.log("CARD UPDATE:"); console.log(update);}

        // UPDATE CARDS IN YOUR HAND
        if(update['your cards'] != undefined) {
            this.yourStacks.length = 0;
            gui.cardScroller.items.length = 0;
            this.cardIndices = {};
            this.cardNameIndices = {};
            this.canPlay = 0;
    
            for(let card of update['your cards']) {
                if(card['can be played']) this.canPlay++;
    
                this.addCard(card['card id'], card['name'], card['card image url'], card['can be played']);
            }
        }

        // OTHER CARDS

        //update cards at the top
        if(update['cards on deck'] != undefined) {
            this.topCards.length = 0;
            for(let card of update['cards on deck']) {
                this.topCards.push(this.allImages[card['card image url']]);
            }
        }
        //update planning cards
        if(update['planning pile'] != undefined) {
            this.planningCards.length = 0;
            for(let card of update['planning pile']) {
                this.planningCards.push(new CardStack(card['card id'], card['name'], card['card image url'], true));
            }
        }

        //your player id
        if(update["your id"] != undefined)
            this.yourId = update["your id"];
        
        //turn override if you are playing as someone else
        if(update["playing as"] != undefined)
            this.playingAs = update["playing as"];

        //update pickup
        if(update["pickup size"] != undefined)
            this.pickupAmount = update['pickup size'];

        //update direction
        if(update["direction"] != undefined)
            this.direction = update['direction'];

        //can't play reason
        if(update["cant play reason"] != undefined) {
            this.cantPlayReason = update['cant play reason'];
        }
        
        //player iteration amount
        if(update["iteration"] != undefined)
            this.skip = (update['iteration']-1) % this.players.length;
    
        // UPDATE PLAYERS
        if(update['players'] != undefined) {
            this.players.length = 0;
            this.playerIndices = {};
            for(let player of update['players']) {
                if(player['is turn']) {
                    //if this player is having their turn now
                    this.turn = this.players.length;
                }

                this.playerIndices[player['id']] = this.players.length;
                this.players.push(new Player(player['id'],player['name'],player['number of cards'],player['pickup amount'],player["is possessed"],player["effects"]));
            }

            //check if it's your turn
            let index = this.getPlayerIndex();
            let playingAsIndex = -1;
            if(this.playingAs.length > 0) playingAsIndex = this.getPlayerIndex(this.playingAs);
            if(index == this.turn) {
                if(!this.players[index].isPossessed) {
                    // your turn
                    this.turnString = "Your Turn! Cards Avaliable: " + this.canPlay + "/" + this.players[index].nCards;
                    this.yourTurn = true;
                }
                else {
                    // you are possessed
                    this.turnString = "You are possessed! Someone else is taking your turn.";
                    this.yourTurn = false;
                }
            }
            else if(this.turn == playingAsIndex) {
                //you are possessing someone else
                this.turnString = "Possessing " + this.players[playingAsIndex].name + "! Cards Avaliable: " + this.canPlay + "/" + this.players[playingAsIndex].nCards;
                this.yourTurn = true;
            }
            else {
                //another person's turn
                this.turnString = this.players[this.turn].name + "'s Turn";
                this.yourTurn = false;
            }
        }
        
        
        this.finishedEvent();
        gui.shouldDraw = true;
    }

    /**
     * Add a card to your hand
     */
    addCard(id, name, url, canPlay) {
        // add to stack
        if(name in this.cardNameIndices) {
            let index = this.cardNameIndices[name];
            let cardStack = this.yourStacks[index];
            cardStack.addCard(id);
            this.cardIndices[id] = index;
        }
        else {
            let index = this.yourStacks.length;
            let cardStack = new CardStack(id, name, url, canPlay);
            this.yourStacks.push(cardStack);
            gui.cardScroller.items.push(new CardStackPanel(cardStack));
            this.cardNameIndices[name] = index;
            this.cardIndices[id] = index;
        }
    }

    receive_chat_message(data) {
        if(DEBUG) {
            console.log("Message from " + data["player"] + ": " + data["message"]);
        }
        this.chat.push(data);
    }

    /**
     * Loop through all stacks and remove stacks which empty
     * Also recalculate the indices
     */
    clearEmptyStacks() {
        this.cardIndices = {};
        this.cardNameIndices = {};

        let i = 0;
        while(i < this.yourStacks.length) {
            let cardStack = this.yourStacks[i];
            if(cardStack.cardIds.length == 0) {
                //delete
                this.yourStacks.splice(i, 1);
                gui.cardScroller.items.splice(i, 1);
            }
            else {
                this.cardNameIndices[cardStack.name] = i;
                for(let id of cardStack.cardIds) {
                    this.cardIndices[id] = i;
                }
                i++;
            }
        }
    }

    animate(data) {
        switch(data["type"]) {
        // ADD CARDS TO PLANNING PILE
        case "play cards":
            this.addEvent(new GameEvent(function() {
                    gui.animatePlayCards(data["cards"],data["from deck"]);
                }));
            break;
        // ADD PLANNING CARDS TO DISCARD PILE
        case "finish cards":
            this.addEvent(new GameEvent(function() {
                    gui.animateFinishPlayCards(data["cards"]);
                }));
            break;
        // UNDO
        case "undo":
            this.addEvent(new GameEvent(function() {
                gui.animateUndo();
            }));
            break;
        // UNDO ALL
        case "undo all":
            this.addEvent(new GameEvent(function() {
                gui.animateUndoAll();
            }));
            break;
        // PICKUP
        case "pickup":
            if(data["from"] == null) {
                this.addEvent(new GameEvent(function() {
                    gui.animatePickupFromDeck(data["cards"]);  // pickup cards from deck
                }));
            }
            else {
                this.addEvent(new GameEvent(function() {
                    gui.animatePickupFromPlayer(data["cards"], data["from"]); //pickup cards from another player
                }));
            }
            break;
        //PLAYER PICKUP
        case "player pickup":
            if(data["from"] == null) {
                this.addEvent(new GameEvent(function() {
                    gui.animatePlayerPickup(data["player"], data["count"]);
                }));
            }
            else {
                this.addEvent(new GameEvent(function() {
                    gui.animatePlayerCardTransfer(data['from'], data["player"], data["count"]);
                }));
            }
            break;
        // REMOVE CARD
        case "remove cards":
            if(data["to"] == null) {
                this.addEvent(new GameEvent(function() {
                    gui.animateRemoveCards(data["cards"]);
                }));
            } else {
                this.addEvent(new GameEvent(function() {
                    gui.animateRemoveCardsToPlayer(data["cards"], data["to"]);
                }));
            }
            break;
        // PLAYER REMOVE CARD
        case "player remove cards":
            this.addEvent(new GameEvent(function() {
                gui.animatePlayerRemove(data["player"], data["count"]);
            }));
            break;
        //COMMUNIST CARD
        case "communist":
            this.addEvent(new GameEvent(function() {
                gui.currentAnimation = new CommunistAnimation(data["cards"]);
            }));
            break;
        //THANOS
        case "thanos":
            this.addEvent(new GameEvent(function() {
                gui.currentAnimation = new ThanosAnimation(data["cards"]);
            }));
            break;
        //THANOS
        case "genocide":
            this.addEvent(new GameEvent(function() {
                gui.currentAnimation = new GenocideAnimation(data["cards"], data['banned']);
            }));
            break;
        //POSSESS
        case "possess":
            this.addEvent(new GameEvent(function() {
                gui.currentAnimation = new PossessAnimation(data["possessor"], data["possessed"]);
            }));
            break;
        //SOUND EFFECT - FOR THINGS LIKE 69 NICE
        case "sound":
            this.addEvent(new GameEvent(function() {
                let audio = new Audio(data["sound"]);
                audio.play();
                game.finishedEvent();
            }));
            break;
        }
    }

    playCard(card_array){
        // leave picked_option as null unless needed
        socket.emit("game message", GAME_ID, "play cards", card_array);
    }

    ask(question) {
        gui.shouldDraw = true;
        this.addEvent(new GameEvent(function() {
            gui.popup = new OptionWindow(question);
        }));

    }

    pickOption(optionId) {
        socket.emit("game message", GAME_ID, "answer", [optionId]);
    }
    pickOptions(optionIds) {
        socket.emit("game message", GAME_ID, "answer", optionIds);
    }

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
        socket.emit("game message", GAME_ID, "finished turn", null);
    }

    quit() {
        socket.emit("game message", GAME_ID, "quit", null);
    }

    send_chat(message) {
        socket.emit("game message", GAME_ID, "chat", message);
    }
}
