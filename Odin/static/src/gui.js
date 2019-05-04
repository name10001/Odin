
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
        this.currentAnimation = null;
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

        this.MIN_SOUND_DISPLACEMENT = 80;  // sounds will be 80ms apart at the minimum
        this.pickupSound = new Audio('/static/sounds/card_pickup.mp3');
        this.playSound = new Audio('/static/sounds/card_play.mp3');
        this.sovietFlag = new Image;
        this.sovietFlag.src = '/static/soviet.png';
        this.stalin = new Image;
        this.stalin.src = '/static/stalin.png';
        this.cardBack = new Image;
        this.cardBack.src = '/static/cards/back.png';
        this.skull = new Image;
        this.skull.src = '/static/skull.png';
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
        return GUI_SCALE*(1+2*CARD_WIDTH);
    }

    getDiscardHeight() {
        return GUI_SCALE*(CARD_HEIGHT+8);
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
     * 0 = vertical
     * 1 = horizontal
     */
    getLayoutType() {
        let freeSpace = this.getFreeSpace();

        if(freeSpace > GUI_SCALE + this.getButtonsWidth()) return 1;

        return 0;
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
     * Y distance from one player to the next
     */
    getPlayerGapSize() {
        let pheight = GUI_SCALE*5;
        let pgap = GUI_SCALE;
        let totalHeight = pheight + (game.players.length-2) * (pgap + pheight/2);
        let room = this.getBottomY() - GUI_SCALE*17;
        if(totalHeight > room) {
            let ratio = room/totalHeight;
            pheight*=ratio;
            pgap*=ratio;
        }
        return pheight/2 + pgap;

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
        let layoutType = this.getLayoutType();

        //draw deck
        let deckY = bottomY-this.getDiscardHeight()-this.CARD_HEIGHT;
        ctx.drawImage(this.cardBack, leftX, deckY, this.CARD_WIDTH, this.CARD_HEIGHT);

        //draw discard pile
        if(game.topCards.length>0) {
            let gap = (this.getDiscardHeight()-this.CARD_HEIGHT)/game.topCards.length;
            let x = leftX;
            let y = bottomY-this.CARD_HEIGHT;
            for(let image of game.topCards) {
                ctx.drawImage(image, x, y, this.CARD_WIDTH, this.CARD_HEIGHT);
                ctx.drawImage(this.transparentImage,x,y,this.CARD_WIDTH,this.CARD_HEIGHT);
                y-=gap;
            }
        }
        //draw planning cards
        if(game.planningCards.length>0) {
            let x = leftX+GUI_SCALE+this.CARD_WIDTH;
            let y = bottomY-this.CARD_HEIGHT;
            let gap = GUI_SCALE*2;

            let maxGap = (y-GUI_SCALE*10)/(game.planningCards.length-1);
            if(layoutType==1) {
                maxGap = (y-GUI_SCALE)/(game.planningCards.length-1);
            }
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
            let totalHeight = pheight + (game.players.length-2) * (pgap + pheight/2);
            let room = this.getBottomY() - GUI_SCALE*17;
            if(totalHeight > room) {
                let ratio = room/totalHeight;
                fontSize *= ratio;
                medFontSize *= ratio;
                pheight*=ratio;
                pgap*=ratio;
            }

            let i = game.turn;
            let skip = game.skip;
            do {
                let player = game.players[i];
                //box
                ctx.fillStyle = i==game.getPlayerIndex() ? "#06cbbf" : "#038cde";
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
                if(player.nPickup!=0) {
                    drawText((player.nPickup ? "+" : "") + player.nPickup, px+fontSize*5, py+pheight/2+fontSize/3, "left", fontSize, undefined, "#fff");
                }

                //adjust size for non-turn players
                if(i==game.turn) {
                    //draw extra details about the person's turn
                    if(game.turnsLeft>1) {
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
        this.cardScroller.draw(this.currentAnimation==null && this.popup==null);
        //DRAW POPUP
        if(this.popup!=null) this.popup.draw();
        if(this.currentAnimation!=null) this.currentAnimation.draw(dt);
        

        //DRAW MOVING CARDS
        let cardIndex = 0;
        while(cardIndex < this.movingCards.length) {
            let card = this.movingCards[cardIndex];
            card.move(dt);
            if(card.isFinished()) {
                this.movingCards.splice(cardIndex,1);
                card.playSound();
                card.place();
            }else{
                card.draw();
                cardIndex++;
            }
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

        if(this.currentAnimation!=null) return;//don't allow clicking on these buttons if an animation playing
        
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
        let x = this.getDiscardX()+this.CARD_WIDTH+GUI_SCALE;
        let y = this.getBottomY()-this.CARD_HEIGHT;

        let layoutType = this.getLayoutType();
        let gap = GUI_SCALE*2;

        if (game.planningCards.length == 0) {
            return {x, y, gap};
        }

        let maxGap = (y-GUI_SCALE*10)/(game.planningCards.length-1);
        if(layoutType==1) {
            maxGap = (y-GUI_SCALE)/(game.planningCards.length-1);
        }
        if(maxGap < gap) gap = maxGap;

        y -= gap * (game.planningCards.length-1);
        return {x, y, gap};
    }

    getDeckPosition() {
        return {x:this.getDiscardX(), y:this.getBottomY()-this.getDiscardHeight()-this.CARD_HEIGHT};
    }

    getPlayerPosition(playerId) {
        let x = this.getPlayerX();

        let gap = this.getPlayerGapSize();
        let y = gap;

        let i = game.turn;
        do {
            let player = game.players[i];
            
            console.log(player.id);
            if(player.id == playerId) break;
            y += gap;

            i+=game.direction;
            if(i<0) i = game.players.length-1;
            else if(i>=game.players.length) i = 0;
        }while(i != game.turn);

        return {x,y};
    }

    /**
     * Animate a list of cards being played
     */
    animatePlayCards(cards, fromDeck=false) {
        if(game.yourTurn && !fromDeck) {
            // cards from your hand
            let planningPilePosition = this.getPlanningPilePosition();
            this.animateMoveCardsFromHand(cards, planningPilePosition, function() {
                game.clearEmptyStacks();
                game.finishedEvent();
            }, function() {
                game.planningCards.push(new CardStack(this.id, this.cardStack.name, this.cardStack.url, true));
            });
            return;
        }
        // cards from another person's hand
        let wait = 0;
        let planningPilePosition = this.getPlanningPilePosition();
        planningPilePosition.y -= GUI_SCALE*2;

        //position either deck or from the player on their turn
        let position = fromDeck ? this.getDeckPosition() : {x:canvas.width/2, y:-this.CARD_HEIGHT};
        
        let waitIncr = this.getCardWaitIncrement(cards.length);
        let soundDisplacement = this.MIN_SOUND_DISPLACEMENT;
        let movingCard;
        for(let card of cards) {
            let image = game.allImages[card['card image url']];
            movingCard = new AnimatedCard(position, planningPilePosition, 300, wait, image, this.CARD_WIDTH, this.CARD_HEIGHT, soundDisplacement>=this.MIN_SOUND_DISPLACEMENT ? this.playSound : null);
            
            movingCard.id = card["id"];
            movingCard.name = card["name"];
            movingCard.url = card["card image url"];
            movingCard.place = function() {
                game.planningCards.push(new CardStack(this.id, this.name, this.url, true));
            }
            this.movingCards.push(movingCard);
            wait += waitIncr;
            if(soundDisplacement >= this.MIN_SOUND_DISPLACEMENT) soundDisplacement -= this.MIN_SOUND_DISPLACEMENT;
            soundDisplacement += waitIncr;
        }
        if(movingCard != undefined) {
            movingCard.place = function() {
                game.planningCards.push(new CardStack(this.id, this.name, this.url, true));
                game.finishedEvent();
            }
        }else game.finishedEvent();
    }

    animateFinishPlayCards(cards) {
        let startPosition = {x:this.getDiscardX() + GUI_SCALE + this.CARD_WIDTH, y:this.getBottomY()-this.CARD_HEIGHT};
        let endPosition = {x:this.getDiscardX(), y: this.getBottomY()-this.CARD_HEIGHT};

        let wait = 0;
        let waitIncr = this.getCardWaitIncrement(cards.length);
        let soundDisplacement = this.MIN_SOUND_DISPLACEMENT;
        let movingCard;
        for(let card of cards) {
            let image = game.allImages[card['card image url']];
            movingCard = new AnimatedCard(startPosition, endPosition, 300, wait, image, this.CARD_WIDTH, this.CARD_HEIGHT, soundDisplacement>=this.MIN_SOUND_DISPLACEMENT ? this.playSound : null);

            movingCard.release = function() {
                game.planningCards.splice(0,1);
            }
            movingCard.place = function() {
                game.topCards.splice(0,1);
                game.topCards.push(this.image);
            }
            this.movingCards.push(movingCard);
            wait += waitIncr;
            if(soundDisplacement >= this.MIN_SOUND_DISPLACEMENT) soundDisplacement -= this.MIN_SOUND_DISPLACEMENT;
            soundDisplacement += waitIncr;
        }
        if(movingCard != undefined) {
            movingCard.place = function() {
                game.topCards.splice(0,1);
                game.topCards.push(this.image);
                game.finishedEvent();
            }
        }else game.finishedEvent();
    }

    /**
     * Animate removing cards from your hand
     */
    animateRemoveCards(cards, finishEvent=true) {
        // cards from your hand
        this.animateMoveCardsFromHand(cards, this.getDeckPosition(), 
            finishEvent ? function() {
                game.clearEmptyStacks();
                game.finishedEvent(); 
            } : null);
    }

    animateMoveCardsFromHand(cards, endPosition, finishedFunction=null, cardPlaceFunction=null) {
        let wait = 0;
        let waitIncr = this.getCardWaitIncrement(cards.length);
        let soundDisplacement = this.MIN_SOUND_DISPLACEMENT;
        let movingCard;
        for(let card of cards) {
            let index = game.cardIndices[card['id']];

            if(index == undefined) {
                console.error("Could not find card to animate: " + card['id']);
                continue;
            }
            let position = this.cardScroller.getPositionOf(index);

            //adjust position if too far off screen
            if(position.x < -this.CARD_WIDTH) {
                position.x = -this.CARD_WIDTH;
            }
            else if(position.x > canvas.width) {
                position.x = canvas.width;
            }

            let image = game.allImages[card['card image url']];
            movingCard = new AnimatedCard(position, endPosition, 300, wait, image, this.CARD_WIDTH, this.CARD_HEIGHT, 
                soundDisplacement>=this.MIN_SOUND_DISPLACEMENT ? this.playSound : null);
            movingCard.cardStack = game.yourStacks[index];
            movingCard.id = card["id"];
            movingCard.release = function() {
                this.cardStack.remove(this.id);
            }
            if(cardPlaceFunction!=null) {
                movingCard.place = cardPlaceFunction;
            }
            this.movingCards.push(movingCard);
            wait += waitIncr;
            if(soundDisplacement >= this.MIN_SOUND_DISPLACEMENT) soundDisplacement -= this.MIN_SOUND_DISPLACEMENT;
            soundDisplacement += waitIncr;
        }
        if(finishedFunction!=null) {
            if(movingCard != undefined) {
                if(cardPlaceFunction != null) {
                    movingCard.cardPlaceFunction = cardPlaceFunction;
                    movingCard.finishedFunction = finishedFunction;
                    movingCard.place = function() {
                        this.cardPlaceFunction();
                        this.finishedFunction();
                    }
                }
                else {
                    movingCard.place = finishedFunction;
                }
            }else finishedFunction();
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
        
        let movingCard = new AnimatedCard(position, endPosition, 300, 0, image, this.CARD_WIDTH, this.CARD_HEIGHT, this.pickupSound);
        movingCard.place = function() {
            game.finishedEvent();
        }
        this.movingCards.push(movingCard);
    }

    /**
     * Animate all cards being undone
     */
    animateUndoAll() {
        //begin position
        let position = this.getPlanningPilePosition();
        let gap = position.gap;

        //end position
        let endPosition = game.yourTurn ? {x:canvas.width/2, y:this.getBottomY()+GUI_SCALE*3.5} : {x:canvas.width/2, y:-this.CARD_HEIGHT};

        let wait = 0;
        let waitIncr = this.getCardWaitIncrement(game.planningCards.length);
        
        let soundDisplacement = this.MIN_SOUND_DISPLACEMENT;
        let movingCard;

        // loop
        while(game.planningCards.length > 0) {
            let card = game.planningCards.pop();
            let image = card.image;
            
            movingCard = new AnimatedCard(position, endPosition, 300, wait, image, this.CARD_WIDTH, this.CARD_HEIGHT, 
                soundDisplacement>=this.MIN_SOUND_DISPLACEMENT ? this.pickupSound : null, true);
            this.movingCards.push(movingCard);
            wait+=waitIncr;
            position.y += gap;
            if(soundDisplacement >= this.MIN_SOUND_DISPLACEMENT) soundDisplacement -= this.MIN_SOUND_DISPLACEMENT;
            soundDisplacement += waitIncr;
        }
        if(movingCard != undefined) {
            movingCard.place = function() {
                game.finishedEvent();
            }
        }else game.finishedEvent();
        this.movingCards.reverse();
    }

    /**
     * Animate picking up cards
     */
    animatePickup(cards) {
        let wait = 0;
        let waitIncr = this.getCardWaitIncrement(cards.length);
        let startPosition = this.getDeckPosition();
        let endPosition =  {x:canvas.width/2, y:this.getBottomY()+GUI_SCALE*3.5};
        
        let soundDisplacement = this.MIN_SOUND_DISPLACEMENT;
        let movingCard;
        for(let card of cards) {
            let name = card["name"];
            let url = card["card image url"];
            let image = game.allImages[url];

            movingCard = new AnimatedCard(startPosition, endPosition, 600, wait, image, this.CARD_WIDTH, this.CARD_HEIGHT, soundDisplacement>=this.MIN_SOUND_DISPLACEMENT ? this.pickupSound : null);
            movingCard.id = card["id"];
            movingCard.name = name;
            movingCard.url = url;

            movingCard.place = function() {
                game.addCard(this.id, this.name, this.url, true);
            }
            
            this.movingCards.push(movingCard);
            wait+=waitIncr;
            if(soundDisplacement >= this.MIN_SOUND_DISPLACEMENT) soundDisplacement -= this.MIN_SOUND_DISPLACEMENT;
            soundDisplacement += waitIncr;
        }
        if(movingCard != undefined) {
            movingCard.place = function() {
                game.addCard(this.id, this.name, this.url, true);
                game.finishedEvent();
            }
        }else game.finishedEvent();
        this.movingCards.reverse();
    }

    /**
     * Animate a player picking up cards
     */
    animatePlayerPickup(playerId, nCards) {
        let wait = 0;
        let waitIncr = this.getCardWaitIncrement(nCards);
        let startPosition = this.getDeckPosition();
        let endPosition = this.getPlayerPosition(playerId);
        endPosition.y -= GUI_SCALE/2;
        let image = this.cardBack;
        let height = this.getPlayerGapSize();
        let width = height * CARD_RATIO;
        let soundDisplacement = this.MIN_SOUND_DISPLACEMENT;
        let movingCard;
        for(let i = 0; i < nCards; i++) {
            movingCard = new AnimatedCard(startPosition, endPosition, 400, wait, image, width, height, soundDisplacement>=this.MIN_SOUND_DISPLACEMENT ? this.pickupSound : null);
            this.movingCards.push(movingCard);
            wait+=waitIncr;
            if(soundDisplacement >= this.MIN_SOUND_DISPLACEMENT) soundDisplacement -= this.MIN_SOUND_DISPLACEMENT;
            soundDisplacement += waitIncr;
        }
        if(movingCard != undefined) {
            movingCard.place = function() {
                game.finishedEvent();
            }
        }else game.finishedEvent();
    }

    /**
     * Animate a player remove cards
     */
    animatePlayerRemove(playerId, nCards) {
        let wait = 0;
        let waitIncr = this.getCardWaitIncrement(nCards);
        let startPosition = this.getPlayerPosition(playerId);
        startPosition.y -= GUI_SCALE/2;
        let endPosition = this.getDeckPosition();
        let height = this.getPlayerGapSize();
        let width = height * CARD_RATIO;
        let image = this.cardBack;

        let soundDisplacement = this.MIN_SOUND_DISPLACEMENT;
        let movingCard;
        for(let i = 0; i < nCards; i++) {
            movingCard = new AnimatedCard(startPosition, endPosition, 400, wait, image, width, height, soundDisplacement>=this.MIN_SOUND_DISPLACEMENT ? this.playSound : null);
            this.movingCards.push(movingCard);
            wait+=waitIncr;
            if(soundDisplacement >= this.MIN_SOUND_DISPLACEMENT) soundDisplacement -= this.MIN_SOUND_DISPLACEMENT;
            soundDisplacement += waitIncr;
        }
        if(movingCard != undefined) {
            movingCard.place = function() {
                game.finishedEvent();
            }
        }else game.finishedEvent();
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
        this.cardScroller.release(this.currentAnimation==null && this.popup==null);
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
}