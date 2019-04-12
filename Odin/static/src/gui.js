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


/**
 * Class for the main game canvas
 */
class Gui {
    /**
     * Creates a game canvas
     */
    constructor() {
        //some assets
        this.backImage = new Image;
        this.backImage.src = '/static/cards/back.png';
        this.transparentImage = new Image;
        this.transparentImage.src = '/static/transparent.png';


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
        this.dragAll = false;
        this.optionsWindow = null;
        this.scrollSpeed = 0;
        this.dragType = 0;
        this.mousePressed = false;

        //some buttons (update the size in the setCardDimensions() function)
        this.finishButton = new Button(0,0,0,0,"FINISHED");
        this.undoButton = new Button(0,0,0,0,"UNDO");
        
        //work out some "constants"
        this.setCardDimensions();
        this.scrollOffset = -this.CARD_WIDTH/2;
    }

    /**
     * Set the dimensions of gaps and gaps based on your canvas window size
     */
    setCardDimensions() {

        let width = canvas.width/6;
        if(width>MAX_CARD_WIDTH) width = MAX_CARD_WIDTH;
        let height = width/CARD_RATIO;
        if(height>canvas.height/4.2) height = canvas.height/4.2;

        this.CARD_WIDTH = height*CARD_RATIO;
        this.CARD_HEIGHT = height;
        
        this.GAP_SIZE = this.CARD_WIDTH/8;
        this.CARD_WIDTH_GAP = this.CARD_WIDTH + this.GAP_SIZE;


        //update buttons
        this.finishButton.updateSize(canvas.width/2+this.CARD_WIDTH*0.75,canvas.height/2-this.GAP_SIZE*1.5,this.CARD_WIDTH,this.GAP_SIZE*3);
        this.undoButton.updateSize(canvas.width/2+this.GAP_SIZE+this.CARD_WIDTH*1.75,canvas.height/2-this.GAP_SIZE*1.5,this.CARD_WIDTH,this.GAP_SIZE*3);
    }
    
