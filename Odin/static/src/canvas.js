//constants
const CARD_RATIO = 670.0/1045.0;
const MAX_CARD_WIDTH = 134;
const MAX_FONT_SIZE = 40;

class Button {
    constructor(x,y,width,height,text) {
        this.x = x;
        this.y = y;
        this.width = width;
        this.height = height;
        this.text = text;
    }
    
    updateSize(x,y,width,height) {
        this.x = x;
        this.y = y;
        this.width = width;
        this.height = height;
    }

    draw(ctx, fontSize, mousePosition, canPress) {
        let hover = this.isClicked(mousePosition.x,mousePosition.y);
        //draw the next turn button
        ctx.fillStyle = canPress ? "#376" : "#999";
        ctx.strokeStyle = canPress ? (hover ? "#ffa" : "#fff") : "#fff";
        ctx.fillRect(this.x,this.y,this.width,this.height);
        ctx.strokeRect(this.x,this.y,this.width,this.height);
        ctx.fillStyle = canPress ? (hover ? "#ffa" : "#fff") : "#bbb";
        ctx.textAlign = "center";
        ctx.font = "bold " + fontSize + "px Courier New";
        ctx.fillText(this.text,this.x+this.width/2,this.y+this.height/2+fontSize/3);
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
        if('ontouchstart' in document.documentElement) {
            this.canvas.addEventListener('touchstart',touchStart);
            this.canvas.addEventListener('touchmove',touchMove);
            this.canvas.addEventListener('touchend',touchEnd);
        }
        else {
            this.canvas.addEventListener('mousedown',mouseDown);
            this.canvas.addEventListener('mousemove',mouseMove);
            this.canvas.addEventListener('mouseup',mouseUp);
        }

        this.canvas.addEventListener('mouseleave',mouseLeave);
        this.canvas.addEventListener('wheel',mouseWheel);
        window.addEventListener('resize',resize);

        this.cardImages = [];
        //load all card images
        for(let url of ALL_URLS) {
            let image = new Image;
            image.src = '/static/' + url;
            this.cardImages['/static/' + url] = image;
        }


        //initialize some variables
        this.mousePosition = {x:0,y:0};
        this.selectOffset = {x:0,y:0};
        this.clickPosition = {x:0,y:0};
        this.mouseMove = {x:0,y:0};
        this.draggedCard = -1;
        this.scrollSpeed = 0;
        this.dragType = 0;
        this.mousePressed = false;

        //some buttons (update the size in the setCardDimensions() function)
        this.finishButton = new Button(0,0,0,0,"FINISHED");
        this.undoButton = new Button(0,0,0,0,"UNDO");
        
        //work out some "constants"
        this.setCardDimensions(window.innerWidth,window.innerHeight);
        this.scrollOffset = -this.CARD_WIDTH/2;
    }

    /**
     * Set the dimensions of gaps and gaps based on your canvas window size
     */
    setCardDimensions(newWidth, newHeight) {
        this.canvas.width = newWidth;
        this.canvas.height = newHeight;

        let width = this.canvas.width/6;
        if(width>MAX_CARD_WIDTH) width = MAX_CARD_WIDTH;
        let height = width/CARD_RATIO;
        if(height>this.canvas.height/4.2) height = this.canvas.height/4.2;

        this.CARD_WIDTH = height*CARD_RATIO;
        this.CARD_HEIGHT = height;
        
        this.GAP_SIZE = this.CARD_WIDTH/8;
        this.CARD_WIDTH_GAP = this.CARD_WIDTH + this.GAP_SIZE;


        //update buttons
        this.finishButton.updateSize(this.canvas.width/2+this.CARD_WIDTH*0.75,this.canvas.height/2-this.GAP_SIZE*1.5,this.CARD_WIDTH,this.GAP_SIZE*3);
        this.undoButton.updateSize(this.canvas.width/2+this.GAP_SIZE+this.CARD_WIDTH*1.75,this.canvas.height/2-this.GAP_SIZE*1.5,this.CARD_WIDTH,this.GAP_SIZE*3);
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
            let x = this.canvas.width / 2 - this.CARD_WIDTH/2 - (GAME.topCards.length-1)*this.GAP_SIZE*2;
            let y = this.canvas.height / 2 - this.CARD_HEIGHT / 2;
            for(let image of GAME.topCards) {
                this.ctx.drawImage(image, x, y, this.CARD_WIDTH, this.CARD_HEIGHT);
                this.ctx.drawImage(this.transparentImage,x,y,this.CARD_WIDTH,this.CARD_HEIGHT);
                x+=this.GAP_SIZE*2;
            }
        }
        //draw planning cards
        if(GAME.planningCards.length>0) {
            let x = this.canvas.width/2-this.CARD_WIDTH/2+this.GAP_SIZE;
            let y = this.canvas.height/2-this.CARD_HEIGHT/2-this.GAP_SIZE;
            let gap = this.GAP_SIZE*2;
            let maxGap = (y-this.GAP_SIZE)/(GAME.planningCards.length-1);
            if(maxGap < gap) gap = maxGap;
            for(let card of GAME.planningCards) {
                this.ctx.drawImage(card.image,x,y,this.CARD_WIDTH,this.CARD_HEIGHT);
                y-=gap;
            }
        }

