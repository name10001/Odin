class AnimatedCard {
    constructor(startPosition, endPosition, time, wait, image, width, height, sound, displayWhileWaiting=false) {
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
        if(start <= this.wait && this.current > this.wait) {
            dt = this.current - this.wait;
            this.release();
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

    release() {}
    place() {}

    draw() {
        if(this.current >= this.wait || this.displayWhileWaiting) {
            ctx.drawImage(this.image,this.position.x,this.position.y,this.width,this.height);
        }
    }
}

class CommunistAnimation {
    constructor(yourCards) {
        this.yourCards = yourCards;
        let song = new Audio('/static/sounds/communist_card.mp3');
        song.play();
        
        this.timeElapsed = 0;
        this.timeUntilDone = 13000;
        this.ourCards = this.yourCards.length * game.players.length;
        this.removedCards = false;

        //When the counts should start going down
        this.playerCountDownStart = [];
        this.playerCountUpStart = [];

        //THE BECOMING OF OUR CARDS
        let pwidth = CARD_WIDTH * 3 * GUI_SCALE;
        let pheight = GUI_SCALE * 3;
        let pgap = GUI_SCALE;
        let ourWidth = CARD_WIDTH * 4 * GUI_SCALE;
        let ourHeight = ourWidth/2 + GUI_SCALE;
        let totalHeight = game.players.length * pheight + (game.players.length - 1) * pgap + ourHeight;

        let x = canvas.width/2 - ourWidth/2;
        let y = canvas.height/2 - totalHeight/2;
        let px = canvas.width/2 - pwidth/2;
        let py = y + ourHeight;


        let wait = 3200;
        this.playerIncr = gui.getCardWaitIncrement(game.players.length, 6000);
        let soundDisplacement = gui.MIN_SOUND_DISPLACEMENT;

        let cardDimensions = {width:CARD_WIDTH*GUI_SCALE/2, height:CARD_HEIGHT*GUI_SCALE/2};
        let endPosition = {x:x+ourWidth * 0.75-cardDimensions.width/2, y:y+ourWidth/4-cardDimensions.height/2};

        this.countStart = wait + 400;

        px += GUI_SCALE*10;
        py -= (cardDimensions.height - pheight)/2;
        for(let player of game.players) {
            let nCards = player.nCards;
            let cardIncr = this.playerIncr/nCards;
            this.playerCountDownStart.push(wait);
            for(let i = 0; i < nCards; i++) {
                let movingCard = new AnimatedCard({x:px,y:py}, endPosition, 400, wait, gui.cardBack, 
                    cardDimensions.width, cardDimensions.height, 
                    soundDisplacement>=this.MIN_SOUND_DISPLACEMENT ? this.pickupSound : null, false);
                gui.movingCards.push(movingCard);
                wait += cardIncr;
                if(soundDisplacement >= gui.MIN_SOUND_DISPLACEMENT) soundDisplacement -= gui.MIN_SOUND_DISPLACEMENT;
                soundDisplacement += cardIncr;
            }
            py += pgap+pheight;
        }
        this.countEnd = wait+400;

        //SHARING OUT ANIMATION
        wait = 7000;
        py = y + ourHeight - (cardDimensions.height - pheight)/2;
        soundDisplacement = gui.MIN_SOUND_DISPLACEMENT;
        for(let player of game.players) {
            let cardIncr = this.playerIncr / this.yourCards.length;
            this.playerCountUpStart.push(wait + 400);
            for(let i = 0; i < this.yourCards.length; i++) {
                let movingCard = new AnimatedCard(endPosition, {x:px,y:py}, 400, wait, gui.cardBack,
                    cardDimensions.width, cardDimensions.height, 
                    soundDisplacement>=this.MIN_SOUND_DISPLACEMENT ? this.pickupSound : null, false);
                gui.movingCards.push(movingCard);
                wait += cardIncr;
                if(soundDisplacement >= gui.MIN_SOUND_DISPLACEMENT) soundDisplacement -= gui.MIN_SOUND_DISPLACEMENT;
                soundDisplacement += cardIncr;
            }
            py += pgap+pheight;
        }
    }

    draw(dt) {
        let pwidth = CARD_WIDTH * 3 * GUI_SCALE;
        let pheight = GUI_SCALE * 3;
        let pgap = GUI_SCALE;
        let ourWidth = CARD_WIDTH * 4 * GUI_SCALE;
        let ourHeight = ourWidth/2 + GUI_SCALE;
        let totalHeight = game.players.length * pheight + (game.players.length - 1) * pgap + ourHeight;

        let x = canvas.width/2 - ourWidth/2;
        let y = canvas.height/2 - totalHeight/2;
        let px = canvas.width/2 - pwidth/2;
        let py = y + ourHeight;
        let fontSize = Math.round(GUI_SCALE*2);


        ctx.globalAlpha = 0.5;
        ctx.fillStyle = "#fff";
        ctx.fillRect(x - GUI_SCALE, y-GUI_SCALE, ourWidth+2*GUI_SCALE,totalHeight+GUI_SCALE*2);

        ctx.globalAlpha = 1;
        ctx.drawImage(gui.sovietFlag, x, y, ourWidth, ourWidth/2);
        ctx.drawImage(gui.stalin,x+ourWidth/2,y, ourWidth/2,ourWidth/2);

        let ourCards = 0;
        if(this.timeElapsed > this.countStart && this.timeElapsed < this.countEnd) {
            ourCards = Math.floor((this.timeElapsed-this.countStart)/(this.countEnd-this.countStart) * this.ourCards);
        }else if(this.timeElapsed >= this.countEnd) {
            ourCards = this.ourCards;
        }

        
        drawText("OUR CARDS:", x + ourWidth/4, y+GUI_SCALE * 13, "center", fontSize, undefined, "#fff");
        drawText(ourCards, x + ourWidth/4, y+GUI_SCALE * 13 + fontSize, "center", fontSize, undefined, "#fff");


        for(let i = 0; i < game.players.length; i++) {
            let player = game.players[i];
            let nCards = player.nCards;
            let timeElapse = this.timeElapsed - this.playerCountDownStart[i];
            let timeElapse2 = this.timeElapsed - this.playerCountUpStart[i];
            if(timeElapse2 > this.playerIncr) {
                nCards = this.yourCards.length;
            }else if(timeElapse2>0) {
                nCards += this.yourCards.length * timeElapse2/this.playerIncr;
                nCards = Math.floor(nCards);
            }else if(timeElapse > this.playerIncr) {
                nCards = 0;
            }else if(timeElapse>0) {
                nCards -= nCards * timeElapse/this.playerIncr;
                nCards = Math.floor(nCards);
            }

            //box
            ctx.fillStyle = "#ed1b24";
            ctx.strokeStyle = "#fff";
            ctx.lineJoin = "round";
            ctx.lineWidth = pheight*0.1;
            ctx.strokeStyle = "#000";
            ctx.strokeRect(px+3, py+3, pwidth, pheight);
            ctx.fillRect(px, py, pwidth, pheight);
            ctx.strokeStyle = "#fff";
            ctx.strokeRect(px, py, pwidth, pheight);

            drawText(player.name,px+fontSize/2,py+pheight/2+fontSize/3,"left",fontSize,fontSize*5,"#fff");
            drawText(nCards,px+pwidth-fontSize/2,py+pheight/2+fontSize/3,"right",fontSize,fontSize*4,"#fff");
            py+=pgap+pheight;
        }



        this.timeUntilDone -= dt;
        this.timeElapsed += dt;

        if(!this.removedCards && this.timeElapsed > 4000) {
            for(let cardStack of game.yourStacks) {
                cardStack.cardIds.length = 0;
            }
            this.removedCards = true;
        }

        if(this.timeUntilDone <= 0) {
            gui.currentAnimation = null;
            gui.animatePickup(this.yourCards);
        }
    }
}