    /**
     * Main game loop for updating the canvas
     */
    draw(dt) {
        //clear
        ctx.clearRect(0,0,canvas.width,canvas.height);
        
        //background
        ctx.fillStyle = "#222";
        ctx.globalAlpha = 0.6;
        ctx.fillRect(0,0,canvas.width,canvas.height);
        ctx.globalAlpha = 1;

        //draw discard pile
        if(game.topCards.length>0) {
            let x = canvas.width / 2 - this.CARD_WIDTH/2 - (game.topCards.length-1)*this.GAP_SIZE*2;
            let y = canvas.height / 2 - this.CARD_HEIGHT / 2;
            for(let image of game.topCards) {
                ctx.drawImage(image, x, y, this.CARD_WIDTH, this.CARD_HEIGHT);
                ctx.drawImage(this.transparentImage,x,y,this.CARD_WIDTH,this.CARD_HEIGHT);
                x+=this.GAP_SIZE*2;
            }
        }
        //draw planning cards
        if(game.planningCards.length>0) {
            let x = canvas.width/2-this.CARD_WIDTH/2+this.GAP_SIZE;
            let y = canvas.height/2-this.CARD_HEIGHT/2-this.GAP_SIZE;
            let gap = this.GAP_SIZE*2;
            let maxGap = (y-this.GAP_SIZE)/(game.planningCards.length-1);
            if(maxGap < gap) gap = maxGap;
            for(let card of game.planningCards) {
                ctx.drawImage(card.image,x,y,this.CARD_WIDTH,this.CARD_HEIGHT);
                y-=gap;
            }
        }

        //draw whose turn it is
        let fontSize = Math.round(this.CARD_WIDTH/8);
        if(fontSize>MAX_FONT_SIZE) fontSize = MAX_FONT_SIZE;
        ctx.textAlign = "left";
        ctx.font = "bold " + (fontSize*2) + "px Courier New";
        ctx.fillStyle = "#fff";
        ctx.fillText(game.turnString,canvas.width/2+this.CARD_WIDTH*0.75,canvas.height/2-this.GAP_SIZE*3.5);

        //draw buttons
        if(game.planningCards.length==0) {
            let pickupAmount = 1;
            if(game.pickupAmount>0) pickupAmount = game.pickupAmount;
            this.finishButton.text = "+" + pickupAmount;
        }
        else {
            this.finishButton.text = "PLAY CARDS";
        }
        this.finishButton.draw(ctx,fontSize,this.mousePosition,game.yourTurn);

        if(game.planningCards.length>0) this.undoButton.draw(ctx,fontSize,this.mousePosition,true);

        //draw players
        if(game.players.length>0) {
            let px = canvas.width/2-this.CARD_WIDTH*2.5;
            let py = canvas.height/2+this.CARD_HEIGHT/4;
            let pheight = this.GAP_SIZE*2.5;
            let pgap = this.GAP_SIZE;
            fontSize = Math.round(this.CARD_WIDTH/8);

            ctx.textAlign = "left";
            ctx.font = "bold " + fontSize + "px Courier New";
            let i = 0;
            for(let player of game.players) {
                //box
                ctx.fillStyle = i==game.yourId ? "#b99" : "#999";
                ctx.fillRect(px-fontSize/2,py-fontSize,this.CARD_WIDTH,pheight);
                if(i==game.turn) ctx.strokeStyle = "#ffa";
                else ctx.strokeStyle = "#fff";
                ctx.strokeRect(px-fontSize/2,py-fontSize,this.CARD_WIDTH,pheight);
                
                //name
                if(i==game.turn) ctx.fillStyle = "#ffa";
                else ctx.fillStyle = "#fff";
                ctx.fillText(player.name,px,py,this.CARD_WIDTH-fontSize);
                ctx.fillText(player.nCards,px,py+pgap,this.CARD_WIDTH-fontSize);

                //iterate
                py-=pgap+pheight;
                i++;
            }

            //draw an arrow to show direction
            ctx.strokeStyle = "#ffa";
            ctx.beginPath();
            let topy = py-fontSize+pheight+pgap+pheight/2;
            let bottomy = canvas.height/2+this.CARD_HEIGHT/4-fontSize+pheight/2;
            let arrowx = px+this.CARD_WIDTH+this.GAP_SIZE*0.75;
            ctx.moveTo(arrowx,topy);
            ctx.lineTo(arrowx,bottomy);
            ctx.stroke();
            //arrowhead
            ctx.beginPath();
            if(game.direction==1) {
                ctx.moveTo(arrowx-this.GAP_SIZE/2,topy+this.GAP_SIZE/2);
                ctx.lineTo(arrowx,topy);
                ctx.lineTo(arrowx+this.GAP_SIZE/2,topy+this.GAP_SIZE/2);
            }
            else {
                ctx.moveTo(arrowx-this.GAP_SIZE/2,bottomy-this.GAP_SIZE/2);
                ctx.lineTo(arrowx,bottomy);
                ctx.lineTo(arrowx+this.GAP_SIZE/2,bottomy-this.GAP_SIZE/2);
            }
            ctx.stroke();
        }

        //draw hand scroller
        let scrollY = canvas.height-this.CARD_HEIGHT-this.GAP_SIZE*3;
        let scrollX = this.getScrollBarX();
        ctx.strokeStyle = "#ddd";
        ctx.fillStyle = "#999";
        ctx.beginPath();
        ctx.moveTo(this.GAP_SIZE,scrollY);
        ctx.lineTo(canvas.width-this.GAP_SIZE,scrollY);
        ctx.stroke();
        ctx.fillRect(scrollX-this.CARD_WIDTH/2,scrollY-this.GAP_SIZE,this.CARD_WIDTH,this.GAP_SIZE*2);
        ctx.strokeRect(scrollX-this.CARD_WIDTH/2,scrollY-this.GAP_SIZE,this.CARD_WIDTH,this.GAP_SIZE*2);
        

        
        //draw your hand
        //number font
        ctx.font = "bold " + (fontSize*2) + "px Courier New";
        ctx.textAlign = "left";

        for(let i = 0; i<game.yourStacks.length;i++) {
            let stack = game.yourStacks[i];
            let stackSize = stack.size();
            if(stackSize>=100) stackSize = 99;//if you have >=100 of one type, just say 99
            if(i==this.draggedCard) {
                stackSize--;
                if(this.dragAll || stackSize==0) {
                    continue;
                }
            }
            let x = canvas.width/2+this.scrollOffset+i*this.CARD_WIDTH_GAP;
            let y = canvas.height-this.GAP_SIZE-this.CARD_HEIGHT;
            ctx.drawImage(stack.image,x,y,this.CARD_WIDTH,this.CARD_HEIGHT);
            if(!stack.allowedToPlay) {
                ctx.drawImage(this.transparentImage,
                    x,y,this.CARD_WIDTH,this.CARD_HEIGHT);
            }
            if(stackSize>1) {
                ctx.fillStyle = "#fff";
                ctx.fillRect(x,y+this.CARD_HEIGHT-fontSize*2.5,fontSize*5,fontSize*2.5);
                ctx.fillStyle = "#000";
                
                ctx.fillText("x" + stackSize, x+fontSize/2,y+this.CARD_HEIGHT-fontSize*0.5);
            }
        }

        //draw card you are dragging
        if(this.draggedCard>=0 && this.optionsWindow == null) {
            let x = this.mousePosition.x+this.selectOffset.x;
            let y = this.mousePosition.y+this.selectOffset.y;

            ctx.drawImage(game.yourStacks[this.draggedCard].image,x,y,this.CARD_WIDTH,this.CARD_HEIGHT);
            if(!game.yourStacks[this.draggedCard].allowedToPlay) {
                ctx.drawImage(this.transparentImage,x,y,this.CARD_WIDTH,this.CARD_HEIGHT);
            }
            if(this.dragAll) {
                let stack = game.yourStacks[this.draggedCard];
                let stackSize = stack.size();

                if(stackSize>1) {
                    ctx.fillStyle = "#fff";
                    ctx.fillRect(x,y+this.CARD_HEIGHT-fontSize*2.5,fontSize*5,fontSize*2.5);
                    ctx.fillStyle = "#000";
                    
                    ctx.fillText("x" + stackSize, x+fontSize/2,y+this.CARD_HEIGHT-fontSize*0.5);
                }
            }
        }


        //DRAW CARD OPTIONS WINDOW
        if(this.optionsWindow!=null) this.optionsWindow.draw(ctx, canvas.width/2-this.CARD_WIDTH*2,canvas.height/4,this.CARD_WIDTH*4,canvas.height/2);

    }

