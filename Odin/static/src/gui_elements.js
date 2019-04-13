class Button {
    constructor(width, height, fontSize, text) {
        this.width = width;
        this.height = height;
        this.fontSize = fontSize;
        this.text = text;
    }

    x() {return 0;}
    y() {return 0;}

    isMouseOver(x, y) {
        return mousePosition.x>x && mousePosition.x<x+this.width * GUI_SCALE &&
            mousePosition.y>y && mousePosition.y<y+this.height * GUI_SCALE;
    }
    isMouseOverThis() {
        return mousePosition.x>this.x() && mousePosition.x<this.x()+this.width * GUI_SCALE &&
            mousePosition.y>this.y() && mousePosition.y<this.y()+this.height * GUI_SCALE;
    }
    drawThis(canPress) {
        this.draw(this.x(),this.y(),canPress);
    }

    draw(x, y, canPress) {
        let hover = this.isMouseOver(x, y);
        let fontSize = this.fontSize * GUI_SCALE;
        //draw the next turn button
        ctx.fillStyle = canPress ? "#376" : "#999";
        ctx.strokeStyle = canPress ? (hover ? "#ffa" : "#fff") : "#fff";
        ctx.fillRect(x,y,this.width * GUI_SCALE,this.height * GUI_SCALE);
        ctx.strokeRect(x,y,this.width * GUI_SCALE,this.height * GUI_SCALE);
        ctx.fillStyle = canPress ? (hover ? "#ffa" : "#fff") : "#bbb";
        ctx.textAlign = "center";
        ctx.font = "bold " + fontSize + "px Courier New";
        ctx.fillText(this.text,x+this.width*GUI_SCALE/2,y+this.height*GUI_SCALE/2+fontSize/3);
    }
}

/**
 * Container class.
 * By default this just represents the canvas
 */
class Container {
    getLeft() { return 0;}
    getRight() {return canvas.width;}
    getTop() {return 0;}
    getBottom() {return canvas.height;}
    getWidth() {return canvas.width;}
    getHeight() {return canvas.height;}
}

class CardStackPanel {
    constructor(cardStack) {
        this.cardStack = cardStack;
        this.playButton = new Button(CARD_WIDTH-1,3,1.5,"Add");
        this.playallButton = new Button(CARD_WIDTH-1,3,1.5,"Add All");
    }

    draw(x,y,width,height) {

        let stackSize = this.cardStack.size();
        if(stackSize>=100) stackSize = 99;//if you have >=100 of one type, just say 99

        //draw card
        ctx.drawImage(this.cardStack.image,
            x+GUI_SCALE/2, y+GUI_SCALE/2,
            GUI_SCALE*CARD_WIDTH, GUI_SCALE*CARD_HEIGHT);
        
        this.playButton.draw(x+GUI_SCALE, y + (CARD_HEIGHT+1.5)*GUI_SCALE,this.cardStack.allowedToPlay);
        this.playallButton.draw(x+GUI_SCALE, y + (CARD_HEIGHT+5.5)*GUI_SCALE,this.cardStack.allowedToPlay);
        //draw stack size
        if(stackSize>1) {
            ctx.font = "bold " + (GUI_SCALE*2) + "px Courier New";
            ctx.textAlign = "left";
            ctx.fillStyle = "#fff";
            ctx.fillRect(x+GUI_SCALE/2, y+GUI_SCALE*CARD_HEIGHT-GUI_SCALE*2,GUI_SCALE*5,GUI_SCALE*2.5);
            ctx.fillStyle = "#000";
            
            ctx.fillText("x" + stackSize, x+GUI_SCALE, y+GUI_SCALE*CARD_HEIGHT);
            
        }

        //draw transparent overlay if you aren't allowed to play
        if(!this.cardStack.allowedToPlay) {
            ctx.drawImage(gui.transparentImage,
                x+GUI_SCALE/2, y+GUI_SCALE/2,
                GUI_SCALE*CARD_WIDTH, GUI_SCALE*CARD_HEIGHT);
        }

        //this.helpButton.draw(x+GUI_SCALE*(CARD_WIDTH-2.5),y+GUI_SCALE/2,true);

    }

