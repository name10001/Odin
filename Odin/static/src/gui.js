
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
        //this.selectOffset = {x:0,y:0};
        //this.clickPosition = {x:0,y:0};
        //this.draggedCard = -1;
        //this.dragAll = false;
        this.optionsWindow = null;
        //this.scrollSpeed = 0;
        ///this.dragType = 0;
        ///this.scrollOffset = 0;
        this.playAll = false;

        //some buttons (update the size in the setCardDimensions() function)
        this.finishButton = new Button(CARD_WIDTH, 3, 1, "FINISHED");
        this.undoButton = new Button(CARD_WIDTH, 3, 1, "UNDO");

        this.cardScroller = new ScrollArea(new Container(),CARD_WIDTH+1,CARD_HEIGHT+5);
    }

    updateCards(cardPanels) {
        this.cardScroller.setItems(cardPanels);
    }

    /**
     * Set the dimensions of gaps and gaps based on your canvas window size
     */
    setCardDimensions() {
        this.CARD_WIDTH = CARD_WIDTH*GUI_SCALE;
        this.CARD_HEIGHT = CARD_HEIGHT*GUI_SCALE;
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
            let x = canvas.width / 2 - this.CARD_WIDTH/2 - (game.topCards.length-1)*GUI_SCALE*2;
            let y = canvas.height / 2 - this.CARD_HEIGHT / 2;
            for(let image of game.topCards) {
                ctx.drawImage(image, x, y, this.CARD_WIDTH, this.CARD_HEIGHT);
                ctx.drawImage(this.transparentImage,x,y,this.CARD_WIDTH,this.CARD_HEIGHT);
                x+=GUI_SCALE*2;
            }
        }
        //draw planning cards
        if(game.planningCards.length>0) {
            let x = canvas.width/2-this.CARD_WIDTH/2+GUI_SCALE;
            let y = canvas.height/2-this.CARD_HEIGHT/2-GUI_SCALE;
            let gap = GUI_SCALE*2;
            let maxGap = (y-GUI_SCALE)/(game.planningCards.length-1);
            if(maxGap < gap) gap = maxGap;
            for(let card of game.planningCards) {
                ctx.drawImage(card.image,x,y,this.CARD_WIDTH,this.CARD_HEIGHT);
                y-=gap;
            }
        }

        //draw whose turn it is
        let fontSize = Math.round(this.CARD_WIDTH/8);
        ctx.textAlign = "left";
        ctx.font = "bold " + (fontSize*2) + "px Courier New";
        ctx.fillStyle = "#fff";
        ctx.fillText(game.turnString,canvas.width/2+this.CARD_WIDTH*0.75,canvas.height/2-GUI_SCALE*3.5);

        //draw buttons
        if(game.planningCards.length==0) {
            let pickupAmount = 1;
            if(game.pickupAmount>0) pickupAmount = game.pickupAmount;
            this.finishButton.text = "+" + pickupAmount;
        }
        else {
            this.finishButton.text = "PLAY CARDS";
        }
        this.finishButton.draw(canvas.width/2+this.CARD_WIDTH*0.75,canvas.height/2-GUI_SCALE*1.5,game.yourTurn);

        if(game.planningCards.length>0) this.undoButton.draw(canvas.width/2+GUI_SCALE+this.CARD_WIDTH*1.75,canvas.height/2-GUI_SCALE*1.5,true);

        //draw players
        if(game.players.length>0) {
            let px = canvas.width/2-this.CARD_WIDTH*2.5;
            let py = canvas.height/2+this.CARD_HEIGHT/4;
            let pheight = GUI_SCALE*2.5;
            let pgap = GUI_SCALE;
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
            let arrowx = px+this.CARD_WIDTH+GUI_SCALE*0.75;
            ctx.moveTo(arrowx,topy);
            ctx.lineTo(arrowx,bottomy);
            ctx.stroke();
            //arrowhead
            ctx.beginPath();
            if(game.direction==1) {
                ctx.moveTo(arrowx-GUI_SCALE/2,topy+GUI_SCALE/2);
                ctx.lineTo(arrowx,topy);
                ctx.lineTo(arrowx+GUI_SCALE/2,topy+GUI_SCALE/2);
            }
            else {
                ctx.moveTo(arrowx-GUI_SCALE/2,bottomy-GUI_SCALE/2);
                ctx.lineTo(arrowx,bottomy);
                ctx.lineTo(arrowx+GUI_SCALE/2,bottomy-GUI_SCALE/2);
            }
            ctx.stroke();
        }
        this.cardScroller.draw();
        //DRAW CARD OPTIONS WINDOW
        if(this.optionsWindow!=null) this.optionsWindow.draw(canvas.width/2-this.CARD_WIDTH*2,canvas.height/4,this.CARD_WIDTH*4,canvas.height/2);

        //draw hand scroller
        /*let scrollY = canvas.height-this.CARD_HEIGHT-GUI_SCALE*3;
        let scrollX = this.getScrollBarX();
        ctx.strokeStyle = "#ddd";
        ctx.fillStyle = "#999";
        ctx.beginPath();
        ctx.moveTo(GUI_SCALE,scrollY);
        ctx.lineTo(canvas.width-GUI_SCALE,scrollY);
        ctx.stroke();
        ctx.fillRect(scrollX-this.CARD_WIDTH/2,scrollY-GUI_SCALE,this.CARD_WIDTH,GUI_SCALE*2);
        ctx.strokeRect(scrollX-this.CARD_WIDTH/2,scrollY-GUI_SCALE,this.CARD_WIDTH,GUI_SCALE*2);*/
        

        
        //draw your hand
        //number font
        /*ctx.font = "bold " + (fontSize*2) + "px Courier New";
        ctx.textAlign = "left";
        console.log(this.scrollOffset);

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
            let x = canvas.width/2+this.scrollOffset+i*(this.CARD_WIDTH+GUI_SCALE);
            let y = canvas.height-GUI_SCALE-this.CARD_HEIGHT;
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
        }*/

        //draw card you are dragging
        /*if(this.draggedCard>=0 && this.optionsWindow == null) {
            let x = mousePosition.x+this.selectOffset.x;
            let y = mousePosition.y+this.selectOffset.y;

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
        }*/



    }

    /**
     * Method when you tap/click a point on the screen
     */
    click() {
        if(this.optionsWindow!=null) {
            this.optionsWindow.click();
            return;
        }
        this.cardScroller.click();
        //Clicked in hand area
        /*if(mousePosition.y > canvas.height-this.CARD_HEIGHT-GUI_SCALE) {
            this.clickPosition.x = mousePosition.x-this.scrollOffset;
            this.clickPosition.y = mousePosition.y;
            this.dragType = 1;
            //if(shiftPressed) this.dragAll = true;
        }
        //Clicked in the scroll area
        else if(mousePosition.y<canvas.height-this.CARD_HEIGHT-GUI_SCALE*2 && mousePosition.y>canvas.height-this.CARD_HEIGHT-GUI_SCALE*4) {
            this.dragType = 4;
        }
        //clicking on the finish turn button
        else*/
        
        if(this.finishButton.isMouseOver(canvas.width/2+this.CARD_WIDTH*0.75,canvas.height/2-GUI_SCALE*1.5) && game.yourTurn) {
            game.finishTurn();
        }
        //clicking on the undo button
        else if(this.undoButton.isMouseOver(canvas.width/2+GUI_SCALE+this.CARD_WIDTH*1.75,canvas.height/2-GUI_SCALE*1.5) && game.planningCards.length>0) {
            game.undo();
        }
    }

    /**
     * Determines the card at the clickPosition
     */
    /*getClickedCard() {
        let x = this.clickPosition.x-canvas.width/2;
        let r = x % (this.CARD_WIDTH+GUI_SCALE);
    
        if(r<=this.CARD_WIDTH && this.clickPosition.y<canvas.height-GUI_SCALE && this.clickPosition.y>canvas.height-GUI_SCALE-this.CARD_HEIGHT) {
            let i = Math.floor(x/(this.CARD_WIDTH+GUI_SCALE));
    
            if(i>=0 && i<game.yourStacks.length) {
                //i is the card id you selected
                this.draggedCard = i;
                this.selectOffset.x = -r;
                this.selectOffset.y = (canvas.height-GUI_SCALE-this.CARD_HEIGHT)-this.clickPosition.y;
                return;
            }
        }
    
        this.draggedCard = -1;
    }*/

    /**
     * When you drag the mouse/touch 
     */
    drag() {
        if(this.optionsWindow!=null) {
            this.optionsWindow.drag();
            return;
        }
        this.cardScroller.drag();
        
        /*if(mousePressed) {
            //scrolling through cards
            if(this.dragType==2) {
                this.scrollOffset = mousePosition.x-this.clickPosition.x;
                if(mousePosition.y<canvas.height-GUI_SCALE*3-this.CARD_HEIGHT) {
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
                if(Math.abs(mousePosition.x-this.scrollOffset-this.clickPosition.x)>20) {
                    this. dragType = 2;
                }
                else if(Math.abs(mousePosition.y-this.clickPosition.y)>20) {
                    this.dragType = 3;
                    this.getClickedCard();
                }
            }
        }*/
    }
    /**
     * Release the mouse/touch
     */
    release() {
        if(this.optionsWindow!=null) {
            this.optionsWindow.release();
            return;
        }
        this.cardScroller.release();
        //selected a card
        /*if(this.draggedCard>=0 && mousePosition.y<canvas.height-this.CARD_HEIGHT-GUI_SCALE*3) {
            let card = game.yourStacks[this.draggedCard];
            if(card.allowedToPlay) {
                //TODO show all card options
                if(card.optionIds.length>0) {
                    //open option picking window
                    this.optionsWindow = new OptionsWindow(card,mousePosition);
                    //keep dragged card at same value
                    this.dragType = 0;
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
        this.dragType = 0;
        this.dragAll = false;*/
    }

    /** 
     * Mouse Wheel
     */
    wheel(amount) {
        if(this.optionsWindow!=null) {
            this.optionsWindow.wheel(amount);
            return;
        }
        this.cardScroller.setScrollSpeed(amount*0.7);
        //this.scrollSpeed = -amount * this.CARD_WIDTH;
    }

    /**
     * Scrolling 
     */
    scroll(dt) {
        if(this.optionsWindow!=null) return;

        this.cardScroller.scroll(dt);

        //accelerate based on your dragging speed
        /*if(this.scrollSpeed > 0) {
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
        }*/
    }

    /**
     * Is called when you make a decision in the options menu
     */
    exitOptions(card, pickedOption) {
        this.optionsWindow = null;

        if(this.playAll) {
            card.playAll(pickedOption);

        }else {
            card.playSingle(pickedOption);

        }
        //game.playCard(game.your[this.draggedCard].id,pickedOption);
        
        //this.draggedCard = -1;
        this.playAll = false;
    }

    /*getMinScroll() {
        return -game.yourStacks.length*(this.CARD_WIDTH+GUI_SCALE)-canvas.width/4;
    }
    getMaxScroll() {
        return canvas.width/4 + GUI_SCALE;
    }
    getScrollBarX() {
        let d = this.getMaxScroll()-this.getMinScroll();
        let interpolate = 1 - (this.scrollOffset-this.getMinScroll())/d;
        return GUI_SCALE+interpolate * (canvas.width-(GUI_SCALE*2));
    }
    setScrollBarX() {
        let interpolate = (mousePosition.x-20)/(canvas.width-(GUI_SCALE*2));
        if(interpolate<0) interpolate = 0;
        if(interpolate>1) interpolate = 1;
        interpolate = 1 - interpolate;
        this.scrollOffset = this.getMinScroll() + interpolate * (this.getMaxScroll()-this.getMinScroll());
    }*/
}
