function getLines(text, maxWidth) {
    let words = text.split(" ");
    let lines = [];
    let currentLine = words[0];

    for (let i = 1; i < words.length; i++) {
        let word = words[i];
        let width = ctx.measureText(currentLine + " " + word).width;
        if (width < maxWidth) {
            currentLine += " " + word;
        } else {
            lines.push(currentLine);
            currentLine = word;
        }
    }
    lines.push(currentLine);
    return lines;
}

class DescriptionWindow {
    constructor(cardStack) {
        this.image = cardStack.image;
        this.card = cardStack.card;
        this.cardStack = cardStack;
        this.allowedToPlay = cardStack.allowedToPlay;

        this.exitButton = new Button(CARD_WIDTH-1, 3, 1.5, "EXIT");
        this.exitButton.x = function() {
            return canvas.width/2 + (CARD_WIDTH*1.25+1) * GUI_SCALE;
        }
        this.exitButton.y = function() {
            return canvas.height/2 - (0.5*CARD_HEIGHT-2) * GUI_SCALE;
        }

        this.addButton = new Button(CARD_WIDTH-1, 3, 1.5, "ADD");
        this.addButton.x = function() {
            return canvas.width/2 + (CARD_WIDTH*1.25+1) * GUI_SCALE;
        }
        this.addButton.y = function() {
            return canvas.height/2 - (0.5*CARD_HEIGHT-6) * GUI_SCALE;
        }

        this.addallButton = new Button(CARD_WIDTH-1, 3, 1.5, "ADD ALL");
        this.addallButton.x = function() {
            return canvas.width/2 + (CARD_WIDTH*1.25+1) * GUI_SCALE;
        }
        this.addallButton.y = function() {
            return canvas.height/2 - (0.5*CARD_HEIGHT-10) * GUI_SCALE;
        }
    }

    getWidth() {
        return (CARD_WIDTH * 4.5 + 3) * GUI_SCALE;
    }
    getHeight() {
        return CARD_HEIGHT * 3 * GUI_SCALE;
    }
    getX() {
        return canvas.width/2 - this.getWidth()/2;
    }
    getY() {
        return canvas.height/2 - this.getHeight()/2;
    }

    draw() {
        let width = this.getWidth();
        let height = this.getHeight();
        let x = this.getX();
        let y = this.getY();

        let cardWidth = GUI_SCALE*CARD_WIDTH;
        let cardHeight = GUI_SCALE*CARD_HEIGHT;

        //draw the window
        ctx.strokeStyle = "#000";
        ctx.lineWidth = GUI_SCALE/2;
        ctx.strokeRect(x+3,y+3,width,height);
        ctx.fillStyle = "#0d3a0d";
        ctx.fillRect(x,y,width,height);
        ctx.strokeStyle = "#fff";
        ctx.strokeRect(x,y,width,height);

        //draw card
        ctx.drawImage(this.image,x+width-GUI_SCALE-cardWidth,y+GUI_SCALE,cardWidth,cardHeight);
        this.exitButton.drawThis(true);
        this.addButton.drawThis(this.allowedToPlay);
        this.addallButton.drawThis(this.allowedToPlay);
        
        let descWidth = 3.5*CARD_WIDTH*GUI_SCALE;
        
        //draw title
        drawText(this.card.name, x+GUI_SCALE+descWidth/2, y+GUI_SCALE*4, "center", GUI_SCALE*2.5, descWidth, true);

        //draw a description
        ctx.fillStyle = "#fff";
        ctx.textAlign = "left";
        y += GUI_SCALE*8;
        drawText("Effects", x+GUI_SCALE, y, "left", GUI_SCALE*2, descWidth, true);
        ctx.font = "bold " + Math.round(GUI_SCALE*1.4) + "px Arial";
        let effectLines = getLines(this.card.effectDescription,descWidth);
        y+=GUI_SCALE*2;
        for(let line of effectLines) {
            ctx.fillText(line,x+GUI_SCALE,y);
            y+=GUI_SCALE*1.5;
        }

        y+=GUI_SCALE*2;
        drawText("Compatibility", x+GUI_SCALE, y, "left", GUI_SCALE*2, descWidth, true);
        ctx.font = "bold " + Math.round(GUI_SCALE*1.4) + "px Arial";
        y += GUI_SCALE*2;
        let compatibilityLines = getLines(this.card.compatibilityDescription,descWidth);
        for(let line of compatibilityLines) {
            ctx.fillText(line,x+GUI_SCALE,y);
            y+=GUI_SCALE*1.5;
        }
        y+=GUI_SCALE/2;
        ctx.fillText("Pickup chains: " + (this.card.compatiblePickup ? "Compatible" : "Incompatible"), x+GUI_SCALE, y);

    }

    

