function drawText(text, x, y, textAlign, fontSize, maxWidth, colour) {
    if(colour == undefined) {
        colour = "#fff";
    }
    ctx.font = "bold italic " + Math.round(fontSize) + "px Arial";
    ctx.textAlign = textAlign;
    ctx.fillStyle = colour;
    ctx.fillText(text,Math.floor(x),Math.floor(y),maxWidth);
}

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
        //draw the next turn button
        ctx.fillStyle = canPress ? "#27ab25" : "#999";
        ctx.strokeStyle = canPress ? (hover ? "#ffa" : "#fff") : "#ececec";
        ctx.lineWidth = this.height*GUI_SCALE*0.1;
        ctx.fillRect(x,y,this.width * GUI_SCALE,this.height * GUI_SCALE);
        ctx.strokeRect(x,y,this.width * GUI_SCALE,this.height * GUI_SCALE);
        drawText(this.text,x+this.width*GUI_SCALE/2,y+this.height*GUI_SCALE/2+GUI_SCALE*this.fontSize*0.38,"center",
                this.fontSize*GUI_SCALE,this.width*GUI_SCALE-GUI_SCALE*this.fontSize, ctx.strokeStyle);
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
    getWidth() {return this.getRight()-this.getLeft();}
    getHeight() {return this.getBottom()-this.getTop();}
}

class CardStackPanel {
    constructor(cardStack) {
        this.cardStack = cardStack;
        this.helpButton = new Button(3,3,1.5,"?");
        this.playallButton = new Button(CARD_WIDTH-4.5,3,1.5,"+ALL");
    }

    draw(x,y,allowClick) {
        let stackSize = this.cardStack.size();

        this.helpButton.draw(x+GUI_SCALE, y + (CARD_HEIGHT+1.5)*GUI_SCALE, true);
        this.playallButton.draw(x+GUI_SCALE*4.5, y + (CARD_HEIGHT+1.5)*GUI_SCALE, 
            this.cardStack.allowedToPlay && allowClick);

        if(stackSize == 0) return;
        //draw card
        ctx.drawImage(this.cardStack.image,
            x+GUI_SCALE/2, y+GUI_SCALE/2,
            GUI_SCALE*CARD_WIDTH, GUI_SCALE*CARD_HEIGHT);
        
        //draw stack size
        if(stackSize>1) {
            ctx.fillStyle = "#fff";
            ctx.fillRect(x+GUI_SCALE/2, y+GUI_SCALE*CARD_HEIGHT-GUI_SCALE*2,GUI_SCALE*5,GUI_SCALE*2.5);
            drawText("x" + stackSize, x+GUI_SCALE, y + GUI_SCALE*CARD_HEIGHT, "left", GUI_SCALE * 2, GUI_SCALE*4, "#000");
        }

        //draw transparent overlay if you aren't allowed to play
        if(!this.cardStack.allowedToPlay || !allowClick) {
            ctx.drawImage(gui.transparentImage,
                x+GUI_SCALE/2, y+GUI_SCALE/2,
                GUI_SCALE*CARD_WIDTH, GUI_SCALE*CARD_HEIGHT);
        }
    }

