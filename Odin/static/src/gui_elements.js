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

    draw(ctx, fontSize, mousePosition, canPress) {
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
