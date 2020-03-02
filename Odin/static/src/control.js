/*

control.js initialises the game, gui and handles game events.

*/

const CARD_RATIO = 300.0 / 469.0;
const CARD_WIDTH = 9;
const CARD_HEIGHT = CARD_WIDTH / CARD_RATIO;
const MIN_WIDTH = 48;//in terms of GUI_SCALE units
const MIN_HEIGHT = 64;
const PICKUP_TIME = 500;
const REMOVE_TIME = 350;
const CARD_TRANSFER_TIME = 200;
const MAX_CARD_TRANSFER_TIME = 1500;

const $r = React.createElement;

var DEBUG = false;

/**
 * A list of functions to be performed in order. The function ends once eventHandler.finishedEvent() is called.
 */
class EventHandler {
    constructor() {
        this.events = [];
    }

    /**
     * Add a new event to the queue, if the queue is empty, run the event.
     */
    addEvent(event) {
        this.events.push(event);
        if (this.events.length == 1) {
            event();
        }
    }

    /**
     * Finish the current event in the queue and move onto the next one if it exists
     */
    finishedEvent() {
        if (this.events.length == 0) return;

        this.events.splice(0, 1);

        if (this.events.length > 0) {
            this.events[0]();
        }
    }
}

/**
 * Play a sound effect
 * @param {*} sound 
 */
function playSound(sound) {
    let audio = new Audio(sound);
    audio.play();
}

function removeCardsEvent(cards) {
    eventHandler.addEvent(() => {
        for (const card of cards) {
            game.removeCard(card.id);
        }
        gui.getCardScroller().updateStacks(game.yourStacks);
        eventHandler.finishedEvent();
    });
}

function addCardsEvent(cards) {
    eventHandler.addEvent(() => {
        for (const card of cards) {
            game.addCard(card.id, card.name, card.url, false);
        }
        gui.getCardScroller().updateStacks(game.yourStacks);
        eventHandler.finishedEvent();
    });
}

function clearEmptyStacksEvent(cards) {
    eventHandler.addEvent(() => {
        game.clearEmptyStacks();
        gui.getCardScroller().updateStacks(game.yourStacks);
        eventHandler.finishedEvent();
    });
}

function addPlanningCardsEvent(cards) {
    eventHandler.addEvent(() => {
        for (const card of cards) {
            game.planningCards.push(card);
        }
        gui.getPlanningPile().updateCards(game.planningCards.map((card) => card['url']));
        eventHandler.finishedEvent();
    });
}



/**
 * Main method - sets up game, gui and listeners
 */
