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

    draw(ctx, fontSize, canPress) {
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
    }

    draw(x,y,width,height) {

        ctx.font = "bold " + (GUI_SCALE*2) + "px Courier New";
        ctx.textAlign = "left";

        let stackSize = this.cardStack.size();
        if(stackSize>=100) stackSize = 99;//if you have >=100 of one type, just say 99

        ctx.drawImage(this.cardStack.image,
            x+GUI_SCALE/2, y+GUI_SCALE/2,
            GUI_SCALE*CARD_WIDTH, GUI_SCALE*CARD_HEIGHT);
        
        if(!this.cardStack.allowedToPlay) {
            ctx.drawImage(gui.transparentImage,
                x+GUI_SCALE/2, y+GUI_SCALE/2,
                GUI_SCALE*CARD_WIDTH, GUI_SCALE*CARD_HEIGHT);
        }
        
        if(stackSize>1) {
            ctx.fillStyle = "#fff";
            ctx.fillRect(x+GUI_SCALE/2, y+GUI_SCALE*CARD_HEIGHT-GUI_SCALE*2,GUI_SCALE*5,GUI_SCALE*2.5);
            ctx.fillStyle = "#000";
            
            ctx.fillText("x" + stackSize, x+GUI_SCALE, y+GUI_SCALE*CARD_HEIGHT);
        }
    }

    click(x,y) {
        //clicked the card
        if(x > GUI_SCALE/2 && x<GUI_SCALE*CARD_WIDTH+GUI_SCALE/2 &&
            y > GUI_SCALE/2 && y<GUI_SCALE*CARD_HEIGHT+GUI_SCALE/2) {
            this.play();
        }

        //clicked the buttons? TODO here

    }

    play() {
        if(this.cardStack.optionIds.length>0) {
            gui.optionsWindow = new OptionsWindow(this.cardStack);
        }
        else {
            this.cardStack.playSingle();
        }
    }

    playAll() {
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
    constructor(container, itemWidth, itemHeight) {
        this.container = container;
        this.itemWidth = itemWidth;
        this.itemHeight = itemHeight;
        this.location = location;

        this.scrollOffset = 0.5;//offset from 0 to 1.
        this.scrollSpeed = 0;

        this.items = [];//init with nothing

        this.clickPosition = {x:0,y:0};
        this.dragging = false;

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
        //accelerate based on your dragging speed
        if(this.scrollSpeed > 0) {
            this.scrollSpeed-=dt*0.0001;
            if(this.scrollSpeed<0) this.scrollSpeed = 0;
        }
        else if(this.scrollSpeed < 0) {
            this.scrollSpeed+=dt*0.0001;
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
        this.dragging = false;
    }
}