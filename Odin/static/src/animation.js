/*

animation.js has the gui code for "animations" - which play temporarily on screen and are removed immeditately after.

*/

/**
 * Handles all animations and draws them all to the screen
 */
class AnimationHandler extends React.Component {
    constructor(props) {
        super(props);
        this.state = { animations: {} };
    }

    /**
     * Play an animation
     * @param {String} id
     * @param {Function} createAnimation A React.createElement function that creates the animation
     * @param {Function} endFunction A function that is called when endAnimation() is called
     */
    playAnimation(id, createAnimation, endFunction) {
        const animations = this.state.animations;
        animations[id] = { createAnimation, endFunction };

        this.setState({ animations });
    }

    /**
     * Is called when an animation is finished, causing the animation to be removed and the endFunction to be called
     * @param {*} id 
     */
    endAnimation(id) {
        const animations = this.state.animations;
        
        if(id in animations) {
            if (animations[id].endFunction) {
                animations[id].endFunction();
            }

            delete animations[id];

            this.setState({ animations });
        }
    }

    hasAnimation(id) {
        return id in this.state.animations;
    }

    getUniqueId(id) {
        while (id in this.state.animations) {
            id += "_";
        }
        return id;
    }

    /**
     * Render all animations
     */
    render() {
        if (Object.keys(this.state.animations).length > 0) {
            const animations = [];
            for (const id of Object.keys(this.state.animations)) {
                animations.push(this.state.animations[id].createAnimation());
            }
            return animations;
        }
        else {
            return "";
        }
    }
}

/**
 * An abstract animation which contains a gameloop
 */
class AbsAnimation extends React.Component {
    constructor(props) {
        super(props);

        this.beginTime = 0;
        this.running = true;
    }

    /**
     * Begin the animation at time t = 0
     */
    componentDidMount() {
        window.requestAnimationFrame((timestamp) => {
            this.beginTime = timestamp;
            this.loop(timestamp);
        });
    }

    /**
     * Stop the animation
     */
    componentWillUnmount() {
        this.running = false;
    }

    /**
     * Perform a loop of animation frames
     * @param {Number} timestamp 
     */
    loop(timestamp) {
        const t = timestamp - this.beginTime;
        this.update(t);

        if (this.running) {
            window.requestAnimationFrame((timestamp) => this.loop(timestamp));
        }
    }

    /**
     * update the animation
     * @param {*} t time (in ms) since the beginning of the animation 
     */
    update(t) {
        console.log("TIME: " + t + " (This function should be overridden)");
    }

    render() {
        return "";
    }
}

class MessageAnimation extends AbsAnimation {
    constructor(props) {
        super(props);

        this.message = props.message;
        this.time = props.time;
        this.fadeIn = props.fadeIn;
        this.fadeOut = props.fadeOut;

        this.state = { opacity: 0 };
    }

    update(t) {

        if (t > this.time) {
            gui.getAnimationHandler().endAnimation(this.props.id);

        } else if (t < this.fadeIn) {
            this.setState({ opacity: t / this.fadeIn });

        } else if (t > this.time - this.fadeOut) {
            this.setState({ opacity: (this.time - t) / this.fadeOut });

        } else {
            this.setState({ opacity: 1 });
        }
    }

    render() {
        const text = $r('h1', { key: '1', style: { position: 'fixed', top: '50%', left: '50%', transform: 'translate(-50%, -50%)', opacity: this.state.opacity, color: '#fff', zIndex: '9999' } }, this.message);

        const background = $r('div', { key: '2', style: { left: '0', top: '0', width: '100%', height: '100%', position: 'fixed', backgroundColor: '#000', opacity: 0.5 * this.state.opacity, zIndex: '9998' } });
        return [background, text];
    }
}


/**
 * A card that moves from one position to another on the screen.
 * 
 * Rquired props: startPos, endPos, startTime, endTime, url TODO
 */
