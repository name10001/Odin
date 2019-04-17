class OptionItem {
    constructor(card, optionId, optionString) {
        this.card = card;
        this.optionId = optionId;
        this.button = new Button(CARD_WIDTH*2-0.3,2.7,1.5,optionString);
    }

    draw(x,y,width,height) {
        this.button.draw(x+GUI_SCALE*0.15,y+GUI_SCALE*0.15,true);
    }

    click(x,y) {
        gui.exitOptions(this.card, this.optionId);
    }

}


/**
 * Class for the options window
 */
class OptionsWindow {
    constructor(card) {
        this.card = card;
        this.image = card.image;

        //Create the scroll container
        this.scrollContainer = new Container();
        this.scrollContainer.window = this;
        this.scrollContainer.getLeft = function() {
            return this.window.getX() + GUI_SCALE*2;
        }
        this.scrollContainer.getRight = function() {
            return canvas.width - this.window.getX();
        }
        this.scrollContainer.getTop = function() {
            return canvas.height*0.25 + GUI_SCALE * 5;
        }
        this.scrollContainer.getBottom = function() {
            return canvas.height*0.75 - GUI_SCALE*3.5;
        }

        //Create the scroller
        this.optionsScroller = new ScrollArea(this.scrollContainer,CARD_WIDTH*2,3,3,1);
        this.optionsScroller.scrollOffset = 0;
        let items = [];
        for(let i = 0;i<card.optionIds.length;i++) {
            let id = card.optionIds[i];
            let text = card.optionStrings[i];
            
            items.push(new OptionItem(card,id,text));
        }
        this.optionsScroller.setItems(items);

        //create a cancel button
        this.cancelButton = new Button(CARD_WIDTH,3,1.5,"CANCEL");
        this.cancelButton.x = function() {
            return canvas.width/2 + (0.5*CARD_WIDTH+2.5) * GUI_SCALE;
        }
        this.cancelButton.y = function() {
            return canvas.height/4 + (CARD_HEIGHT+2) * GUI_SCALE;
        }
    }
    getWidth() {
        return (3 * CARD_WIDTH + 7) * GUI_SCALE;
    }

    getX() {
        return (canvas.width-this.getWidth())/2;
    }

    getY() {
        return canvas.height/4;
    }

    /**
     * Draw the options window with specified dimensions
     */
    draw() {
        let width = this.getWidth();
        let height = canvas.height/2;
        let x = this.getX();
        let y = this.getY();

        let fontSize = GUI_SCALE*2;
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
        this.cancelButton.drawThis(true);
        
        ctx.strokeStyle = "#fff";
        ctx.fillStyle = "#222";
        ctx.fillRect(this.scrollContainer.getLeft(),this.scrollContainer.getTop(),GUI_SCALE*CARD_WIDTH*2,this.scrollContainer.getHeight());
        
        //draw options box
        this.optionsScroller.draw();

        ctx.fillStyle = "#0d3a0d";
        ctx.strokeStyle = "#fff";
        ctx.fillRect(x+GUI_SCALE*2-1,y+GUI_SCALE*2-1,GUI_SCALE*CARD_WIDTH*2+2,GUI_SCALE*3+2);
        ctx.fillRect(x+GUI_SCALE*2-1,y+height-GUI_SCALE*3.5-1,GUI_SCALE*CARD_WIDTH*2+2,GUI_SCALE*3+2);
        
        //ctx.lineWidth = GUI_SCALE/4;
        //ctx.strokeRect(this.scrollContainer.getLeft(),this.scrollContainer.getTop(),GUI_SCALE*CARD_WIDTH*2,this.scrollContainer.getHeight());
        
        
        ctx.lineWidth = GUI_SCALE/2;
        ctx.strokeStyle = "#fff";
        ctx.strokeRect(x,y,width,height);

        //draw text
        drawText("Choose option",x + GUI_SCALE*(CARD_WIDTH+2),y+GUI_SCALE*3,"center",GUI_SCALE*2,undefined,true);
    }

    click() {
        this.optionsScroller.click();
        if(this.cancelButton.isMouseOverThis()) {
            gui.exitOptions(null,null);
        }
    }

    drag() {
        this.optionsScroller.drag();

    }
    
    release() {
        this.optionsScroller.release();
    }
    wheel(amount) {
        this.optionsScroller.setScrollSpeed(amount*0.07);
    }
    scroll(dt) {
        this.optionsScroller.scroll(dt);
    }
}