    /**
     * Method when you tap/click a point on the screen
     */
    click(x, y, shiftPressed) {
        if(this.optionsWindow!=null) {
            this.optionsWindow.click(x,y);
            return;
        }
        this.mousePressed = true;
        this.mousePosition.x = x;
        this.mousePosition.y = y;
        //Clicked in hand area
        if(this.mousePosition.y > canvas.height-this.CARD_HEIGHT-this.GAP_SIZE) {
            this.clickPosition.x = this.mousePosition.x-this.scrollOffset;
            this.clickPosition.y = this.mousePosition.y;
            this.dragType = 1;
            if(shiftPressed) this.dragAll = true;
        }
        //Clicked in the scroll area
        else if(this.mousePosition.y<canvas.height-this.CARD_HEIGHT-this.GAP_SIZE*2 && this.mousePosition.y>canvas.height-this.CARD_HEIGHT-this.GAP_SIZE*4) {
            this.dragType = 4;
        }
        //clicking on the finish turn button
        else if(this.finishButton.isClicked(this.mousePosition.x,this.mousePosition.y) && game.yourTurn) {
            game.finishTurn();
        }
        //clicking on the undo button
        else if(this.undoButton.isClicked(this.mousePosition.x,this.mousePosition.y) && game.planningCards.length>0) {
            game.undo();
        }
    }