        //draw whose turn it is
        let fontSize = Math.round(this.CARD_WIDTH/8);
        if(fontSize>MAX_FONT_SIZE) fontSize = MAX_FONT_SIZE;
        this.ctx.textAlign = "left";
        this.ctx.font = "bold " + (fontSize*2) + "px Courier New";
        this.ctx.fillStyle = "#fff";
        this.ctx.fillText(GAME.turnString,this.canvas.width/2+this.CARD_WIDTH*0.75,this.canvas.height/2-this.GAP_SIZE*3.5);

        //draw buttons
        if(GAME.planningCards.length==0) {
            let pickupAmount = 1;
            if(GAME.pickupAmount>0) pickupAmount = GAME.pickupAmount;
            this.finishButton.text = "+" + pickupAmount;
        }
        else {
            this.finishButton.text = "PLAY CARDS";
        }
        this.finishButton.draw(this.ctx,fontSize,this.mousePosition,GAME.yourTurn);

        if(GAME.planningCards.length>0) this.undoButton.draw(this.ctx,fontSize,this.mousePosition,true);

        //draw players
        if(GAME.players.length>0) {
            let px = this.canvas.width/2-this.CARD_WIDTH*2.5;
            let py = this.canvas.height/2+this.CARD_HEIGHT/2-this.GAP_SIZE*3.5*(GAME.players.length-1);
            this.ctx.textAlign = "left";
            this.ctx.font = "bold " + fontSize + "px Courier New";
            let i = 0;
            for(let player of GAME.players) {
                //box
                this.ctx.fillStyle = "#999";
                this.ctx.fillRect(px-fontSize/2,py-fontSize,this.CARD_WIDTH,this.GAP_SIZE*2.5);
                if(i==GAME.turn) this.ctx.strokeStyle = "#ffa";
                else this.ctx.strokeStyle = "#fff";
                this.ctx.strokeRect(px-fontSize/2,py-fontSize,this.CARD_WIDTH,this.GAP_SIZE*2.5);
                
                //name
                if(i==GAME.turn) this.ctx.fillStyle = "#ffa";
                else this.ctx.fillStyle = "#fff";
                this.ctx.fillText(player.name,px,py);
                this.ctx.fillText(player.nCards,px,py+this.GAP_SIZE);

                //iterate
                py-=this.GAP_SIZE*3.5;
                i++;
            }
        }

        //draw hand scroller
        let scrollY = this.canvas.height-this.CARD_HEIGHT-this.GAP_SIZE*3;
        let scrollX = this.getScrollBarX();
        this.ctx.strokeStyle = "#ddd";
        this.ctx.fillStyle = "#999";
        this.ctx.beginPath();
        this.ctx.moveTo(this.GAP_SIZE,scrollY);
        this.ctx.lineTo(this.canvas.width-this.GAP_SIZE,scrollY);
        this.ctx.stroke();
        this.ctx.fillRect(scrollX-this.CARD_WIDTH/2,scrollY-this.GAP_SIZE,this.CARD_WIDTH,this.GAP_SIZE*2);
        this.ctx.strokeRect(scrollX-this.CARD_WIDTH/2,scrollY-this.GAP_SIZE,this.CARD_WIDTH,this.GAP_SIZE*2);