    click(x,y) {

        //clicked the card
        if(x > GUI_SCALE/2 && x<GUI_SCALE*CARD_WIDTH+GUI_SCALE/2 &&
                y > GUI_SCALE/2 && y<GUI_SCALE*CARD_HEIGHT+GUI_SCALE/2) {
            console.log("info");
        }
        //clicked the play button
        else if(x > GUI_SCALE && x<GUI_SCALE*CARD_WIDTH &&
            y > GUI_SCALE*(CARD_HEIGHT+1.5) && y<GUI_SCALE*(CARD_HEIGHT+4.5)) {
            this.play();
        }
        //clicked the play all button
        else if(x > GUI_SCALE && x<GUI_SCALE*CARD_WIDTH &&
            y > GUI_SCALE*(CARD_HEIGHT+5.5) && y<GUI_SCALE*(CARD_HEIGHT+8.5)) {
            this.playAll();
        }
    }

    play() {
        if(!this.cardStack.allowedToPlay) return;

        if(this.cardStack.optionIds.length>0) {
            gui.optionsWindow = new OptionsWindow(this.cardStack);
        }
        else {
            this.cardStack.playSingle();
        }
    }

    playAll() {
        if(!this.cardStack.allowedToPlay) return;

        if(this.cardStack.optionIds.length>0) {
            gui.optionsWindow = new OptionsWindow(this.cardStack);
            gui.playAll = true;
        }
        else {
            this.cardStack.playAll();
        }
    }
}


/**
 * Arbitrary scroll area that sticks to the bottom of a given container
 */
class ScrollArea {
    /**
     * Create new scroll area
     * @param {Container} container container with a set width and height
     * @param {float} itemWidth width of each item in GUI_SCALE units
     * @param {float} itemHeight height of each item in GUI_SCALE units
     */
    constructor(container, itemWidth, itemHeight, scrollbarHeight) {
        this.container = container;
        this.itemWidth = itemWidth;
        this.itemHeight = itemHeight;
        this.scrollbarHeight = scrollbarHeight;
        this.location = location;

        this.scrollOffset = 0.5;//offset from 0 to 1.
        this.scrollSpeed = 0;

        this.items = [];//init with nothing

        this.clickPosition = {x:0,y:0};
        this.dragging = false;
        this.scrolling = false;

        this.clickScrollOffset = this.scrollOffset;
    }

    /**
     * Set the item list
     * @param {Object[]} list of items that can be drawn (must contain draw(x,y,width,height) method)
     */
    setItems(items) {
        this.items = items;
    }

    /**
     * Draw the scroll area
     */
    draw() {
        let numItems = this.items.length;
        if(numItems<1) return;

        //get dimensions of items
        let width = this.itemWidth * GUI_SCALE;
        let height = this.itemHeight * GUI_SCALE;

        let x = this.container.getLeft();
        let y = this.container.getBottom() - height;

        //scroll area
        let minScroll = this.getMinScroll();
        let maxScroll = this.getMaxScroll();
        let totalWidth = maxScroll - minScroll;

        //draw items from left to right
        let start = minScroll + this.scrollOffset * totalWidth;
        x-=start;
        for(let item of this.items) {
            item.draw(x,y,width,height);
            x+=width;
        }

        //draw the scrollbar
        if(this.scrollbarHeight > 0) {
            let scrollY = this.container.getBottom() - height - GUI_SCALE*this.scrollbarHeight/2;
            let scrollX = this.scrollOffset*(this.container.getWidth()-GUI_SCALE*2);
            ctx.strokeStyle = "#ddd";
            ctx.fillStyle = "#999";
            ctx.beginPath();
            ctx.moveTo(this.container.getLeft()+GUI_SCALE,scrollY);
            ctx.lineTo(this.container.getRight()-GUI_SCALE,scrollY);
            ctx.stroke();
            ctx.fillRect(scrollX-width/2,scrollY-GUI_SCALE,width,GUI_SCALE*2);
            ctx.strokeRect(scrollX-width/2,scrollY-GUI_SCALE,width,GUI_SCALE*2);
        }
    }