    /**
     * Determines the card at the clickPosition
     */
    getClickedCard() {
        let x = this.clickPosition.x-canvas.width/2;
        let r = x % this.CARD_WIDTH_GAP;
    
        if(r<=this.CARD_WIDTH && this.clickPosition.y<canvas.height-this.GAP_SIZE && this.clickPosition.y>canvas.height-this.GAP_SIZE-this.CARD_HEIGHT) {
            let i = Math.floor(x/this.CARD_WIDTH_GAP);
    
            if(i>=0 && i<game.yourStacks.length) {
                //i is the card id you selected
                this.draggedCard = i;
                this.selectOffset.x = -r;
                this.selectOffset.y = (canvas.height-this.GAP_SIZE-this.CARD_HEIGHT)-this.clickPosition.y;
                return;
            }
        }
    
        this.draggedCard = -1;
    }

    /**
     * When you drag the mouse/touch 
     */
    drag(x,y) {
        if(this.optionsWindow!=null) {
            this.optionsWindow.drag(x,y);
            return;
        }
        this.mouseMove.x = x-this.mousePosition.x;
        this.mouseMove.y = y-this.mousePosition.y;
        this.mousePosition.x = x;
        this.mousePosition.y = y;
        
        if(this.mousePressed) {
            //scrolling through cards
            if(this.dragType==2) {
                this.scrollOffset = this.mousePosition.x-this.clickPosition.x;
                if(this.mousePosition.y<canvas.height-this.GAP_SIZE*3-this.CARD_HEIGHT) {
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
        if(this.optionsWindow!=null) {
            this.optionsWindow.release();
            return;
        }
        //selected a card
        if(this.draggedCard>=0 && this.mousePosition.y<canvas.height-this.CARD_HEIGHT-this.GAP_SIZE*3) {
            let card = game.yourStacks[this.draggedCard];
            if(card.allowedToPlay) {
                //TODO show all card options
                if(card.optionIds.length>0) {
                    //open option picking window
                    this.optionsWindow = new OptionsWindow(card,this.mousePosition);
                    //keep dragged card at same value
                    this.mousePressed = false;
                    this.dragType = 0;
                    if(IS_MOBILE) {
                        this.mousePosition.x = 0;
                        this.mousePosition.y = 0;
                    }
                    return;
                }else {
                    if(this.dragAll) {
                        card.playAll();
                    }
                    else {
                        card.playSingle();
                    }
                }
            }
        }
        this.draggedCard = -1;
        this.mousePressed = false;
        this.dragType = 0;
        this.dragAll = false;
        if(IS_MOBILE) {
            this.mousePosition.x = 0;
            this.mousePosition.y = 0;
        }
    }

    /** 
     * Mouse Wheel
     */
    wheel(amount) {
        if(this.optionsWindow!=null) {
            this.optionsWindow.wheel(amount);
            return;
        }
        this.scrollSpeed = -amount * this.CARD_WIDTH;
    }

    /**
     * Scrolling 
     */
    scroll(dt) {
        if(this.optionsWindow!=null) return;
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

    /**
     * Is called when you make a decision in the options menu
     */
    exitOptions(pickedOption) {
        this.optionsWindow = null;

        if(this.dragAll) {
            game.yourStacks[this.draggedCard].playAll(pickedOption);

        }else {
            game.yourStacks[this.draggedCard].playSingle(pickedOption);

        }
        //game.playCard(game.your[this.draggedCard].id,pickedOption);
        
        this.draggedCard = -1;
        this.dragAll = false;
    }

    getMinScroll() {
        return -game.yourStacks.length*this.CARD_WIDTH_GAP-canvas.width/4;
    }
    getMaxScroll() {
        return canvas.width/4 + this.GAP_SIZE;
    }
    getScrollBarX() {
        let d = this.getMaxScroll()-this.getMinScroll();
        let interpolate = 1 - (this.scrollOffset-this.getMinScroll())/d;
        return this.GAP_SIZE+interpolate * (canvas.width-(this.GAP_SIZE*2));
    }
    setScrollBarX() {
        let interpolate = (this.mousePosition.x-20)/(canvas.width-(this.GAP_SIZE*2));
        if(interpolate<0) interpolate = 0;
        if(interpolate>1) interpolate = 1;
        interpolate = 1 - interpolate;
        this.scrollOffset = this.getMinScroll() + interpolate * (this.getMaxScroll()-this.getMinScroll());
    }
}
