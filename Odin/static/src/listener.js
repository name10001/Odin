
function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

/**
 * Sets up all listeners
 */
function setup() {
    //load all events
    if('ontouchstart' in document.documentElement) {
        this.canvas.addEventListener('touchstart',touchStart);
        this.canvas.addEventListener('touchmove',touchMove);
        this.canvas.addEventListener('touchend',touchEnd);
        IS_MOBILE = true;
    }
    else {
        this.canvas.addEventListener('mousedown',mouseDown);
        this.canvas.addEventListener('mousemove',mouseMove);
        this.canvas.addEventListener('mouseup',mouseUp);
        this.canvas.addEventListener('mouseleave',mouseLeave);
        this.canvas.addEventListener('wheel',mouseWheel);
        IS_MOBILE = false;
    }

    window.addEventListener('resize',resize);

    gameLoop(0);

}

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
        GUI.release(false);
    }
}

function touchStart(event) {
    GUI.click(event.touches[0].clientX,event.touches[0].clientY,false);
}
function touchMove(event) {
    GUI.drag(event.touches[0].clientX, event.touches[0].clientY);
}
function touchEnd(event) {
    GUI.release(true);
}

function mouseLeave(event) {
    if(GUI.mousePressed) {
        GUI.release();
    }
}
function mouseWheel(event) {
    GUI.wheel(Math.sign(event.deltaY));
}
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