
const CARD_RATIO = 670.0/1045.0;
const CARD_WIDTH = 9;
const CARD_HEIGHT = CARD_WIDTH/CARD_RATIO;
const MIN_WIDTH = 48;//in terms of GUI_SCALE units
const MIN_HEIGHT = 65;

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

/**
 * Main method - sets up game, gui and listeners
 */
$(document).ready(function() {
    // SETUP GUI
    IS_MOBILE = 'ontouchstart' in document.documentElement;
    game = new Game();
    gui = new Gui();
    mousePosition = {x:0,y:0};
    mouseMoveVector = {x:0,y:0};
    mousePressed = false;
    
    canvas = document.getElementById('canvas');
    resize();
    ctx = canvas.getContext('2d');
    
    // EVENTS
    if(IS_MOBILE) {
        canvas.addEventListener('touchstart',touchStart);
        canvas.addEventListener('touchmove',touchMove);
        canvas.addEventListener('touchend',touchEnd);
    }
    else {
        canvas.addEventListener('mousedown',mouseDown);
        canvas.addEventListener('mousemove',mouseMove);
        canvas.addEventListener('mouseup',mouseUp);
        canvas.addEventListener('mouseleave',mouseLeave);
        canvas.addEventListener('wheel',mouseWheel);
    }

    window.addEventListener('resize',resize);

    
    // SocketIO
    socket = io.connect(location.host, {
        'reconnection': true,
        'reconnectionDelay': 500,
        'maxReconnectionAttempts': Infinity
    });

    socket.on('connect', function () {
        socket.emit("initial game connection", GAME_ID);
    });

    socket.on('message for player', function (message) {
        $("#message-from-server").html(message);
        $('.modal').modal("show");

    });

    socket.on('card update', function(update) {
        game.update(update);
    });

    // BEGIN GAMELOOP
    gameLoop(0);
});

function mouseDown(event) {
    if(event.button == 0) {
        mousePressed = true;
        mousePosition.x = event.offsetX;
        mousePosition.y = event.offsetY;
        gui.click();
    }
}
function mouseMove(event) {
    mouseMoveVector.x = event.offsetX - mousePosition.x;
    mouseMoveVector.y = event.offsetY - mousePosition.y;
    mousePosition.x = event.offsetX;
    mousePosition.y = event.offsetY;
    gui.drag();
}
function mouseUp(event) {
    if(event.button==0) {
        mousePressed = false;
        gui.release();
    }
}

function touchStart(event) {
    mousePressed = true;
    mousePosition.x = event.touches[0].clientX;
    mousePosition.y = event.touches[0].clientY;
    gui.click();
}
function touchMove(event) {
    mouseMoveVector.x = event.touches[0].clientX - mousePosition.x;
    mouseMoveVector.y = event.touches[0].clientY - mousePosition.y;
    mousePosition.x = event.touches[0].clientX;
    mousePosition.y = event.touches[0].clientY;
    gui.drag();
}
function touchEnd(event) {
    mousePressed = false;
    gui.release();
    mousePosition.x = 0;
    mousePosition.y = 0;
}

function mouseLeave(event) {
    if(mousePressed) {
        mousePressed = false;
        gui.release();
    }
}
function mouseWheel(event) {
    gui.wheel(Math.sign(event.deltaY));
}

/**
 * Resize method, calculates new GUI_SCALE and resizes the canvas
 */
function resize() {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;

    let width = canvas.width/MIN_WIDTH;
    let height = canvas.height/MIN_HEIGHT;

    if (width<height) GUI_SCALE = width;
    else GUI_SCALE = height;

    if(width/height < 0.9) LAYOUT_TYPE = 0;//Tall
    else if(width/height > 1.4) LAYOUT_TYPE = 2;//Wide
    else LAYOUT_TYPE = 1;//Square

    gui.setCardDimensions();
}

var lastTime = 0;
function gameLoop(timestamp) {
    sleep(2);
    let dt = timestamp-lastTime;
    lastTime = timestamp;
    
    //update scrolling speed
    gui.scroll(dt);
    gui.draw(dt);

    requestAnimationFrame(gameLoop);
}