    getMinScroll() {
        return -this.container.getWidth()*0.75;
    }
    getMaxScroll() {
        return this.items.length * this.itemWidth * GUI_SCALE - this.container.getWidth()*0.25;
    }
    getTotalWidth() {
        return this.getMaxScroll() - this.getMinScroll();
    }

    /**
     * Update scroll
     * @param {float} dt 
     */
    scroll(dt) {
        let numItems = this.items.length;
        if(numItems<1) return;
        //accelerate based on your dragging speed
        if(this.scrollSpeed > 0) {
            this.scrollSpeed-=dt*0.004/numItems;
            if(this.scrollSpeed<0) this.scrollSpeed = 0;
        }
        else if(this.scrollSpeed < 0) {
            this.scrollSpeed+=dt*0.004/numItems;
            if(this.scrollSpeed>0) this.scrollSpeed = 0;
        }

        this.scrollOffset+=this.scrollSpeed;
        if(this.scrollOffset<0) this.scrollOffset = 0;
        else if(this.scrollOffset>1) this.scrollOffset = 1;
    }

    /**
     * Set the scroll speed
     */
    setScrollSpeed(amount) {
        let numItems = this.items.length;
        if(numItems<1) return;

        this.scrollSpeed = amount / numItems;
    }

    click() {
        let height = this.itemHeight * GUI_SCALE;
        //check if within bounds of the scroll area
        if(mousePosition.x>this.container.getLeft() && mousePosition.x<this.container.getRight() &&
                    mousePosition.y<this.container.getBottom() && mousePosition.y>this.container.getBottom()-height) {
            this.clickPosition.x = mousePosition.x-this.container.getLeft();
            this.clickPosition.y = mousePosition.y-this.container.getBottom()+height;
            this.clickScrollOffset = this.scrollOffset;
            this.dragging = false;
        }
        //check if in bounds of scrollbar
        else if(mousePosition.x>this.container.getLeft() && mousePosition.x<this.container.getRight() &&
                    mousePosition.y>this.container.getBottom()-height-this.scrollbarHeight*GUI_SCALE && mousePosition.y<this.container.getBottom()-height) {
            this.scrolling = true;
        }
    }

    drag() {
        if(this.clickPosition.x>0 || this.clickPosition.y > 0) {
            let dx = mousePosition.x-this.container.getLeft()-this.clickPosition.x;
            
            if(Math.abs(dx) > 10) {
                this.dragging = true;
            }

            //scroll by dragging
            if(this.dragging) {
                let totalWidth = this.getTotalWidth();

                let offset = totalWidth*this.clickScrollOffset;
                offset-=dx;

                this.scrollOffset = offset/totalWidth;
            }
        }
        //scrollbar
        else if(this.scrolling) {
            let offsetX = mousePosition.x-this.container.getLeft();
            this.scrollOffset = offsetX / (this.container.getWidth()-GUI_SCALE*2);
        }
    }

    release() {
        if(this.clickPosition.x>0 || this.clickPosition.y > 0) {
            let height = this.itemHeight * GUI_SCALE;
            let x = mousePosition.x-this.container.getLeft();
            let y = mousePosition.y-this.container.getBottom()+height;
            if(!this.dragging) {
                let offset = this.getTotalWidth() * this.scrollOffset + this.getMinScroll();
                let offsetX = x + offset;
                let width = this.itemWidth * GUI_SCALE;

                if(offsetX>0) {
                    let index = Math.floor(offsetX/width);
                    //click
                    if(index < this.items.length) {
                        this.items[index].click(offsetX - index * width, y);
                    }
                }
            }
        }

        this.clickPosition.x = 0;
        this.clickPosition.y = 0;
        this.scrolling = false;
        this.dragging = false;
    }
}