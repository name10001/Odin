
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
        this.popup = null;
        this.playAll = false;

        //SOME BUTTONS


        //finish
        this.finishButton = new Button(CARD_WIDTH*2+1, 4, 2, "+1");
        this.finishButton.x = function() {
            return gui.getLeftX() + GUI_SCALE*18;
        }
        this.finishButton.y = function() {
            return gui.getBottomY() - GUI_SCALE*12;
        };
        //undo
        this.undoButton = new Button(CARD_WIDTH, 3, 1, "UNDO");
        this.undoButton.x = function() {
            return gui.getLeftX() + GUI_SCALE*18;
        }
        this.undoButton.y = function() {
            return gui.getBottomY() - GUI_SCALE*7;
        };
        //undo all
        this.undoAllButton = new Button(CARD_WIDTH, 3, 1, "UNDO ALL");
        this.undoAllButton.x = function() {
            return gui.getLeftX() + GUI_SCALE*(19+CARD_WIDTH);
        }
        this.undoAllButton.y = function() {
            return gui.getBottomY() - GUI_SCALE*7;
        };


        //SCROLLER
        this.cardScroller = new ScrollArea(new Container(),CARD_WIDTH+1,CARD_HEIGHT+9,3,0);
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

    getLeftX() {
        return (canvas.width/2-GUI_SCALE*22)*0.8;
    }

    getBottomY() {
        let y = canvas.height - GUI_SCALE*(CARD_HEIGHT+13);
        return y;
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

        let bottomY = this.getBottomY();
        if(LAYOUT_TYPE == 0) bottomY -= GUI_SCALE*3;
        let leftX = this.getLeftX();

        //draw discard pile
        if(game.topCards.length>0) {
            let x = leftX + (game.topCards.length-1)*GUI_SCALE*2;
            let y = bottomY-this.CARD_HEIGHT;
            for(let image of game.topCards) {
                ctx.drawImage(image, x, y, this.CARD_WIDTH, this.CARD_HEIGHT);
                ctx.drawImage(this.transparentImage,x,y,this.CARD_WIDTH,this.CARD_HEIGHT);
                x-=GUI_SCALE*2;
            }
        }
        //draw planning cards
        if(game.planningCards.length>0) {
            let x = leftX-GUI_SCALE;
            let y = bottomY-this.CARD_HEIGHT-GUI_SCALE;
            let gap = GUI_SCALE*2;
            let maxGap = (y-GUI_SCALE)/(game.planningCards.length-1);
            if(maxGap < gap) gap = maxGap;
            for(let card of game.planningCards) {
                ctx.drawImage(card.image,x,y,this.CARD_WIDTH,this.CARD_HEIGHT);
                y-=gap;
            }
        }

        //draw the number of cards you have
        let bigFontSize = Math.round(GUI_SCALE*2);
        ctx.textAlign = LAYOUT_TYPE == 0 ? "center" : "left";
        ctx.font = "bold " + bigFontSize + "px Courier New";
        ctx.fillStyle = "#fff";

        leftX += GUI_SCALE*18;

        if(LAYOUT_TYPE == 0) {
            ctx.fillText(game.turnString,canvas.width/2,bottomY+GUI_SCALE*3);
        }
        else {
            ctx.fillText(game.turnString,leftX,bottomY-GUI_SCALE/2);
        }

        //DRAW BUTTONS

        //finish button
        if(game.planningCards.length==0) {
            let pickupAmount = 1;
            if(game.pickupAmount>0) pickupAmount = game.pickupAmount;
            this.finishButton.text = "+" + pickupAmount;
        }
        else {
            this.finishButton.text = "PLAY CARDS";
        }
        this.finishButton.drawThis(game.yourTurn);

        //undo button(s)
        if(game.planningCards.length>0) {
            this.undoButton.drawThis(true);
            this.undoAllButton.drawThis(true);
        }


        //draw players
        if(game.players.length>0) {
            let px = canvas.width/2 - this.CARD_WIDTH;
            let fontSize = bigFontSize;
            let medFontSize = Math.round(GUI_SCALE*1.5);
            let py = GUI_SCALE;
            let pheight = GUI_SCALE*5;
            let pgap = GUI_SCALE;
            let pwidth = this.CARD_WIDTH*3+GUI_SCALE;

            ctx.font = "bold " + bigFontSize + "px Courier New";
            let i = game.turn;
            do {
                let player = game.players[i];
                //box
                ctx.fillStyle = i==game.yourId ? "#ece677" : "#a4e4e5";
                ctx.strokeStyle = "#fff";
                ctx.fillRect(px, py, pwidth, pheight);
                ctx.strokeRect(px, py, pwidth, pheight);
                
                //name
                ctx.fillStyle = "#000";
                ctx.textAlign = "left";
                ctx.fillText(player.name,px+fontSize/2,py+pheight/2+fontSize/3,fontSize*5);
                ctx.textAlign = "right";
                ctx.fillText(player.nCards,px+pwidth-fontSize/2,py+pheight/2+fontSize/3.,fontSize*4);

                //adjust size for non-turn players
                if(i==game.turn) {
                    py+=pheight/2;
                    ctx.font = "bold " + medFontSize + "px Courier New";
                    px+=this.CARD_WIDTH;
                    pwidth-=this.CARD_WIDTH;
                    pheight/=2;
                    fontSize = medFontSize;
                }
                py+=pgap+pheight;
                i+=game.direction;
                if(i<0) i = game.players.length-1;
                else if(i>=game.players.length) i = 0;
            }while(i!=game.turn);
        }


        //DRAW CARD SCROLLER
        this.cardScroller.draw();
        //DRAW POPUP
        if(this.popup!=null) this.popup.draw();
        

        //DRAW MOVING CARDS
        //TODO

    }

    /**
     * Method when you tap/click a point on the screen
     */
    click() {
        if(this.popup!=null) {
            this.popup.click();
            return;
        }
        this.cardScroller.click();
        
        //clciking the end turn button
        if(this.finishButton.isMouseOverThis() && game.yourTurn) {
            game.finishTurn();
        }
        //clicking on the undo button
        else if(this.undoButton.isMouseOverThis() && game.planningCards.length>0) {
            game.undo();
        }
        //clicking the undo all button
        else if(this.undoAllButton.isMouseOverThis() && game.planningCards.length>0) {
            for(let i = 0; i<game.planningCards.length;i++) {
                game.undo();
            }
        }
    }

    /**
     * When you drag the mouse/touch 
     */
    drag() {
        if(this.popup!=null) {
            this.popup.drag();
            return;
        }
        this.cardScroller.drag();
        
    }
    /**
     * Release the mouse/touch
     */
    release() {
        if(this.popup!=null) {
            this.popup.release();
            return;
        }
        this.cardScroller.release();
    }

    /** 
     * Mouse Wheel
     */
    wheel(amount) {
        if(this.popup!=null) {
            this.popup.wheel(amount);
            return;
        }
        this.cardScroller.setScrollSpeed(amount*0.7);
        //this.scrollSpeed = -amount * this.CARD_WIDTH;
    }

    /**
     * Scrolling 
     */
    scroll(dt) {
        if(this.popup!=null) return;

        this.cardScroller.scroll(dt);
    }

    /**
     * Is called when you make a decision in the options menu
     */
    exitOptions(card, pickedOption) {
        this.popup = null;

        if(this.playAll) {
            card.playAll(pickedOption);

        }else {
            card.playSingle(pickedOption);

        }
        //game.playCard(game.your[this.draggedCard].id,pickedOption);
        
        //this.draggedCard = -1;
        this.playAll = false;
    }

}
