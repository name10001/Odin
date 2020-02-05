const $r = React.createElement


function getButtonStyle(size) {
    size = Math.floor(size);
    return {
        fontSize: size + "px",
        padding: size * 0.3 + "px " + size * 0.6 + "px ",
        margin: "0"
    };
}


/**
 * Represents the "play cards" "undo" and "undo all" buttons
 */
class ButtonPanel extends React.Component {
    render() {

        const playButton = $r('button', { key: '1', onClick: () => game.finishTurn(), className: this.props.playAvaliable ? 'btn btn-primary btn-lg btn-block' : 'btn btn-secondary btn-lg btn-block' }, this.props.playMessage);

        if (this.props.undoAvaliable) {
            // undo buttons
            const undoButton = $r('div', { key: '2', className: 'col-xs-5', style: { padding: "10px 5px 0 0" } }, $r('button', { onClick: () => game.undo(), className: 'btn btn-primary btn-lg btn-block' }, "UNDO"));
            const undoAllButton = $r('div', { key: '3', className: 'col-xs-7', style: { padding: "10px 0 0 5px" } }, $r('button', { onClick: () => game.undoAll(), className: 'btn btn-primary btn-lg btn-block' }, "UNDO ALL"));

            return [playButton, undoButton, undoAllButton];
        }
        else {
            return playButton;
        }
    }
}

/**
 * Represents a panel on the screen with a card and 2 buttons.
 */
class CardPanel extends React.Component {
    constructor(props) {
        super(props);
    }

    render() {
        const width = this.props.guiScale * (CARD_WIDTH + 1) + "px";

        const cardWidth = this.props.guiScale * CARD_WIDTH + "px";
        const cardHeight = this.props.guiScale * CARD_HEIGHT + "px";

        // card click button
        const card = $r('button', {
            style: { margin: this.props.guiScale / 2 + "px", display: 'block' }, className: 'transparent-button', onClick: () => this.props.stack.playSingle()
        }, $r('img', { src: this.props.stack.url, width: cardWidth, height: cardHeight, alt: this.props.stack.name }));

        // help button
        const helpStyle = getButtonStyle(this.props.guiScale * 1.3);
        helpStyle.float = "left";
        helpStyle.marginLeft = this.props.guiScale + "px";

        const help = $r('button', { className: 'btn btn-primary', style: helpStyle }, "?");

        // addall button
        const addAllStyle = getButtonStyle(this.props.guiScale * 1.3);
        addAllStyle.marginRight = this.props.guiScale + "px";
        addAllStyle.float = "right";

        const addAll = $r('button', {
            className: 'btn btn-primary', style: addAllStyle, onClick: () => this.props.stack.playAll()
        }, "+ALL");

        // return entire card stack
        return $r('div', { style: { width: width, display: "inline-block" } }, card, help, addAll);
    }
}

/**
 * Scrolling function with the mouse wheel
 */
function scrollHorizontally(e) {
    e = window.event || e;
    var delta = Math.max(-1, Math.min(1, (e.wheelDelta || -e.detail)));
    document.getElementById('card-scroller').scrollLeft -= (delta * 80); // Multiplied by 40
}

/**
 * The scroll panel at the bottom which shows all your cards
 */
class CardScroller extends React.Component {
    constructor(props) {
        super(props);
    }

    /**
     * Add resize listener
     */
    componentDidMount() {
        // IE9, Chrome, Safari, Opera
        window.addEventListener("mousewheel", (e) => scrollHorizontally(e), false);
        // Firefox
        window.addEventListener("DOMMouseScroll", (e) => scrollHorizontally(e), false);
    }
    /**
     * Render all card stack panels
     */
    render() {
        const panels = this.props.cardStacks.map((stack) =>
            $r(CardPanel, { key: stack.url, guiScale: this.props.guiScale, stack: stack })
        );

        const height = ((this.props.guiScale * (CARD_HEIGHT + 4)) + 25) + "px";

        return $r('div', { id: 'card-scroller', style: { width: '100%', height: height, overflowX: 'auto', textAlign: 'center', whiteSpace: 'nowrap', position: 'fixed', bottom: '0px' } }, panels);
    }
}

/**
 * OdinGui represents the entire wrapper of the 
 */
class OdinGui extends React.Component {

    /**
     * Initialize the gui
     * @param {*} props 
     */
    constructor(props) {
        super(props);

        this.state = {
            width: 0,
            height: 0,
            guiScale: 0,
            cardStacks: game.yourStacks,
            planningCards: game.planningCards,
            yourTurn: game.yourTurn,
            cantPlayReason: game.cantPlayReason
        };
    }

    /**
     * Animate playing cards
     */
    animatePlayCards() {
        console.log("TODO: ANIMATE");
        game.finishedEvent();
    }

    /**
     * Animate playing cards
     */
    animateFinishPlayCards() {
        console.log("TODO: ANIMATE");
        game.finishedEvent();
    }

    /**
     * Animate playing cards
     */
    animateUndoAll() {
        console.log("TODO: ANIMATE");
        game.finishedEvent();
    }

    /**
     * Animate playing cards
     */
    animatePickupFromDeck() {
        console.log("TODO: ANIMATE");
        game.finishedEvent();
    }

    /**
     * Animate playing cards
     */
    animatePickupFromPlayer() {
        console.log("TODO: ANIMATE");
        game.finishedEvent();
    }

    /**
     * Animate playing cards
     */
    animatePlayerPickup() {
        console.log("TODO: ANIMATE");
        game.finishedEvent();
    }

    /**
     * Animate playing cards
     */
    animatePlayerCardTransfer() {
        console.log("TODO: ANIMATE");
        game.finishedEvent();
    }

    /**
     * Animate playing cards
     */
    animateUndo() {
        console.log("TODO: ANIMATE");
        game.finishedEvent();
    }

    /**
     * Update the size of the gui when resizing the window
     */
    updateSize() {
        const width = window.innerWidth / MIN_WIDTH;
        const height = window.innerHeight / MIN_HEIGHT;
        let guiScale;
        if (width < height) guiScale = width;
        else guiScale = height;

        this.state.width = window.innerWidth;
        this.state.height = window.innerHeight;
        this.state.guiScale = guiScale;

        this.setState(this.state);
    }

    /**
     * On the creation of this element
     */
    componentDidMount() {
        window.addEventListener('resize', () => {
            this.updateSize()
        });
        this.updateSize();
    }

    /**
     * Update the gui with anything that changed in the game.
     * @param {*} game
     */
    updateGame(game) {
        this.state.cardStacks = game.yourStacks;
        this.state.planningCards = game.planningCards;
        this.state.cantPlayReason = game.cantPlayReason;
        this.state.yourTurn = game.yourTurn;
        this.setState(this.state);
    }

    /**
     * Render the entire game
     */
    render() {
        // button panel
        let playMessage;
        if (game.planningCards.length == 0) {
            playMessage = "+1";
        }
        else if (game.cantPlayReason.length > 0) {
            playMessage = game.cantPlayReason;
        }
        else {
            playMessage = "PLAY CARDS";
        }


        const buttons = $r(ButtonPanel, { undoAvaliable: this.state.planningCards.length > 0, playMessage: playMessage, playAvaliable: this.state.yourTurn && this.state.cantPlayReason.length == 0 });
        const buttonsWrapper = $r('div', { key: '1', style: { width: this.state.guiScale * CARD_WIDTH * 2.5 + "px" } }, buttons);


        // card scroller
        const scroller = $r(CardScroller, { key: '2', cardStacks: this.state.cardStacks, guiScale: this.state.guiScale });


        return [buttonsWrapper, scroller];
    }
}