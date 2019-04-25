class AnimatedCard {
    constructor(startPosition, endPosition, time, wait, image, width, height, sound, isLastCard=false, displayWhileWaiting=false) {
        let dx = endPosition.x-startPosition.x;
        let dy = endPosition.y-startPosition.y;
        let len = Math.sqrt(dx*dx+dy*dy);
        let speed = len/time;
        this.moveVector = {
            x:speed*dx/len,
            y:speed*dy/len
        }
        this.position = {
            x:startPosition.x,
            y:startPosition.y
        }
        this.image = image;
        this.width = width;
        this.height = height;
        this.wait = wait;
        this.end = time + wait;
        this.current = 0;
        this.isLastCard = isLastCard;
        this.displayWhileWaiting = displayWhileWaiting;
        
        if(sound==undefined) this.sound = null;
        else if(sound==null) this.sound = null;
        else {
            this.sound = sound.cloneNode(true);
            this.sound.playbackRate = Math.random()/4 + 1;
        }
    }

    move(dt) {
        let start = this.current; 
        this.current += dt;
        if(start < this.wait && this.current > this.wait) {
            dt = this.current - this.wait;
        }
        if(this.current >= this.wait) {
            this.position.x += this.moveVector.x*dt;
            this.position.y += this.moveVector.y*dt;
        }
    }

    isFinished() {
        return this.current >= this.end;
    }

    playSound() {
        if(this.sound != null)
            this.sound.play();
    }
    place() {}

    draw() {
        if(this.current >= this.wait || this.displayWhileWaiting) {
            ctx.drawImage(this.image,this.position.x,this.position.y,this.width,this.height);
        }
    }
}