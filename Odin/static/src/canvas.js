//constants
const CARD_WIDTH = 134;
const CARD_HEIGHT = 209;
const GAP_SIZE = 20;

class Button {
    constructor(x,y,width,height,text) {
        this.x = x;
        this.y = y;
        this.width = width;
        this.height = height;
        this.text = text;
        this.hover = false;
    }
    setHover(hover) {
        this.hover = hover;
    }
    
    updateLocation(x,y) {
        this.x = x;
        this.y = y;
    }

    draw(ctx) {
        //draw the next turn button
        ctx.fillStyle = "#376";
        ctx.strokeStyle = this.hover ? "#ffa" : "#fff";
        ctx.fillRect(this.x,this.y,this.width,this.height);
        ctx.strokeRect(this.x,this.y,this.width,this.height);
        ctx.fillStyle = this.hover ? "#ffa" : "#fff";
        ctx.textAlign = "center";
        ctx.font = "bold 16px Courier New";
        ctx.fillText(this.text,this.x+this.width/2,this.y+this.height/2+5);
    }

    isClicked(x,y) {
       return x>this.x && x<this.x+this.width && y>this.y && y<this.y+this.height;
    }
}

class GameCanvas {
    /**
     * Creates a game canvas
     */
    constructor() {
        this.canvas = document.getElementById('canvas');
        this.ctx = canvas.getContext('2d');
    
        this.canvas.width = window.innerWidth;
        this.canvas.height = window.innerHeight;
        
        //some assets
        this.backImage = new Image;
        this.backImage.src = '/static/cards/back.png';
        this.transparentImage = new Image;
        this.transparentImage.src = '/static/transparent.png';

        //load all events
        this.canvas.addEventListener('mousedown',mouseDown);
        this.canvas.addEventListener('touchstart',touchStart);
        this.canvas.addEventListener('mouseup',mouseUp);
        this.canvas.addEventListener('touchend',touchEnd);
        this.canvas.addEventListener('mouseleave',mouseLeave);
        this.canvas.addEventListener('wheel',mouseWheel);
        this.canvas.addEventListener('mousemove',mouseMove);
        this.canvas.addEventListener('touchmove',touchMove);
        window.addEventListener('resize',resize);

        this.cardImages = [];
        //load all card images
        for(let url of ALL_URLS) {
            let image = new Image;
            image.src = '/static/' + url;
            this.cardImages['/static/' + url] = image;
        }

        //work out some "constants"
        this.CARD_WIDTH = 134;
        this.CARD_HEIGHT = 209;
        this.GAP_SIZE = 20;
        this.CARD_WIDTH_GAP = this.CARD_WIDTH + this.GAP_SIZE;

        //initialize some variables
        this.mousePosition = {x:0,y:0};
        this.selectOffset = {x:0,y:0};
        this.clickPosition = {x:0,y:0};
        this.mouseMove = {x:0,y:0};
        this.draggedCard = -1;
        this.scrollOffset = -this.CARD_WIDTH/2;
        this.scrollSpeed = 0;
        this.dragType = 0;
        this.mousePressed = false;
        

        //some buttons?
        this.finishButton = new Button(this.canvas.width/2+120,this.canvas.height/2-30,120,60,"FINISHED");
        this.undoButton = new Button(this.canvas.width/2+270,this.canvas.height/2-30,120,60,"UNDO");
    }
    
