
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
        this.movingCards = [];


        //initialize some variables
        this.popup = null;
        this.playAll = false;

        //SOME BUTTONS


        //finish
        this.finishButton = new Button(CARD_WIDTH*2+1, 4, 2, "+1");
        this.finishButton.x = function() {
            return gui.getButtonX();
        }
        this.finishButton.y = function() {
            return gui.getBottomY() - GUI_SCALE*12;
        };
        //undo
        this.undoButton = new Button(CARD_WIDTH, 3, 1, "UNDO");
        this.undoButton.x = function() {
            return gui.getButtonX();
        }
        this.undoButton.y = function() {
            return gui.getBottomY() - GUI_SCALE*7;
        };
        //undo all
        this.undoAllButton = new Button(CARD_WIDTH, 3, 1, "UNDO ALL");
        this.undoAllButton.x = function() {
            return gui.getButtonX() + GUI_SCALE*(1+CARD_WIDTH);
        }
        this.undoAllButton.y = function() {
            return gui.getBottomY() - GUI_SCALE*7;
        };


        //SCROLLER
        this.cardScroller = new ScrollArea(new Container(),CARD_WIDTH+1,CARD_HEIGHT+6,3,0);
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

    getBottomY() {
        let y = canvas.height - GUI_SCALE*(CARD_HEIGHT+13);
        return y;
    }

    getDiscardWidth() {
        return GUI_SCALE*(15+CARD_WIDTH);
    }

    getButtonsWidth() {
        return GUI_SCALE*(1+2*CARD_WIDTH);
    }

    /**
     * Free horizontal space on the screen after adding together the width of the buttons and the width of the discard pile
     */
    getFreeSpace() {
        let taken = this.getDiscardWidth() + GUI_SCALE*6 + this.getButtonsWidth();
        return canvas.width - taken;
    }

    /**
     * Get the total width of all components on the screen: discard pile, buttons and player list
     * Player list is shifted right if there's enough horizontal space to add it.
     */
    getTotalWidth() {
        let freeSpace = this.getFreeSpace();
        if(freeSpace > GUI_SCALE + this.getButtonsWidth()) freeSpace -= GUI_SCALE + this.getButtonsWidth();
        return canvas.width - freeSpace;
    }

    /**
     * X position of the discard pile on screen
     * (Far left)
     */
    getDiscardX() {
        return (canvas.width - this.getTotalWidth())/2 + GUI_SCALE * 2;
    }

    /**
     * X position of the buttons on screen
     * (right of discard pile)
     */
    getButtonX() { 
        return this.getDiscardX() + this.getDiscardWidth() + GUI_SCALE*2;
    }

    /**
     * X position of the player list (left of the smaller player rectangles)
     * (Far right)
     */
    getPlayerX() {
        return canvas.width - (canvas.width - this.getTotalWidth())/2 - GUI_SCALE * 2 - this.getButtonsWidth();
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
        let leftX = this.getDiscardX();

        //draw discard pile
        if(game.topCards.length>0) {
            let gap = (this.getDiscardWidth()-this.CARD_WIDTH)/game.topCards.length;
            let x = leftX + (game.topCards.length-1)*gap;
            let y = bottomY-this.CARD_HEIGHT;
            for(let image of game.topCards) {
                ctx.drawImage(image, x, y, this.CARD_WIDTH, this.CARD_HEIGHT);
                ctx.drawImage(this.transparentImage,x,y,this.CARD_WIDTH,this.CARD_HEIGHT);
                x-=gap;
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
        drawText(game.turnString,canvas.width/2,bottomY+GUI_SCALE*3,"center",bigFontSize);

        //DRAW BUTTONS
        leftX = this.getButtonX();
        //finish button
        if(game.planningCards.length==0 || !game.yourTurn) {
            let pickupAmount = 1;
            if(game.pickupAmount>0) pickupAmount = game.pickupAmount;
            this.finishButton.text = "+" + pickupAmount;
        }
        else {
            this.finishButton.text = game.cantPlayReason==null ? "PLAY CARDS" : game.cantPlayReason;
        }
        this.finishButton.drawThis(game.yourTurn && game.cantPlayReason==null);

        //undo button(s)
        if(game.planningCards.length>0 && game.yourTurn) {
            this.undoButton.drawThis(true);
            this.undoAllButton.drawThis(true);
        }


        //draw players
        if(game.players.length>0) {
            let px = this.getPlayerX() - this.CARD_WIDTH;
            let fontSize = bigFontSize;
            let medFontSize = Math.round(GUI_SCALE*1.5);
            let py = GUI_SCALE;
            let pheight = GUI_SCALE*5;
            let pgap = GUI_SCALE;
            let pwidth = this.CARD_WIDTH + this.getButtonsWidth();

            let i = game.turn;
            let skip = game.skip;
            do {
                let player = game.players[i];
                //box
                ctx.fillStyle = i==game.yourId ? "#06cbbf" : "#038cde";
                ctx.strokeStyle = "#fff";
                ctx.lineJoin = "round";
                ctx.lineWidth = pheight*0.1;
                ctx.strokeStyle = "#000";
                ctx.strokeRect(px+3, py+3, pwidth, pheight);
                ctx.fillRect(px, py, pwidth, pheight);
                ctx.strokeStyle = "#fff";
                ctx.strokeRect(px, py, pwidth, pheight);
                
                //name
                drawText(player.name,px+fontSize/2,py+pheight/2+fontSize/3,"left",fontSize,fontSize*5,"#fff");
                drawText(player.nCards,px+pwidth-fontSize/2,py+pheight/2+fontSize/3,"right",fontSize,fontSize*4,"#fff");

                //adjust size for non-turn players
                if(i==game.turn) {
                    //draw extra details about the person's turn
                    if(game.turnsLeft>1) {
                        console.log("got here");
                        drawText(game.turnsLeft + " turns", px+fontSize*6,py+pheight*0.3,"left",fontSize/2,undefined,"#fff");
                    }


                    py+=pheight/2;
                    px+=this.CARD_WIDTH;
                    pwidth-=this.CARD_WIDTH;
                    pheight/=2;
                    fontSize = medFontSize;
                }
                else {
                    //draw skips
                    if(skip>0) {
                        ctx.strokeStyle = "#f00";
                        ctx.beginPath();
                        ctx.moveTo(px,py);
                        ctx.lineTo(px+pwidth,py+pheight);
                        ctx.moveTo(px,py+pheight);
                        ctx.lineTo(px+pwidth,py);
                        ctx.stroke();

                        skip--;
                    }
                }

                py+=pgap+pheight;
                i+=game.direction;
                if(i<0) i = game.players.length-1;
                else if(i>=game.players.length) i = 0;
            }while(i!=game.turn);
        }

        //draw pickup amount
        if(game.pickupAmount>0) {
            drawText("+" + game.pickupAmount, this.getPlayerX()-GUI_SCALE, GUI_SCALE*8.75, 
                    "right", bigFontSize, this.CARD_WIDTH);
        }

        //DRAW CARD SCROLLER
        this.cardScroller.draw();
        //DRAW POPUP
        if(this.popup!=null) this.popup.draw();
        

        //DRAW MOVING CARDS
        //TODO
        let cardIndex = 0;
        while(cardIndex < this.movingCards.length) {
            let card = this.movingCards[cardIndex];
            card.move(dt);
            if(card.isFinished()) {
                this.movingCards.splice(cardIndex,1);
            }else{
                card.draw();
                cardIndex++;
            }
        }
    }

    play(cardStack) {
        if(!cardStack.allowedToPlay) return;

        if(cardStack.optionIds.length>0) {
            this.popup = new OptionsWindow(cardStack);
        }
        else {
            this.popup = null;
            cardStack.playSingle();
        }
    }

    playAllCards(cardStack) {
        if(!cardStack.allowedToPlay) return;

        if(cardStack.optionIds.length>0) {
            this.popup = new OptionsWindow(cardStack);
            this.playAll = true;
        }
        else {
            this.popup = null;
            cardStack.playAll();
        }
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
        if(this.finishButton.isMouseOverThis() && game.yourTurn && game.cantPlayReason==null) {
            game.finishTurn();
        }
        //clicking on the undo button
        else if(this.undoButton.isMouseOverThis() && game.planningCards.length>0) {
            game.undo();
        }
        //clicking the undo all button
        else if(this.undoAllButton.isMouseOverThis() && game.planningCards.length>0) {
            game.undoAll();
        }
    }

    getCardWaitIncrement(count, maxWaitTime=1200) {
        return (maxWaitTime - maxWaitTime * Math.exp(-0.1*count))/count;
    }

    getPlanningPilePosition() {
        let x = this.getDiscardX()-GUI_SCALE;
        let y = this.getBottomY()-this.CARD_HEIGHT-GUI_SCALE;
        return {x, y};
    }

    /**
     * Animate a list of cards being played
     */
    animatePlayCards(cards) {
        if(game.yourTurn) {
            // cards from your hand
            let wait = 0;
            let planningPilePosition = this.getPlanningPilePosition();
            let waitIncr = this.getCardWaitIncrement(cards.length);
            for(let card of cards) {
                let index = game.cardIndices[card['id']];
                let position = this.cardScroller.getPositionOf(index);
                let image = game.allImages[card['card image url']];
                let movingCard = new AnimatedCard(position, planningPilePosition, 3, wait, image, this.CARD_WIDTH, this.CARD_HEIGHT);
                this.movingCards.push(movingCard);
                wait += waitIncr;
            }
        }
        else {
            // cards from another person's hand
            let wait = 0;
            let planningPilePosition = this.getPlanningPilePosition();
            let position = {x:canvas.width/2, y:-this.CARD_HEIGHT};
            let waitIncr = this.getCardWaitIncrement(cards.length);
            for(let card of cards) {
                let image = game.allImages[card['card image url']];
                let movingCard = new AnimatedCard(position, planningPilePosition, 3, wait, image, this.CARD_WIDTH, this.CARD_HEIGHT);
                this.movingCards.push(movingCard);
                wait += waitIncr;
            }
        }
    }

    /**
     * Animate the top card being undone
     */
    animateUndo() {
        let position = this.getPlanningPilePosition();
        let gap = GUI_SCALE*2;
        let maxGap = (position.y-GUI_SCALE)/(game.planningCards.length-1);
        if(maxGap < gap) gap = maxGap;
        position.y -= gap * (game.planningCards.length-1);

        let card = game.planningCards.pop();
        
        let endPosition = game.yourTurn ? {x:canvas.width/2, y:this.getBottomY()+GUI_SCALE*3.5} : {x:canvas.width/2, y:-this.CARD_HEIGHT};
        
        let image = card.image;
        
        let movingCard = new AnimatedCard(position, endPosition, 3, 0, image, this.CARD_WIDTH, this.CARD_HEIGHT);
        this.movingCards.push(movingCard);
    }

    /**
     * Animate all cards being undone
     */
    animateUndoAll() {
        //begin position
        let position = this.getPlanningPilePosition();
        let gap = GUI_SCALE*2;
        let maxGap = (position.y-GUI_SCALE)/(game.planningCards.length-1);
        if(maxGap < gap) gap = maxGap;
        position.y -= gap * (game.planningCards.length-1);

        //end position
        let endPosition = game.yourTurn ? {x:canvas.width/2, y:this.getBottomY()+GUI_SCALE*3.5} : {x:canvas.width/2, y:-this.CARD_HEIGHT};

        let wait = 0;
        let waitIncr = this.getCardWaitIncrement(game.planningCards.length);

        // loop
        while(game.planningCards.length > 0) {
            let card = game.planningCards.pop();
            let image = card.image;
            
            let movingCard = new AnimatedCard(position, endPosition, 3, wait, image, this.CARD_WIDTH, this.CARD_HEIGHT, true);
            this.movingCards.push(movingCard);
            wait+=waitIncr;
            position.y += gap;
        }
        this.movingCards.reverse();
    }

    /**
     * Animate picking up cards
     */
    animatePickup(cards) {
        let wait = 0;
        let waitIncr = this.getCardWaitIncrement(cards.length);
        let startPosition = {x:canvas.width, y: canvas.height/2};
        let endPosition =  {x:canvas.width/2, y:this.getBottomY()+GUI_SCALE*3.5};
        for(let url of cards) {
            let image = game.allImages[url];
            console.log(url);
            let movingCard = new AnimatedCard(startPosition, endPosition, 2, wait, image, this.CARD_WIDTH, this.CARD_HEIGHT);
            this.movingCards.push(movingCard);
            wait+=waitIncr;
        }
        this.movingCards.reverse();


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
        this.cardScroller.setScrollSpeed(amount*0.07);
        //this.scrollSpeed = -amount * this.CARD_WIDTH;
    }

    /**
     * Scrolling 
     */
    scroll(dt) {
        if(this.popup!=null) {
            this.popup.scroll(dt);
            return;
        }

        this.cardScroller.scroll(dt);
    }

    /**
     * Is called when you make a decision in the options menu
     */
    pickOption(card, pickedOption) {
        if(this.playAll) {
            card.playAll(pickedOption);
            
        }else {
            card.playSingle(pickedOption);
        }
        
        this.cancelOptions();
    }

    /**
     * Exit options menu
     */
    cancelOptions() {
        this.popup = null;
        this.playAll = false;
    }

}