        //draw your hand
        for(let i = 0; i<GAME.yourCards.length;i++) {
            let card = GAME.yourCards[i];
            if(i==this.draggedCard) continue;
            this.ctx.drawImage(card.image,
                this.canvas.width/2+this.scrollOffset+i*this.CARD_WIDTH_GAP,this.canvas.height-this.GAP_SIZE-this.CARD_HEIGHT,
                this.CARD_WIDTH,this.CARD_HEIGHT);
            if(!card.allowedToPlay) {
                this.ctx.drawImage(this.transparentImage,
                    this.canvas.width/2+this.scrollOffset+i*this.CARD_WIDTH_GAP,this.canvas.height-this.GAP_SIZE-this.CARD_HEIGHT,
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
        if(this.mousePosition.y > this.canvas.height-this.CARD_HEIGHT-this.GAP_SIZE) {
            this.clickPosition.x = this.mousePosition.x-this.scrollOffset;
            this.clickPosition.y = this.mousePosition.y;
            this.dragType = 1;
        }
        //Clicked in the scroll area
        else if(this.mousePosition.y<this.canvas.height-this.CARD_HEIGHT-this.GAP_SIZE*2 && this.mousePosition.y>this.canvas.height-this.CARD_HEIGHT-this.GAP_SIZE*4) {
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
        let r = x % this.CARD_WIDTH_GAP;
    
        if(r<=this.CARD_WIDTH && this.clickPosition.y<this.canvas.height-this.GAP_SIZE && this.clickPosition.y>this.canvas.height-this.GAP_SIZE-this.CARD_HEIGHT) {
            let i = Math.floor(x/this.CARD_WIDTH_GAP);
    
            if(i>=0 && i<GAME.yourCards.length) {
                //i is the card id you selected
                this.draggedCard = i;
                this.selectOffset.x = -r;
                this.selectOffset.y = (this.canvas.height-this.GAP_SIZE-this.CARD_HEIGHT)-this.clickPosition.y;
                return;
            }
        }
    
        this.draggedCard = -1;
    }

    /**
     * When you drag the mouse/touch 
     */
    drag(x,y) {
        this.mouseMove.x = x-this.mousePosition.x;
        this.mouseMove.y = y-this.mousePosition.y;
        this.mousePosition.x = x;
        this.mousePosition.y = y;
        
        if(this.mousePressed) {
            //scrolling through cards
            if(this.dragType==2) {
                this.scrollOffset = this.mousePosition.x-this.clickPosition.x;
                if(this.mousePosition.y<this.canvas.height-this.GAP_SIZE*3-this.CARD_HEIGHT) {
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
        if(this.draggedCard>=0 && this.mousePosition.y<this.canvas.height-this.CARD_HEIGHT-this.GAP_SIZE*3) {
            let card = GAME.yourCards[this.draggedCard];
            if(card.allowedToPlay) {
                GAME.playCard(card.id,null,null);
            }
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
        return this.GAP_SIZE+interpolate * (this.canvas.width-(this.GAP_SIZE*2));
    }
    setScrollBarX() {
        let interpolate = (this.mousePosition.x-20)/(this.canvas.width-(this.GAP_SIZE*2));
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
function mouseMove(event) {
    GAME_CANVAS.drag(event.offsetX,event.offsetY);
}
function mouseUp(event) {
    if(event.button==0) {
        GAME_CANVAS.release();
    }
}

function touchStart(event) {
    GAME_CANVAS.click(event.touches[0].clientX,event.touches[0].clientY);
}
function touchMove(event) {
    GAME_CANVAS.drag(event.touches[0].clientX, event.touches[0].clientY);
}
function touchEnd(event) {
    GAME_CANVAS.release();
    GAME_CANVAS.mousePosition.x = 0;
    GAME_CANVAS.mousePosition.y = 0;
}

function mouseLeave(event) {
    if(GAME_CANVAS.mousePressed) {
        GAME_CANVAS.release();
    }
}
function mouseWheel(event) {
    GAME_CANVAS.scrollSpeed = -GAME_CANVAS.CARD_WIDTH * Math.sign(event.deltaY);
}
function resize() {
    GAME_CANVAS.setCardDimensions(window.innerWidth,window.innerHeight);
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