$(document).ready(() => {

    // SETUP EVENT HANDLER

    eventHandler = new EventHandler();

    // SETUP GAME
    game = new Game();

    //SETUP GUI

    gui = ReactDOM.render($r(OdinGui, {}, null), document.getElementById("root"));

    // Setup Socket IO
    socket = io.connect(location.host, {
        'reconnection': true,
        'reconnectionDelay': 500,
        'maxReconnectionAttempts': Infinity
    });

    // initial connection
    socket.on('connect', () => {
        socket.emit("game message", GAME_ID, "initialise", null);
    });

    // popup message
    socket.on('popup message', function (message) {
        eventHandler.addEvent(() => {
            gui.showPopupMessage(message, 3000);
        });
    });

    // update the game
    socket.on('card update', function (update) {
        eventHandler.addEvent(() => {
            game.update(update);
        });
    });

    // play an animation
    socket.on('animate', function (data) {
        switch (data["type"]) {
            // ADD CARDS TO PLANNING PILE
            case "play cards":
                if (game.yourTurn && !data["from deck"]) {
                    removeCardsEvent(data["cards"]);
                }
                eventHandler.addEvent(() => {
                    gui.animatePlayCards(data["cards"], data["from deck"]);
                });

                addPlanningCardsEvent(data["cards"]);
                if (game.yourTurn && !data["from deck"]) {
                    clearEmptyStacksEvent();
                }
                break;
            // ADD PLANNING CARDS TO DISCARD PILE
            case "finish cards":
                eventHandler.addEvent(() => {
                    gui.animateFinishPlayCards(data["cards"]);
                });
                eventHandler.addEvent(() => {
                    for(const card of data["cards"]) {
                        game.topCards.splice(0, 1);
                        game.topCards.push(card.url);
                    }
                    
                    gui.getDiscardPile().updateCards(game.topCards);
                    eventHandler.finishedEvent();
                });
                break;
            // UNDO
            case "undo":
                eventHandler.addEvent(() => {
                    gui.animateUndo();
                });
                break;
            // UNDO ALL
            case "undo all":
                eventHandler.addEvent(() => {
                    gui.animateUndoAll();
                });
                break;
            // PICKUP
            case "pickup":
                if (data["from"] == null) {
                    eventHandler.addEvent(() => {
                        gui.animatePickupFromDeck(data["cards"]);  // pickup cards from deck
                    });
                }
                else {
                    eventHandler.addEvent(() => {
                        gui.animatePickupFromPlayer(data["cards"], data["from"]); //pickup cards from another player
                    });
                }

                addCardsEvent(data["cards"]);
                break;
            //PLAYER PICKUP
            case "player pickup":
                if (data["from"] == null) {
                    eventHandler.addEvent(() => {
                        gui.animatePlayerPickup(data["player"], data["count"]);
                    });
                }
                else {
                    eventHandler.addEvent(() => {
                        gui.animatePlayerCardTransfer(data['from'], data["player"], data["count"]);
                    });
                }
                break;
            // REMOVE CARD
            case "remove cards":
                if (data["to"] == null) {
                    eventHandler.addEvent(() => {
                        gui.animateRemoveCards(data["cards"]);
                    });
                } else {
                    eventHandler.addEvent(() => {
                        gui.animateRemoveCardsToPlayer(data["cards"], data["to"]);
                    });
                }
                clearEmptyStacksEvent();
                break;
            // PLAYER REMOVE CARD
            case "player remove cards":
                eventHandler.addEvent(() => {
                    gui.animatePlayerRemove(data["player"], data["count"]);
                });
                break;
            //COMMUNIST CARD
            case "communist":
                eventHandler.addEvent(() => {
                    gui.animateCommunism(data['cards']);
                });
                break;
            //GENOCIDE
            case "genocide":
                eventHandler.addEvent(() => {
                    playSound('/static/sounds/genocide.mp3');

                    const message = "All " + data["banned"] + " cards have been removed from the game";

                    gui.showPopupMessage(message, 4000, 0);
                });
                eventHandler.addEvent(() => {
                    gui.animateRemoveCards(data["cards"]);
                });
                break;
            //POSSESS
            case "possess":
                eventHandler.addEvent(() => {
                    playSound('/static/sounds/possess.mp3');

                    const possessorIndex = game.getPlayerIndex(data['possessor']);
                    const possessedIndex = game.getPlayerIndex(data['possessed']);


                    let message;
                    if (possessedIndex == game.getPlayerIndex()) {
                        message = "You have been possessed by " + game.players[possessorIndex].name;
                    }
                    else {
                        message = game.players[possessedIndex].name + " was possessed by " + game.players[possessorIndex].name;
                    }

                    gui.showPopupMessage(message, 4000, 0);
                });


                break;
            //SOUND EFFECT - FOR THINGS LIKE 69 NICE
            case "sound":
                eventHandler.addEvent(() => {
                    playSound(data["sound"]);
                    eventHandler.finishedEvent();
                });
                break;
        }
    });

    // ask a question
    socket.on('ask', function (question) {

        eventHandler.addEvent(() => {
            game.ask(question);
        });
    });

    // recieve a chat message
    socket.on('chat', function (data) {
        game.recieveMessage(data);
    });

    // force refresh
    socket.on("refresh", () => {
        eventHandler.addEvent(() => {
            location.reload(true);
        });
    });
    // you left
    socket.on('quit', () => {
        location.href = "/";
    });
});