class MovingCard extends React.Component {
    constructor(props) {
        super(props);

        this.state = { show: false, t: 0, x: 0, y: 0 }
    }

    /**
     * Returns true once the card has finished moving
     */
    hasStoppedMoving() {
        return this.state.t > this.props.endTime;
    }

    /**
     * Returns true once the card has started moving
     */
    hasBegunMoving() {
        return this.state.t >= this.props.startTime;
    }

    /**
     * Update the position of the card, the card should not display if 
     * @param {Number} t 
     */
    update(t) {
        const state = {};

        const dx = this.props.endPos.x - this.props.startPos.x;
        const dy = this.props.endPos.y - this.props.startPos.y;
        const dt = this.props.endTime - this.props.startTime;

        state.t = t;
        state.show = t >= this.props.startTime && t <= this.props.endTime;

        // don't update if the card is not showing onscreen
        if (!this.state.show && !state.show) return;

        if (state.show) {
            const interpolate = (t - this.props.startTime) / dt;

            state.x = interpolate * dx + this.props.startPos.x;
            state.y = interpolate * dy + this.props.startPos.y;
        }
        else {
            state.x = 0;
            state.y = 0;
        }

        // has just ended moving - play sound if it exists
        if (this.state.show && !state.show) {
            if (this.props.sound !== undefined) {
                playSound(this.props.sound);
            }
        }

        this.setState(state);
    }

    render() {
        if (!this.state.show) return "";
        return $r('img', {
            src: this.props.url, alt: this.props.name, width: this.props.cardWidth, height: this.props.cardHeight, style: {
                position: 'fixed', left: this.state.x, top: this.state.y, zIndex: 8000
            }
        });
    }
}

const MAX_CARDS_IN_ANIMATION = 50;

/**
 * Animate cards moving across the screen
 */
class CardAnimation extends AbsAnimation {
    constructor(props) {
        super(props);

        this.cards = [];


        // if too many cards, don't display (still update tho)

        // I'm sorry I don't know how to describe these variables lmao
        let i = 1;
        const j = props.cards.length / MAX_CARDS_IN_ANIMATION;
        let k = props.cards.length;

        let t = props.delay;

        for (const cardProps of props.cards) {
            if (!cardProps['id'] || !cardProps['name'] || !cardProps['url']) {
                continue;
            }

            const card = { startTime: t, endTime: t + props.travelTime, id: cardProps['id'], name: cardProps['name'], url: cardProps['url'] };
            if (cardProps['startPos'] !== undefined) card.startPos = cardProps['startPos'];
            if (cardProps['endPos'] !== undefined) card.endPos = cardProps['endPos'];


            // only create a reference and add it if there isn't too many cards, always display the last card.
            if (i >= 1 || k == 1) {
                i -= j;

                card.ref = React.createRef();

                this.cards.push(card);
            }
            i++;

            t += props.gap;
            k--;
        }
        if (props.reverse) {
            this.cards.reverse();
        }
    }

    update(t) {

        let finished = true;
        for (const card of this.cards) {
            card.ref.current.update(t);
            if (!card.ref.current.hasStoppedMoving()) finished = false;
        }
        if (finished) {
            gui.getAnimationHandler().endAnimation(this.props.id);
        }
    }

    render() {
        const cards = [];

        for (const card of this.cards) {
            cards.push($r(MovingCard, {
                ref: card.ref, startPos: card.startPos !== undefined ? card.startPos : this.props.startPos, endPos: card.endPos !== undefined ? card.endPos : this.props.endPos, startTime: card.startTime,
                endTime: card.endTime, url: card.url, cardWidth: this.props.cardWidth, cardHeight: this.props.cardHeight, key: card.id, id: card.id, name: card.name, sound: this.props.sound,
                moveStartFunction: this.props.moveStartFunction, moveEndFunction: this.props.moveEndFunction
            }));
        }

        return cards;
    }
}