    /**
     * Main game loop for updating the canvas
     */
    draw(dt) {
        //clear
        this.ctx.clearRect(0,0,canvas.width,canvas.height);
        
        //background
        this.ctx.fillStyle = "#222";
        this.ctx.globalAlpha = 0.6;
        this.ctx.fillRect(0,0,canvas.width,canvas.height);
        this.ctx.globalAlpha = 1;

        //draw discard pile
        if(GAME.topCards.length>0) {
            let x = this.canvas.width / 2 - this.CARD_WIDTH - (GAME.topCards.length-1)*40;
            let y = this.canvas.height / 2 - this.CARD_HEIGHT / 2;
            for(let image of GAME.topCards) {
                this.ctx.drawImage(image, x, y, this.CARD_WIDTH, this.CARD_HEIGHT);
                this.ctx.drawImage(this.transparentImage,x,y,this.CARD_WIDTH,this.CARD_HEIGHT);
                x+=40;
            }
        }
        //draw planning cards
        if(GAME.planningCards.length>0) {
            let x = this.canvas.width/2-this.CARD_WIDTH+20;
            let y = this.canvas.height/2-this.CARD_HEIGHT/2-20;
            let gap = 40;
            let maxGap = (y-20)/(GAME.planningCards.length-1);
            if(maxGap < gap) gap = maxGap;
            for(let card of GAME.planningCards) {
                this.ctx.drawImage(card.image,x,y,this.CARD_WIDTH,this.CARD_HEIGHT);
                y-=gap;
            }
        }

        //draw whose turn it is
        this.ctx.textAlign = "left";
        this.ctx.font = "bold 24px Courier New";
        this.ctx.fillStyle = "#fff";
        this.ctx.fillText(GAME.turnString,this.canvas.width/2+120,this.canvas.height/2-70);

        //draw buttons
        if(GAME.planningCards.length==0) {
            let pickupAmount = 1;
            if(GAME.pickupAmount>0) pickupAmount = GAME.pickupAmount;
            this.finishButton.text = "+" + pickupAmount;
        }
        else {
            this.finishButton.text = "PLAY CARDS";
        }
        this.finishButton.draw(this.ctx);

        if(GAME.planningCards.length>0) this.undoButton.draw(this.ctx);

        //draw hand scroller
        let scrollY = this.canvas.height-this.CARD_HEIGHT-100;
        let scrollX = this.getScrollBarX();
        this.ctx.strokeStyle = "#ddd";
        this.ctx.fillStyle = "#999";
        this.ctx.beginPath();
        this.ctx.moveTo(20,scrollY);
        this.ctx.lineTo(this.canvas.width-20,scrollY);
        this.ctx.stroke();
        this.ctx.fillRect(scrollX-50,scrollY-20,100,40);
        this.ctx.strokeRect(scrollX-50,scrollY-20,100,40);


        //draw your hand
        for(let i = 0; i<GAME.yourCards.length;i++) {
            let card = GAME.yourCards[i];
            if(i==this.draggedCard) continue;
            this.ctx.drawImage(card.image,
                this.canvas.width/2+this.scrollOffset+i*this.CARD_WIDTH_GAP,this.canvas.height-50-this.CARD_HEIGHT,
                this.CARD_WIDTH,this.CARD_HEIGHT);
            if(!card.allowedToPlay) {
                this.ctx.drawImage(this.transparentImage,
                    this.canvas.width/2+this.scrollOffset+i*this.CARD_WIDTH_GAP,this.canvas.height-50-this.CARD_HEIGHT,
                    this.CARD_WIDTH,this.CARD_HEIGHT);
            }
        }

        //draw card you are dragging
        if(this.draggedCard>=0) {
            this.ctx.drawImage(GAME.yourCards[this.draggedCard].image,this.mousePosition.x+this.selectOffset.x,this.mousePosition.y+this.selectOffset.y,this.CARD_WIDTH,this.CARD_HEIGHT);
            if(!GAME.yourCards[this.draggedCard].allowedToPlay) {
                this.ctx.drawImage(this.transparentImage,this.mousePosition.x+this.selectOffset.x,this.mousePosition.y+this.selectOffset.y,this.CARD_WIDTH,this.CARD_HEIGHT);
            }
        }
    }

    /**
     * Method when you tap/click a point on the screen
     */
    click(x, y) {
        this.mousePressed = true;
        this.mousePosition.x = x;
        this.mousePosition.y = y;
        //Clicked in hand area
        if(this.mousePosition.y > this.canvas.height-this.CARD_HEIGHT-70) {
            this.clickPosition.x = this.mousePosition.x-this.scrollOffset;
            this.clickPosition.y = this.mousePosition.y;
            this.dragType = 1;
        }
        //Clicked in the scroll area
        else if(this.mousePosition.y>this.canvas.height-this.CARD_HEIGHT-130) {
            this.dragType = 4;
        }
        //clicking on the finish turn button
        else if(this.finishButton.isClicked(this.mousePosition.x,this.mousePosition.y) && GAME.yourTurn) {
            GAME.finishTurn();
        }
        //clicking on the undo button
        else if(this.undoButton.isClicked(this.mousePosition.x,this.mousePosition.y) && GAME.planningCards.length>0) {
            GAME.undo();
        }
    }

    /**
     * Determines the card at the clickPosition
     */
    getClickedCard() {
        let x = this.clickPosition.x-this.canvas.width/2;
        let r = x % (this.CARD_WIDTH+20);
    
        if(r<=this.CARD_WIDTH && this.clickPosition.y<this.canvas.height-50 && this.clickPosition.y>this.canvas.height-50-this.CARD_HEIGHT) {
            let i = Math.floor(x/(this.CARD_WIDTH+20));
    
            if(i>=0 && i<GAME.yourCards.length) {
                //i is the card id you selected
                this.draggedCard = i;
                this.selectOffset.x = -r;
                this.selectOffset.y = (this.canvas.height-50-CARD_HEIGHT)-this.clickPosition.y;
                return;
            }
        }
    
        this.draggedCard = -1;
    }

