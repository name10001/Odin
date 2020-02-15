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
        if (id in animations) {
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

        if (state.show) {
            const interpolate = (t - this.props.startTime) / dt;

            state.x = interpolate * dx + this.props.startPos.x;
            state.y = interpolate * dy + this.props.startPos.y;
        }
        else {
            state.x = 0;
            state.y = 0;
        }

        // has just started moving
        if (!this.state.show && state.show) {
            this.props.moveStartFunction({ id: this.props.id, name: this.props.name, url: this.props.url });
        }
        // has just ended moving
        else if (this.state.show && !state.show) {
            this.props.moveEndFunction({ id: this.props.id, name: this.props.name, url: this.props.url });
        }

        this.setState(state);
    }

    render() {
        if (!this.state.show) return "";
        return $r('img', {
            src: this.props.url, alt: this.props.name, width: this.props.cardWidth, height: this.props.cardHeight, style: {
                position: 'fixed', backgroundColor: '#ff0', left: this.state.x, top: this.state.y, zIndex: 8000
            }
        });
    }
}

/**
 * Animate cards moving across the screen
 */
class CardAnimation extends AbsAnimation {
    constructor(props) {
        super(props);

        this.cards = [];

        let t = 0;
        for (const cardProps of props.cards) {
            const card = { startTime: t, endTime: t + props.travelTime, id: cardProps['id'], name: cardProps['name'], url: cardProps['url'], ref: React.createRef() };
            if (cardProps['startPos'] !== undefined) card.startPos = cardProps['startPos'];
            if (cardProps['endPos'] !== undefined) card.endPos = cardProps['endPos'];

            this.cards.push(card); // TODO adjust the times

            t += props.gap;
        }
        if (props.reverse) {
            this.cards.reverse();
        }
    }

    update(t) {
        let finished = true;
        for (const card of this.cards) {
            if (!card.ref.current) continue;
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
                endTime: card.endTime, url: card.url, cardWidth: this.props.cardWidth, cardHeight: this.props.cardHeight, key: card.id, id: card.id, name: card.name,
                moveStartFunction: this.props.moveStartFunction, moveEndFunction: this.props.moveEndFunction
            }));
        }

        return cards;
    }
}