    click() {
        //exit
        if(this.exitButton.isMouseOverThis() || mousePosition.x < this.getX() || mousePosition.x > this.getX()+this.getWidth() || mousePosition.y < this.getY() || mousePosition.y > this.getY()+this.getHeight()) {
            gui.popup = null;
        }
        //add
        else if(this.addButton.isMouseOverThis()) {
            gui.play(this.cardStack);
        }
        //add all
        else if(this.addallButton.isMouseOverThis()) {
            gui.playAllCards(this.cardStack);
        }
    }

    drag() {}
    
    release() {}
    wheel(amount) {}
    scroll(dt) {}
}


/**
 * Option in an option window
 */
class OptionItem {
    constructor(optionId, optionString) {
        //this.card = card;
        this.optionId = optionId;
        this.button = new Button(CARD_WIDTH*3-0.5,4.5,2,optionString);
    }

    draw(x,y,allowClick) {
        this.button.draw(x+GUI_SCALE*0.25,y+GUI_SCALE*0.25,allowClick);
    }

    click(x,y) {
        //gui.pickOption(this.card, this.optionId);
        game.pickOption(this.optionId);
        gui.popup = null;
        game.finishedEvent();
    }
}

class CardOptionItem {
    constructor(optionId, cardName, image, window) {
        //this.card = card;
        this.optionIds = [optionId];
        this.cardName = cardName;
        this.image = image;
        this.window = window;
    }

    addId(id) {
        this.optionIds.push(id);
    }

    draw(x,y,allowClick) {
        let stackSize = this.optionIds.length;
        if(stackSize>0) {
            ctx.drawImage(this.image, x, y, GUI_SCALE * CARD_WIDTH, GUI_SCALE * CARD_HEIGHT);

            // draw amount
            if(stackSize > 1) {
                ctx.fillStyle = "#fff";
                ctx.fillRect(x, y+GUI_SCALE*CARD_HEIGHT-GUI_SCALE*2.5,GUI_SCALE*5,GUI_SCALE*2.5);
                drawText("x" + stackSize, x+GUI_SCALE/2, y + GUI_SCALE*CARD_HEIGHT-GUI_SCALE/2, "left", GUI_SCALE * 2, GUI_SCALE*4, "#000");
            }
        }
    }

    click(x,y) {
        if(this.optionIds.length == 0 || this.window.selections.length == this.window.nToPick) return;
        this.window.selections.push({id:this.optionIds[0], stack:this});
        this.optionIds.splice(0, 1);
    }
}

/**
 * Class for the options window
 */
