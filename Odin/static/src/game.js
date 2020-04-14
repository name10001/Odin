/*

game.js has several classes that represent the state of the game and the objects in it.

*/


/**
 * Player object
 */
class Player {
    constructor(id, name, nCards, nPickup, possessedBy, effects) {
        this.id = id;
        this.name = name;
        this.nCards = nCards;
        this.nPickup = nPickup;
        this.possessedBy = possessedBy;
        this.effects = effects;
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

        if (id != undefined) {
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
        if (this.cardIds.length == 0) return;
        let card_array = [];
        for (let id of this.cardIds) {
            card_array.push(id);
        }
        game.playCard(card_array);
    }

    playSingle() {
        if (this.cardIds.length == 0) return;
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
    constructor(card, url) {
        this.name = card["name"];
        this.colour = card["colour"];
        this.type = card["type"];
        this.compatiblePickup = card["can be on pickup"];
        this.compatibilityDescription = card["compatibility description"];
        this.effectDescription = card["effect description"];
        this.url = url;
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
        this.playerType = "Player";

        // chat messages
        this.chat = [];

        // create list of all cards for the help system
        this.allCards = [];
        for (let card of ALL_CARDS) {
            this.allCards[card["name"]] = new Card(card, card["url"]);
        }
    }

    /**
     * Get the player from its index
     * @param {Number} id index of the player, default is your own id
     */
    getPlayerIndex(id = this.yourId) {
        return this.playerIndices[id];
    }

    /**
     * Get player object by id
     */
    getPlayer(id = this.yourId) {
        let index = this.getPlayerIndex(id);

        if (index == -1) return null;
        return this.players[index];
    }

    /**
     * Update the game based on information sent from the server
     * @param {*} update 
     */
    update(update) {
        if (DEBUG) { console.log("CARD UPDATE:"); console.log(update); }

        // UPDATE CARDS IN YOUR HAND
        if (update['your cards'] != undefined) {
            this.yourStacks.length = 0;
            //gui.cardScroller.items.length = 0;
            this.cardIndices = {};
            this.cardNameIndices = {};
            this.canPlay = 0;

            for (let card of update['your cards']) {
                if (card['can be played']) this.canPlay++;

                this.addCard(card['id'], card['name'], card['url'], card['can be played']);
            }
        }

        // OTHER CARDS

        //update cards at the top
        if (update['cards on deck'] != undefined) {
            this.topCards.length = 0;
            for (let card of update['cards on deck']) {
                this.topCards.push(card['url']);
            }
        }
        //update planning cards
        if (update['planning pile'] != undefined) {
            this.planningCards.length = 0;
            for (let card of update['planning pile']) {
                this.planningCards.push(card);
            }
        }

        // player type
        if (update["player type"] != undefined) {
            this.playerType = update["player type"];
        }

        //your player id
        if (update["your id"] != undefined)
            this.yourId = update["your id"];

        //turn override if you are playing as someone else
        if (update["playing as"] != undefined)
            this.playingAs = update["playing as"];

        //update pickup
        if (update["pickup size"] != undefined)
            this.pickupAmount = update['pickup size'];

        //update direction
        if (update["direction"] != undefined)
            this.direction = update['direction'];

        //can't play reason
        if (update["cant play reason"] != undefined) {
            this.cantPlayReason = update['cant play reason'];
        }

        // UPDATE PLAYERS
        if (update['players'] != undefined) {
            this.players.length = 0;
            this.playerIndices = {};
            for (let player of update['players']) {
                if (player['is turn']) {
                    //if this player is having their turn now
                    this.turn = this.players.length;
                }

                this.playerIndices[player['id']] = this.players.length;
                this.players.push(new Player(player['id'], player['name'], player['number of cards'], player['pickup amount'], player["possessed by"], player["effects"]));
            }
            if (this.playerType != 'Player') {
                this.playerIndices[this.yourId] = -1;
            }

            //check if it's your turn
            let index = this.getPlayerIndex();
            let playingAsIndex = -1;
            if (this.playingAs.length > 0) playingAsIndex = this.getPlayerIndex(this.playingAs);
            if (index == this.turn) {
                if (this.players[index].possessedBy.length == 0) {
                    // your turn
                    this.turnString = "Your Turn!";
                    this.yourTurn = true;
                }
                else {
                    // you are possessed
                    this.turnString = this.players[index].possessedBy + "'s Turn (Possessing)";
                    this.yourTurn = false;
                }
            }
            else if (this.turn == playingAsIndex) {
                //you are possessing someone else
                this.turnString = "Your Turn! (Possessing)";
                this.yourTurn = true;
            }
            else {
                if (this.players[this.turn].possessedBy.length > 0) {
                    this.turnString = this.players[this.turn].possessedBy + "'s Turn (Possessing)";
                } else {
                    this.turnString = this.players[this.turn].name + "'s Turn";
                }
                //another person's turn
                this.yourTurn = false;
            }
        }

        //player iteration amount
        if (update["iteration"] != undefined)
            this.skip = (update['iteration'] - 1) % this.players.length;

        gui.updateGame(this);
        eventHandler.finishedEvent();
    }

    /**
     * Add a card to your hand
     */
    addCard(id, name, url, canPlay) {
        // add to stack
        if (name in this.cardNameIndices) {
            let index = this.cardNameIndices[name];
            let cardStack = this.yourStacks[index];
            cardStack.addCard(id);
            this.cardIndices[id] = index;
        }
        else {
            let index = this.yourStacks.length;
            let cardStack = new CardStack(id, name, url, canPlay);
            this.yourStacks.push(cardStack);
            this.cardNameIndices[name] = index;
            this.cardIndices[id] = index;
        }
    }

    recieveMessage(data) {
        if (DEBUG) {
            console.log("Message from " + data["player"] + ": " + data["message"]);
        }
        this.chat.push(data);
        gui.updateChat(this.chat);
    }

    /**
     * Remove a card from your hand
     * @param {*} id 
     */
    removeCard(id) {
        if (!(id in this.cardIndices)) return;

        const index = this.cardIndices[id];

        const stack = this.yourStacks[index];
        if (!stack) return;

        stack.remove(id);
        delete this.cardIndices[id];

        /*if (stack.cardIds.length == 0) {
            this.yourStacks.splice(index, 1);
            delete this.cardNameIndices[stack.name];
            // recalculate all the fucking indices u fuck
            for (let i = index; i < this.yourStacks.length; i++) {
                const stack2 = this.yourStacks[i];
                this.cardNameIndices[stack2.name] = i;
                for (let id2 of stack2.cardIds) {
                    this.cardIndices[id2] = i;
                }
            }
        }*/
    }

    /**
     * Loop through all stacks and remove stacks which empty
     * Also recalculate the indices
     */
    clearEmptyStacks() {
        this.cardIndices = {};
        this.cardNameIndices = {};

        let i = 0;
        while (i < this.yourStacks.length) {
            let cardStack = this.yourStacks[i];
            if (cardStack.cardIds.length == 0) {
                //delete
                this.yourStacks.splice(i, 1);
            }
            else {
                this.cardNameIndices[cardStack.name] = i;
                for (let id of cardStack.cardIds) {
                    this.cardIndices[id] = i;
                }
                i++;
            }
        }
    }

    /**
     * Get the message in the play button
     */
    getPlayButtonMessage() {
        let playMessage;
        if (this.planningCards.length == 0) {
            playMessage = "+" + (this.pickupAmount == 0 ? '1' : this.pickupAmount);
        }
        else if (this.cantPlayReason.length > 0) {
            playMessage = this.cantPlayReason;
        }
        else {
            playMessage = "PLAY CARDS";
        }

        return playMessage;
    }

    /**
     * Get if the undo buttons are avaliable
     */
    undoAvaliable() {
        return this.planningCards.length > 0 && this.yourTurn;
    }

    /**
     * Get if the play button is avaliable
     */
    playAvaliable() {
        return this.yourTurn && this.cantPlayReason.length == 0;
    }

    playCard(card_array) {
        // leave picked_option as null unless needed
        socket.emit("game message", GAME_ID, "play cards", card_array);
    }

    ask(question) {
        gui.openPopup(() => $r(QuestionPopup, { key: '1', question }), question["allow cancel"], () => this.pickOption(null));
    }

    pickOption(optionId) {
        socket.emit("game message", GAME_ID, "answer", [optionId]);
        eventHandler.finishedEvent();
    }
    pickOptions(optionIds) {
        socket.emit("game message", GAME_ID, "answer", optionIds);
        eventHandler.finishedEvent();
    }

    undo() {
        socket.emit("game message", GAME_ID, "undo", null);
    }

    undoAll() {
        socket.emit("game message", GAME_ID, "undo all", null);
    }

    pickup() {
        socket.emit("game message", GAME_ID, "pickup", null);
    }

    finishTurn() {
        socket.emit("game message", GAME_ID, "finished turn", null);
    }

    quit() {
        socket.emit("game message", GAME_ID, "quit", null);
    }

    sendChat(message) {
        socket.emit("game message", GAME_ID, "chat", message);
    }
}