    click(x,y) {
        let cardX = mousePosition.x - x + GUI_SCALE/2;
        let cardY = mousePosition.y - y + GUI_SCALE/2;
        //clicked the card
        if(x > GUI_SCALE/2 && x<GUI_SCALE*CARD_WIDTH+GUI_SCALE/2 &&
                y > GUI_SCALE/2 && y<GUI_SCALE*CARD_HEIGHT+GUI_SCALE/2) {
            if(this.cardStack.allowedToPlay) this.cardStack.playSingle();
            
        }
        //clicked the help button
        else if(x > GUI_SCALE && x<GUI_SCALE*4 &&
            y > GUI_SCALE*(CARD_HEIGHT+1.5) && y<GUI_SCALE*(CARD_HEIGHT+4.5)) {
            gui.popup = new DescriptionWindow(this.cardStack);
        }
        //clicked the play all button
        else if(x > GUI_SCALE*4.5 && x<GUI_SCALE*CARD_WIDTH &&
            y > GUI_SCALE*(CARD_HEIGHT+1.5) && y<GUI_SCALE*(CARD_HEIGHT+4.5) && !this.cardStack.pickOptionsSeparately) {
                if(this.cardStack.allowedToPlay) this.cardStack.playAll();
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
     * @param {integer} location 0 = bottom, 1 = left
     */
    constructor(container, itemWidth, itemHeight, scrollbarSize, location) {
        this.container = container;
        this.itemWidth = itemWidth;
        this.itemHeight = itemHeight;
        this.scrollbarSize = scrollbarSize;
        this.location = location;

        this.scrollOffset = 0.5;//offset from 0 to 1.
        this.scrollSpeed = 0;
        this.dragTime = 0;
        this.clickOffset = 0;

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
    draw(allowClick=true) {
        let numItems = this.items.length;
        if(numItems<1) return;

        //get dimensions of items
        let width = this.itemWidth * GUI_SCALE;
        let height = this.itemHeight * GUI_SCALE;

        let x = this.container.getLeft();
        let y = this.location==0 ? this.container.getBottom() - height : this.container.getTop();

        //scroll area
        let minScroll = this.getMinScroll();
        let maxScroll = this.getMaxScroll();
        let totalWidth = maxScroll - minScroll;

        //draw items from left to right
        let start = minScroll + this.scrollOffset * totalWidth;
        
        if(this.location == 0) {
            x-=start;
            for(let item of this.items) {
                if(x>this.container.getRight()) break;
                if(x+width>this.container.getLeft()) item.draw(x,y,allowClick);
                x+=width;
            }
        }
        else {
            y-=start;
            for(let item of this.items) {
                if(y>this.container.getBottom()) break;
                if(y+height>this.container.getTop()) item.draw(x,y,allowClick);
                y+=height;
            }
        }
        //draw the scrollbar
        if(this.scrollbarSize > 0) {

            ctx.strokeStyle = "#ddd";
            ctx.fillStyle = "#999";
            ctx.lineWidth = 1;
            if(this.location == 0) {
                let scrollY = this.container.getBottom() - height - GUI_SCALE*this.scrollbarSize/2;
                let scrollX = this.container.getLeft() + this.scrollOffset*(this.container.getWidth()-GUI_SCALE*2);
                ctx.beginPath();
                ctx.moveTo(this.container.getLeft()+GUI_SCALE,scrollY);
                ctx.lineTo(this.container.getRight()-GUI_SCALE,scrollY);
                ctx.stroke();
                ctx.fillRect(scrollX-width/2,scrollY-GUI_SCALE,width,GUI_SCALE*2);
                ctx.strokeRect(scrollX-width/2,scrollY-GUI_SCALE,width,GUI_SCALE*2);

            }
            else {
                let scrollX = this.container.getLeft() + width + GUI_SCALE*this.scrollbarSize/2;
                let scrollY = this.container.getTop()+this.scrollOffset*(this.container.getHeight()-GUI_SCALE*2);
                ctx.beginPath();
                ctx.moveTo(scrollX,this.container.getTop()+GUI_SCALE);
                ctx.lineTo(scrollX,this.container.getBottom()-GUI_SCALE);
                ctx.stroke();
                ctx.fillRect(scrollX-GUI_SCALE,scrollY-height/2,GUI_SCALE*2,height);
                ctx.strokeRect(scrollX-GUI_SCALE,scrollY-height/2,GUI_SCALE*2,height);
            }
        }
    }

    getMinScroll() {
        if(this.location==0) {
            return -this.container.getWidth()*0.75;
        }
        else {
            return 0;
        }
    }
    getMaxScroll() {
        if(this.location == 0) {
            return this.items.length * this.itemWidth * GUI_SCALE - this.container.getWidth()*0.25;
        }
        else {
            return (this.items.length-1) * this.itemHeight * GUI_SCALE;
        }
    }
    getTotalWidth() {
        return this.getMaxScroll() - this.getMinScroll();
    }

    getPositionOf(index) {
        let width = this.itemWidth * GUI_SCALE;
        let height = this.itemHeight * GUI_SCALE;

        let x = this.container.getLeft();
        let y = this.location==0 ? this.container.getBottom() - height : this.container.getTop();
        let minScroll = this.getMinScroll();
        let maxScroll = this.getMaxScroll();
        let totalWidth = maxScroll - minScroll;
        let start = minScroll + this.scrollOffset * totalWidth;
        
        if(this.location == 0) {
            x -= start;
            x += width * index;
        }
        else {
            y -= start;
            y += height * index;
        }

        return {x, y};
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
            this.scrollSpeed-=dt*0.0006/numItems;
            if(this.scrollSpeed<0) this.scrollSpeed = 0;
        }
        else if(this.scrollSpeed < 0) {
            this.scrollSpeed+=dt*0.0006/numItems;
            if(this.scrollSpeed>0) this.scrollSpeed = 0;
        }
        if(this.dragging) this.dragTime += dt;
        this.scrollOffset+=this.scrollSpeed*dt;
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
        let left = this.container.getLeft();
        let bottom = this.container.getBottom();
        let right = this.location==0 ? this.container.getRight() : this.container.getLeft() + this.itemWidth * GUI_SCALE;
        let top = this.location==0 ? this.container.getBottom() - this.itemHeight * GUI_SCALE : this.container.getTop();
        
        //check if within bounds of the scroll area
        if(mousePosition.x>left && mousePosition.x<right &&
                    mousePosition.y<bottom && mousePosition.y>top) {
            this.clickPosition.x = mousePosition.x-left;
            this.clickPosition.y = mousePosition.y-top;
            this.clickScrollOffset = this.scrollOffset;
            this.dragging = false;
        }
        //check if in bounds of scrollbar
        else {
            
            if(this.location==0) {
                bottom = top;
                top -= this.scrollbarSize * GUI_SCALE;
                left -= this.itemWidth*GUI_SCALE;
                right += this.itemWidth*GUI_SCALE;
            }
            else {
                left = right;
                right += this.scrollbarSize * GUI_SCALE;
                top -= this.itemHeight*GUI_SCALE;
                bottom += this.itemHeight*GUI_SCALE;
            }
            if(mousePosition.x>left && mousePosition.x<right &&
                mousePosition.y<bottom && mousePosition.y>top) {
                this.scrolling = true;
                if(this.location == 0) {
                    let offsetX = mousePosition.x-this.container.getLeft();
                    let scrollOffset = offsetX / (this.container.getWidth()-GUI_SCALE*2);
                    this.clickOffset = this.scrollOffset - scrollOffset;
                }else {
                    let offsetY = mousePosition.y-this.container.getTop();
                    let scrollOffset = offsetY / (this.container.getHeight()-GUI_SCALE*2);
                    this.clickOffset = this.scrollOffset - scrollOffset;
                }
            }
        }
    }

    drag() {
        if(this.clickPosition.x>0 || this.clickPosition.y > 0) {
            let dx = this.location == 0 ? mousePosition.x-this.container.getLeft()-this.clickPosition.x :
                    mousePosition.y-this.container.getTop()-this.clickPosition.y;
            
            if(Math.abs(dx) > 10 && !this.dragging) {
                this.dragging = true;
                this.dragTime = 0;
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
            if(this.location == 0) {
                let offsetX = mousePosition.x-this.container.getLeft();
                this.scrollOffset = this.clickOffset + offsetX / (this.container.getWidth()-GUI_SCALE*2);
            }else {
                let offsetY = mousePosition.y-this.container.getTop();
                this.scrollOffset = this.clickOffset + offsetY / (this.container.getHeight()-GUI_SCALE*2);
            }
        }
    }

    release(allowClick) {
        if(this.clickPosition.x>0 || this.clickPosition.y > 0) {
            let height = this.itemHeight * GUI_SCALE;
            let x = mousePosition.x-this.container.getLeft();
            let y = this.location==0 ? mousePosition.y-this.container.getBottom()+height : mousePosition.y-this.container.getTop();

            //click on the item (only if allowed and not dragging)
            if(!this.dragging && allowClick) {
                let offset = this.getTotalWidth() * this.scrollOffset + this.getMinScroll();
                let offsetX = this.location==0 ? x + offset : y + offset;
                let width = this.location==0 ? this.itemWidth * GUI_SCALE : this.itemHeight * GUI_SCALE;

                if(offsetX>0) {
                    let index = Math.floor(offsetX/width);
                    //click
                    if(index < this.items.length) {
                        if(this.location==0) {
                            this.items[index].click(offsetX - index * width, y);
                        }else {
                            this.items[index].click(x, offsetX - index * width);
                        }
                    }
                }
            }

            //scrolling speed when release
            if(this.dragging && this.dragTime > 0 && this.items.length > 0) {
                let dx = this.location == 0 ?  x - this.clickPosition.x : y - this.clickPosition.y;
                let dt = this.dragTime;
                let dxdt = dx/dt;
                this.scrollSpeed = -4.0*dxdt/(this.items.length*GUI_SCALE*(this.location==0 ? this.itemWidth : this.itemHeight));
            }
        }

        this.clickPosition.x = 0;
        this.clickPosition.y = 0;
        this.scrolling = false;
        this.dragging = false;
    }
}