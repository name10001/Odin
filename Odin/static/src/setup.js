
function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

/**
 * Main method - sets up game, gui and listeners
 */
$(document).ready(function() {
    // SETUP GUI
    game = new Game();
    gui = new Gui();
    
    canvas = document.getElementById('canvas');
    resize();
    ctx = canvas.getContext('2d');
    
    // EVENTS
    if('ontouchstart' in document.documentElement) {
        canvas.addEventListener('touchstart',touchStart);
        canvas.addEventListener('touchmove',touchMove);
        canvas.addEventListener('touchend',touchEnd);
        IS_MOBILE = true;
    }
    else {
        canvas.addEventListener('mousedown',mouseDown);
        canvas.addEventListener('mousemove',mouseMove);
        canvas.addEventListener('mouseup',mouseUp);
        canvas.addEventListener('mouseleave',mouseLeave);
        canvas.addEventListener('wheel',mouseWheel);
        IS_MOBILE = false;
    }

    window.addEventListener('resize',resize);

    
    // SocketIO
    socket = io.connect(document.domain, {
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
        gui.click(event.offsetX,event.offsetY, event.shiftKey);//TODO change implementation
    }
}
function mouseMove(event) {
    gui.drag(event.offsetX,event.offsetY);
}
function mouseUp(event) {
    if(event.button==0) {
        gui.release();
    }
}

function touchStart(event) {
    gui.click(event.touches[0].clientX,event.touches[0].clientY,false);
}
function touchMove(event) {
    gui.drag(event.touches[0].clientX, event.touches[0].clientY);
}
function touchEnd(event) {
    gui.release();
}

function mouseLeave(event) {
    if(gui.mousePressed) {
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