class OptionWindow {
    constructor(option) {
        //this.card = card;
        //this.image = card.image;
        this.optionTitle = option["title"];
        this.optionType = option["type"];
        this.allowCancel = option["allow cancel"];
        this.nToPick = option["number to pick"];
        this.image = game.allImages[option["image"]];
        this.selections = [];

        //create a cancel button
        if(this.allowCancel) {
            this.cancelButton = new Button(CARD_WIDTH,3,1.5,"CANCEL");
            this.cancelButton.window = this;
            this.cancelButton.x = function() {
                return this.window.getX() + this.window.getWidth() - GUI_SCALE * (1+CARD_WIDTH);
            }
            this.cancelButton.y = function() {
                return this.window.getY() + (CARD_HEIGHT+2) * GUI_SCALE;
            }
        }

        // BUTTONS
        if(this.optionType == "buttons") {
            this.buttons = [];
            for(let optionId of Object.keys(option["options"])) {
                this.buttons.push({
                    id:optionId,
                    button:new Button(CARD_WIDTH*3-0.5, 4.5, 2, option["options"][optionId])
                });
            }
            this.drawItems = function() {
                let x = this.getX() + GUI_SCALE*3;
                let y = this.getY() + GUI_SCALE*11;
                for(let i = 0; i < this.buttons.length; i++) {
                    this.buttons[i].button.draw(x,y,true);
                    y += 5 * GUI_SCALE;
                }
            }
            this.clickItems = function() {
                let x = this.getX() + GUI_SCALE*3;
                let y = this.getY() + GUI_SCALE*11;
                for(let button of this.buttons) {
                    if(button.button.isMouseOver(x,y)) {
                        game.pickOption(button.id);
                        gui.popup = null;
                        game.finishedEvent();
                        return;
                    }
                    y+=5 * GUI_SCALE;
                }
            }
        }
        // CARDS
        else if (this.optionType == "cards") {
            this.scrollContainer = new Container();
            this.scrollContainer.window = this;
            
            this.getWidth = function() {
                return canvas.width - GUI_SCALE/2;
                //let maxWidth = (6 * CARD_WIDTH) * GUI_SCALE;
                //if(canvas.width-GUI_SCALE < maxWidth) return canvas.width - GUI_SCALE;
                //else return maxWidth;
            }
            this.scrollContainer.getLeft = function() {
                return GUI_SCALE/4;
                //return this.window.getX() + GUI_SCALE*(CARD_WIDTH+1);
            }
            this.scrollContainer.getRight = function() {
                return canvas.width - GUI_SCALE/4;
                //return this.window.getX() + this.window.getWidth() - GUI_SCALE * (CARD_WIDTH + 1);
            }
            this.scrollContainer.getTop = function() {
                return this.window.getY();
            }
            this.scrollContainer.getBottom = function() {
                return this.window.getY() + this.window.getHeight() - GUI_SCALE;
            }

            //confirm button
            this.confirmButton = new Button(CARD_WIDTH,3,1.5,"CONFIRM");
            this.confirmButton.window = this;
            this.confirmButton.x = function() {
                return this.window.getX() + this.window.getWidth()/2 - GUI_SCALE * (CARD_WIDTH+1);
            }
            this.confirmButton.y = function() {
                return this.window.getY() + (CARD_HEIGHT+11) * GUI_SCALE;
            }
            //undo button
            this.undoButton = new Button(CARD_WIDTH,3,1.5,"UNDO");
            this.undoButton.window = this;
            this.undoButton.x = function() {
                return this.window.getX() + this.window.getWidth()/2 + GUI_SCALE;
            }
            this.undoButton.y = function() {
                return this.window.getY() + (CARD_HEIGHT+11) * GUI_SCALE;
            }

            //Create cards scroller
            this.optionsScroller = new ScrollArea(this.scrollContainer, CARD_WIDTH+1,CARD_HEIGHT+1,3,0);
            let items = [];
            let cardStack = new CardOptionItem(null, null);
            for(let optionId of Object.keys(option["options"])) {
                let cardName = option["options"][optionId];
                if(cardStack.cardName == cardName) {
                    cardStack.addId(optionId);
                }
                else {
                    cardStack = new CardOptionItem(optionId, cardName, game.allCards[cardName].image, this);
                    items.push(cardStack);
                }

            }
            this.optionsScroller.setItems(items);
            //click function
            this.clickItems = function() {
                this.optionsScroller.click();
                if(this.confirmButton.isMouseOverThis() && this.selections.length == this.nToPick) {
                    let options = [];
                    for(let selection of this.selections) options.push(selection.id);
                    game.pickOptions(options);
                    gui.popup = null;
                    game.finishedEvent();
                }
                else if(this.undoButton.isMouseOverThis() && this.selections.length > 0) {
                    for(let selection of this.selections) {
                        selection.stack.addId(selection.id);
                    }

                    this.selections.length = 0;
                }
            }

            //draw function
            this.drawItems = function() {
                let x = this.getX();
                let y = this.getY();
                //let width = this.getWidth();
                //let height = this.getHeight();
                
                //draw selected cards
                let cx = x + GUI_SCALE*4;
                let cy = y + GUI_SCALE*10;
                for(let card of this.selections) {
                    let image = card.stack.image;
                    ctx.drawImage(image, cx, cy, GUI_SCALE*CARD_WIDTH, GUI_SCALE*CARD_HEIGHT);
                    cx += GUI_SCALE*3;
                }

                //draw options box
                this.optionsScroller.draw();

                //draw overlay
                //ctx.fillStyle = "#0d3a0d";
                //ctx.fillRect(x,y+height - GUI_SCALE * (CARD_HEIGHT+2)-1, GUI_SCALE * CARD_WIDTH, GUI_SCALE * CARD_HEIGHT+2);
                //ctx.fillRect(x+width-GUI_SCALE*CARD_WIDTH,y+height - GUI_SCALE * (CARD_HEIGHT+2)-1, GUI_SCALE * CARD_WIDTH, GUI_SCALE * CARD_HEIGHT+2);

                // buttons
                this.confirmButton.drawThis(this.selections.length == this.nToPick);
                this.undoButton.drawThis(this.selections.length > 0);

            }

            //ADD SCROLL FUNCTIONS
            this.drag = function() {
                this.optionsScroller.drag();

            }
            
            this.release = function() {
                this.optionsScroller.release(true);
            }
            this.wheel = function(amount) {
                this.optionsScroller.setScrollSpeed(amount*0.07);
            }
            this.scroll = function(dt) {
                if(this.optionsScroller.scrollSpeed != 0) gui.shouldDraw = true;
                this.optionsScroller.scroll(dt);
            }
        }
        // VERTICAL SCROLL
        else {
            this.scrollContainer = new Container();
            this.scrollContainer.window = this;
            this.scrollContainer.getLeft = function() {
                return this.window.getX() + GUI_SCALE*2;
            }
            this.scrollContainer.getRight = function() {
                return canvas.width - this.window.getX();
            }
            this.scrollContainer.getTop = function() {
                return this.window.getY() + GUI_SCALE * 11;
            }
            this.scrollContainer.getBottom = function() {
                return this.window.getY() + this.window.getHeight() - GUI_SCALE*5.5;
            }

            //Create the scroller
            this.optionsScroller = new ScrollArea(this.scrollContainer,CARD_WIDTH*3,5,3,1);
            this.optionsScroller.scrollOffset = 0;
            let items = [];
            for(let optionId of Object.keys(option["options"])) {
                items.push(new OptionItem(optionId, option["options"][optionId]));
            }
            this.optionsScroller.setItems(items);

            //click function
            this.clickItems = function() {
                this.optionsScroller.click();
            }

            //draw function
            this.drawItems = function() {
                let width = this.getWidth();
                let height = this.getHeight();
                let x = this.getX();
                let y = this.getY();
                //scroll container box
                ctx.strokeStyle = "#fff";
                ctx.fillStyle = "#222";
                ctx.fillRect(this.scrollContainer.getLeft(),this.scrollContainer.getTop(),GUI_SCALE*CARD_WIDTH*3,this.scrollContainer.getHeight());
                
                //draw options box
                this.optionsScroller.draw();

                //cover up off-screen boxes
                ctx.fillStyle = "#0d3a0d";
                ctx.fillRect(x+GUI_SCALE*2-1,y+GUI_SCALE*6-1,GUI_SCALE*CARD_WIDTH*3+2,GUI_SCALE*5+2);
                ctx.fillRect(x+GUI_SCALE*2-1,y+height-GUI_SCALE*5.5-1,GUI_SCALE*CARD_WIDTH*3+2,GUI_SCALE*5+2);
            }

            //ADD SCROLL FUNCTIONS
            this.drag = function() {
                this.optionsScroller.drag();

            }
            
            this.release = function() {
                this.optionsScroller.release(true);
            }
            this.wheel = function(amount) {
                this.optionsScroller.setScrollSpeed(amount*0.07);
            }
            this.scroll = function(dt) {
                if(this.optionsScroller.scrollSpeed != 0) gui.shouldDraw = true;
                this.optionsScroller.scroll(dt);
            }
        }
    }
    getWidth() {
        return (4 * CARD_WIDTH + 7) * GUI_SCALE;
    }