class CommunistAnimation extends AbsAnimation {
    constructor(props) {
        super(props);

        this.initDelay = 3400;
        this.midDelay = 3400;
        this.endDelay = 6600;

        this.totalCards = props.cards.length * game.players.length;

        this.removeCards = [];
        for (const stack of game.yourStacks) {
            for (const id of stack.cardIds) {
                this.removeCards.push({ 'url': stack.url, 'name': stack.name, 'id': id });
            }
        }

        this.pickupCards = props.cards;

        this.state = { stateIndex: 0, cards: 0 };
    }

    getDeckPosition() {
        const bounds = document.getElementById('communist-div').getBoundingClientRect();
        let s = (bounds.bottom - bounds.top) / 10;
        let x = bounds.right - gui.state.guiScale * CARD_WIDTH - s;
        let y = bounds.top + s;

        return { x, y };
    }

    update(t) {

        // update number of cards
        if (t > this.initDelay + REMOVE_TIME && this.state.stateIndex == 1) {
            let interpolate = (t - this.initDelay - REMOVE_TIME) / MAX_CARD_TRANSFER_TIME;
            this.setState({ stateIndex: 1, cards: Math.floor(Math.min(this.totalCards * interpolate, this.totalCards)) });
        }

        if (t > this.initDelay && this.state.stateIndex == 0) {
            gui.animateRemoveCards(this.removeCards, this.getDeckPosition(), false);

            for (const player of game.players) {
                if (player.id != game.yourId) {
                    gui.animatePlayerRemove(player.id, player.nCards, this.getDeckPosition(), false);
                }
            }
            this.setState({ stateIndex: 1, cards: this.state.cards });
        }

        if (t > this.initDelay + MAX_CARD_TRANSFER_TIME + REMOVE_TIME && this.state.stateIndex == 1) {
            game.clearEmptyStacks();
            gui.getCardScroller().updateStacks(game.yourStacks, game.yourTurn);
            this.setState({ stateIndex: 2, cards: this.state.cards });
        }

        if (t > this.initDelay + this.midDelay && this.state.stateIndex == 2) {
            gui.animatePickupFromDeck(this.pickupCards, this.getDeckPosition(), false);

            for (const player of game.players) {
                if (player.id != game.yourId) {
                    gui.animatePlayerPickup(player.id, this.pickupCards.length, this.getDeckPosition(), false);
                }
            }
            this.setState({ stateIndex: 3, cards: this.state.cards });
        }
        if (t > this.initDelay + this.midDelay + MAX_CARD_TRANSFER_TIME + REMOVE_TIME && this.state.stateIndex == 3) {
            for (const card of this.pickupCards) {
                game.addCard(card.id, card.name, card.url, false);
            }
            gui.getCardScroller().updateStacks(game.yourStacks, game.yourTurn);

            this.setState({ stateIndex: 4, cards: this.state.cards });
        }

        if (t > this.initDelay + this.midDelay + this.endDelay && this.state.stateIndex == 4) {
            gui.getAnimationHandler().endAnimation(this.props.id);
        }
    }

    render() {
        // guiScale shorthand
        const s = gui.state.guiScale;

        let width = s * 36;
        let height = s * 18;


        const flagImg = $r('img', { key: 'flag', width, height, src: '/static/soviet.png', style: { position: 'absolute' } })


        const stalinImg = $r('img', { key: 'stalin', width: height * 0.8, height: height * 0.8, src: '/static/stalin.png', style: { position: 'absolute', right: height * 0.1 + 'px', top: height * 0.1 + 'px' }, alt: 'ya boi stalin' });

        const ourCards = $r('span', { key: 'text', style: { position: 'absolute', left: height * 0.1, bottom: height * 0.1, fontSize: height * 0.1, color: '#fff' } }, 'Our Cards: ' + this.state.cards);


        return $r('div', { id: 'communist-div', style: { width, height, position: 'fixed', left: s * 6 + 'px', top: s * 6 + 'px', zIndex: '7999' } }, [flagImg, stalinImg, ourCards]);
    }
}