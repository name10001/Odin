
const CARD_RATIO = 300.0/469.0;
const CARD_WIDTH = 9;
const CARD_HEIGHT = CARD_WIDTH/CARD_RATIO;
const MIN_WIDTH = 48;//in terms of GUI_SCALE units
const MIN_HEIGHT = 64;

var DEBUG = true;

/**
 * Main method - sets up game, gui and listeners
 */
$(document).ready(function() {

    // SETUP GAME
    game = new Game();

    //SETUP GUI

    gui = ReactDOM.render(React.createElement(OdinGui, {}, null), document.getElementById("root"));
    
    // Setup Socket IO
    socket = io.connect(location.host, {
        'reconnection': true,
        'reconnectionDelay': 500,
        'maxReconnectionAttempts': Infinity
    });

    // initial connection
    socket.on('connect', function () {
        socket.emit("game message", GAME_ID, "initialise", null);
    });

    // popup message
    socket.on('popup message', function(message) {
        //game.addEvent(new GameEvent(function() {
        //    gui.currentAnimation = new MessageAnimation(message);
        //}));
    });

    // update the game
    socket.on('card update', function(update) {

        game.addEvent(new GameEvent(function() {
            game.update(update);
        }));
    });
    
    // play an animation
    socket.on('animate', function(data) {
        game.animate(data);
    });
    
    // ask a question
    socket.on('ask', function(question) {
        game.ask(question);
    });

    // recieve a chat message
    socket.on('chat', function(data) {
        game.receive_chat_message(data);
    });

    // force refresh
    socket.on("refresh", function() {
        game.addEvent(new GameEvent(function() {
            location.reload(true);
        }));
    });
    // you left
    socket.on('quit', function() {
        location.href = "/";
    });
});