    /**
     * When you drag the mouse/touch 
     */
    drag(x,y) {
        this.mouseMove.x = event.offsetX-this.mousePosition.x;
        this.mouseMove.y = event.offsetY-this.mousePosition.y;
        this.mousePosition.x = event.offsetX;
        this.mousePosition.y = event.offsetY;

        this.finishButton.setHover(this.finishButton.isClicked(this.mousePosition.x,this.mousePosition.y));
        this.undoButton.setHover(this.undoButton.isClicked(this.mousePosition.x,this.mousePosition.y));
        
        if(this.mousePressed) {
            //scrolling through cards
            if(this.dragType==2) {
                this.scrollOffset = this.mousePosition.x-this.clickPosition.x;
                if(this.mousePosition.y<this.canvas.height-130-CARD_HEIGHT) {
                    this.dragType = 3;
                    this.getClickedCard();
                }
            }
            //scrolling through cards using the scrollbar
            else if(this.dragType==4) {
                this.setScrollBarX();
            }
            //determine if you are dragging the mouse horizontally or vertically
            else if(this.dragType==1){
                if(Math.abs(this.mousePosition.x-this.scrollOffset-this.clickPosition.x)>20) {
                    this. dragType = 2;
                }
                else if(Math.abs(this.mousePosition.y-this.clickPosition.y)>20) {
                    this.dragType = 3;
                    this.getClickedCard();
                }
            }
        }
    }
    /**
     * Release the mouse/touch
     */
    release() {
        //selected a card
        if(this.draggedCard>=0 && this.mousePosition.y<this.canvas.height-this.CARD_HEIGHT-130) {
            let card = GAME.yourCards[this.draggedCard];
            if(card.allowedToPlay) {
                GAME.playCard(card.id,0,0);
            }
        }
        //pickup
        else if(this.draggedCard==-2 && this.mousePosition.y>this.canvas.height-this.CARD_HEIGHT-70) {
            GAME.pickup();
            GAME.finishTurn();
        }
        this.draggedCard = -1;
        this.mousePressed = false;
        this.dragType = 0;
    }

    /**
     * Scrolling 
     */
    scroll(dt) {
        //accelerate based on your dragging speed
        if(this.scrollSpeed > 0) {
            this.scrollSpeed-=dt;
            if(this.scrollSpeed<0) this.scrollSpeed = 0;
        }
        else if(this.scrollSpeed < 0) {
            this.scrollSpeed+=dt;
            if(this.scrollSpeed>0) this.scrollSpeed = 0;
        }

        this.scrollOffset+=this.scrollSpeed;
        if(this.scrollOffset < this.getMinScroll()) {
            this.scrollOffset = this.getMinScroll();
        }
        else if(this.scrollOffset > this.getMaxScroll()) {
            this.scrollOffset = this.getMaxScroll();
        }
    }

    getMinScroll() {
        return -GAME.yourCards.length*this.CARD_WIDTH_GAP-this.canvas.width/4;
    }
    getMaxScroll() {
        return this.canvas.width/4 + this.GAP_SIZE;
    }
    getScrollBarX() {
        let d = this.getMaxScroll()-this.getMinScroll();
        let interpolate = 1 - (this.scrollOffset-this.getMinScroll())/d;
        return 20+interpolate * (this.canvas.width-40);
    }
    setScrollBarX() {
        let interpolate = (this.mousePosition.x-20)/(this.canvas.width-40);
        if(interpolate<0) interpolate = 0;
        if(interpolate>1) interpolate = 1;
        interpolate = 1 - interpolate;
        this.scrollOffset = this.getMinScroll() + interpolate * (this.getMaxScroll()-this.getMinScroll());
    }
}



/*

VARIOUS EVENTS

*/

function mouseDown(event) {
    if(event.button == 0) {
        GAME_CANVAS.click(event.offsetX,event.offsetY);
    }
}
function touchStart(event) {
    GAME_CANVAS.click(event.touches[0].clientX,event.touches[0].clientY);
}
function mouseUp(event) {
    if(event.button==0) {
        GAME_CANVAS.release();
    }
}
function touchEnd(event) {
    GAME_CANVAS.release();
}
function mouseLeave(event) {
    if(GAME_CANVAS.mousePressed) {
        GAME_CANVAS.release();
    }
}
function mouseWheel(event) {
    GAME_CANVAS.scrollSpeed = -100 * Math.sign(event.deltaY);
}
function mouseMove(event) {
    GAME_CANVAS.drag(event.offsetX,event.offsetY);
}
function touchMove(event) {
    GAME_CANVAS.drag(event.touches[0].clientX, event.clientY);
}
function resize() {
    GAME_CANVAS.canvas.width = window.innerWidth;
    GAME_CANVAS.canvas.height = window.innerHeight;
    GAME_CANVAS.finishButton.updateLocation(GAME_CANVAS.canvas.width/2+120,GAME_CANVAS.canvas.height/2-30);
    GAME_CANVAS.undoButton.updateLocation(GAME_CANVAS.canvas.width/2+270,GAME_CANVAS.canvas.height/2-30);
}

var lastTime = 0;
function gameLoop(timestamp) {
    let dt = timestamp-lastTime;
    lastTime = timestamp;
    
    //update scrolling speed
    GAME_CANVAS.scroll(dt);
    GAME_CANVAS.draw(dt);

    requestAnimationFrame(gameLoop);
}