    getX() {
        return (canvas.width-this.getWidth())/2;
    }

    getY() {
        return canvas.height/8;
    }

    getHeight() {
        return canvas.height * 0.75;
    }

    drawItems() {}
    clickItems() {}

    /**
     * Draw the options window with specified dimensions
     */
    draw() {
        ctx.globalAlpha = 0.8;
        ctx.fillStyle = "#000";
        ctx.fillRect(0,0,canvas.width,canvas.height);
        ctx.globalAlpha = 1;

        let width = this.getWidth();
        let height = this.getHeight();
        let x = this.getX();
        let y = this.getY();
        
        let cardWidth = GUI_SCALE*CARD_WIDTH;
        let cardHeight = GUI_SCALE*CARD_HEIGHT;

        //draw the options window
        ctx.strokeStyle = "#000";
        ctx.lineWidth = GUI_SCALE/2;
        ctx.strokeRect(x+3,y+3,width,height);
        ctx.fillStyle = "#0d3a0d";
        ctx.fillRect(x,y,width,height);

        //draw card
        ctx.drawImage(this.image,x+width-GUI_SCALE-cardWidth,y+GUI_SCALE,cardWidth,cardHeight);

        //draw cancel button
        if(this.allowCancel) {
            this.cancelButton.drawThis(true);
        }

        this.drawItems();
                
        //overlay white outline
        ctx.lineWidth = GUI_SCALE/2;
        ctx.strokeStyle = "#fff";
        ctx.strokeRect(x,y,width,height);

        //draw text
        let textY = y + GUI_SCALE * 6.5;
        let textAreaWidth = width - GUI_SCALE*(1+CARD_WIDTH);
        let textX = x + textAreaWidth/2;
        let gap = 3 * GUI_SCALE;
        ctx.font = "bold " + Math.round(GUI_SCALE*2.5) + "px Arial";
        let lines = getLines(this.optionTitle, textAreaWidth-GUI_SCALE*2);
        textY -= (lines.length-1) * gap/2;

        for(let line of lines) {
            drawText(line, textX, textY, "center", GUI_SCALE*2.5, textAreaWidth-GUI_SCALE*2);
            textY+=gap;
        }
    }

    click() {
        this.clickItems();
        if(this.allowCancel) {
            if(this.cancelButton.isMouseOverThis() || mousePosition.x < this.getX() || mousePosition.x > this.getX()+this.getWidth() || mousePosition.y < this.getY() || mousePosition.y > this.getY()+this.getHeight()) {
                game.pickOption(null);
                gui.popup = null;
                game.finishedEvent();
            }
        }
    }

    drag() {}
    release() {}
    wheel(amount) {}
    scroll(dt) {}
}