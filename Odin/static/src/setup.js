
function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

/**
 * Main method - sets up game, gui and listeners
 */
$(document).ready(function() {
    // SocketIO
    socket = io.connect(document.domain, {
        'reconnection': true,
        'reconnectionDelay': 500,
        'maxReconnectionAttempts': Infinity
    });

    GAME = new Game();
    GUI = new Gui();

    socket.on('connect', function () {
        socket.emit("initial game connection", GAME_ID);
    });

    socket.on('message for player', function (message) {
        $("#message-from-server").html(message);
        $('.modal').modal("show");

    });

    socket.on('card update', function(update) {
        GAME.update(update);
    });
    
    //load all events
    if('ontouchstart' in document.documentElement) {
        GUI.canvas.addEventListener('touchstart',touchStart);
        GUI.canvas.addEventListener('touchmove',touchMove);
        GUI.canvas.addEventListener('touchend',touchEnd);
        IS_MOBILE = true;
    }
    else {
        GUI.canvas.addEventListener('mousedown',mouseDown);
        GUI.canvas.addEventListener('mousemove',mouseMove);
        GUI.canvas.addEventListener('mouseup',mouseUp);
        GUI.canvas.addEventListener('mouseleave',mouseLeave);
        GUI.canvas.addEventListener('wheel',mouseWheel);
        IS_MOBILE = false;
    }

    window.addEventListener('resize',resize);

    gameLoop(0);
});

function mouseDown(event) {
    if(event.button == 0) {
        GUI.click(event.offsetX,event.offsetY, event.shiftKey);//TODO change implementation
    }
}
function mouseMove(event) {
    GUI.drag(event.offsetX,event.offsetY);
}
function mouseUp(event) {
    if(event.button==0) {
        GUI.release();
    }
}

function touchStart(event) {
    GUI.click(event.touches[0].clientX,event.touches[0].clientY,false);
}
function touchMove(event) {
    GUI.drag(event.touches[0].clientX, event.touches[0].clientY);
}
function touchEnd(event) {
    GUI.release();
}

function mouseLeave(event) {
    if(GUI.mousePressed) {
        GUI.release();
    }
}
function mouseWheel(event) {
    GUI.wheel(Math.sign(event.deltaY));
}

/**
 * Resize method, calculates dimensions of items on the screen
 */
function resize() {
    GUI.setCardDimensions(window.innerWidth,window.innerHeight);
}

var lastTime = 0;
function gameLoop(timestamp) {
    sleep(10);
    let dt = timestamp-lastTime;
    lastTime = timestamp;
    
    //update scrolling speed
    GUI.scroll(dt);
    GUI.draw(dt);

    requestAnimationFrame(gameLoop);
}