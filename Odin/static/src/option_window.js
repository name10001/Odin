
/**
 * Class for the options window
 */
class OptionsWindow {
    constructor(card, mousePosition) {
        this.image = card.image;
        this.optionStrings = card.optionStrings;
        this.optionIds = card.optionIds;
        this.scrollAmount = 0;
        this.mousePosition = {x:mousePosition.x,y:mousePosition.y};
        //this.mouseMove = {x:0,y:0};
        this.clickPosition = {x:0,y:0};
        this.mousePressed = false;
        this.dragging = false;
        this.hoveredItem = -1;
        this.optionBoxHeight = 20;//literally just a placeholder number until updated in draw()
    }

    /**
     * Draw the options window with specified dimensions
     */
    draw(ctx, x, y, width, height) {
        let fontSize = Math.round(width/20);
        let cardWidth = width/4;
        let cardHeight = cardWidth / CARD_RATIO;
        let gap = cardWidth/8;
        let optionsWidth = width-cardWidth-gap*2;

        //draw the options window
        ctx.fillStyle = "#999";
        ctx.strokeStyle = "#fff";
        ctx.fillRect(x,y,width,height);
        ctx.strokeRect(x,y,width,height);

        //draw card
        ctx.drawImage(this.image,x+width-gap-cardWidth,y+gap,cardWidth,cardHeight);

        //draw text
        ctx.textAlign = "center";
        ctx.fillStyle = "#fff";
        ctx.font = "bold " + fontSize + "px Courier New";
        ctx.fillText("Choose option:",x + optionsWidth/2,y+fontSize*2);

        //draw options box
        ctx.fillStyle = "#222";
        ctx.strokeStyle = "#fff";
        let optionBoxesHeight = height-gap-fontSize*3;
        let optionBoxWidth = optionsWidth-gap*2;
        ctx.fillRect(x+gap,y+fontSize*3,optionBoxWidth,optionBoxesHeight);
        ctx.strokeRect(x+gap,y+fontSize*3,optionBoxWidth,optionBoxesHeight);

        //draw all options
        ctx.textAlign = "left";
        let nOptions = Math.round(0.5*optionBoxesHeight/fontSize);
        this.optionBoxHeight = optionBoxesHeight/nOptions;
        let y2 = y+fontSize*3;
        let i = this.scrollAmount;

        //calculate the item that you are hovered over
        if(this.mousePosition.x<x+gap || this.mousePosition.x>x+gap+optionBoxWidth) this.hoveredItem = -1;
        else if(!this.dragging && (this.mousePosition.y<y2 || this.mousePosition.y>y2+optionBoxesHeight)) this.hoveredItem = -1;
        else {
            let dy = this.mousePosition.y-y2;
            this.hoveredItem = this.scrollAmount+Math.floor(dy/this.optionBoxHeight);
            if(this.hoveredItem>=this.optionIds.length) this.hoveredItem = -1;//clicked blank space in option window
        }

        while(i<this.optionIds.length && i<this.scrollAmount+nOptions) {
            ctx.fillStyle = "#376";
            ctx.fillRect(x+gap,y2,optionBoxWidth,this.optionBoxHeight);
            ctx.strokeStyle = (this.hoveredItem==i && !this.dragging) ? "#ffa" : "#fff";
            ctx.strokeRect(x+gap,y2,optionBoxWidth,this.optionBoxHeight);

            //draw the text
            ctx.fillStyle = ctx.strokeStyle;
            ctx.fillText(this.optionStrings[i],x+gap+fontSize,y2+fontSize*1.25);

            i++;
            y2+=this.optionBoxHeight;
        }
    }

    click(x,y) {
        this.clickPosition.x = x;
        this.clickPosition.y = y;
        this.mousePosition.x = x;
        this.mousePosition.y = y;
        this.mousePressed = true;
        this.dragging = false;
    }

    drag(x,y) {
        this.mousePosition.x = x;
        this.mousePosition.y = y;
        if(this.mousePressed) {
            if(Math.abs(this.clickPosition.x-this.mousePosition.x)>10 || Math.abs(this.clickPosition.y-this.mousePosition.y)>10) this.dragging = true;
            
            if(this.dragging) {
                if(this.mousePosition.y-this.clickPosition.y>this.optionBoxHeight) {
                    this.clickPosition.y+=this.optionBoxHeight;
                    this.scrollUp();
                }
                else if(this.mousePosition.y-this.clickPosition.y<-this.optionBoxHeight) {
                    this.clickPosition.y-=this.optionBoxHeight;
                    this.scrollDown();
                }
            }
        }

    }
    
    release(touch) {
        if(touch) {
            this.mousePosition.x = 0;
            this.mousePosition.y = 0;
        }
        if(this.hoveredItem!=-1) {
            //picked an option
            let pickedOption = this.optionIds[this.hoveredItem];
            GAME_CANVAS.exitOptions(pickedOption);
            return;
        }
        this.mousePressed = false;
        this.dragging = false;
    }
    wheel(amount) {
        if(amount>0) this.scrollDown();
        else this.scrollUp();
    }

    scrollDown() {
        this.scrollAmount ++;
        if(this.scrollAmount > this.optionIds.length-1) this.scrollAmount = this.optionIds.length-1;
    }
    scrollUp() {
        this.scrollAmount --;
        if(this.scrollAmount<0) this.scrollAmount = 0;
    }
}

