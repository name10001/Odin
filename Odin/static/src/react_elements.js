const $r = React.createElement


/**
 * Gets a button style that corresponds to a size in pixels
 * @param {Number} size 
 */
function getButtonStyle(size) {
    size = Math.floor(size);
    return {
        fontSize: size + "px",
        padding: size * 0.3 + "px " + size * 0.6 + "px ",
        margin: "0"
    };
}

/**
 * The discard pile shows all cards that have been played
 */
class DiscardPile extends React.Component {
    constructor(props) {
        super(props);
    }

    render() {
        //this.props.cards
        //this.props.height this.props.guiScale

        const width = this.props.guiScale * CARD_WIDTH;
        const height = this.props.guiScale * CARD_HEIGHT;
        const maxGap = this.props.height - height;
        const len = this.props.cards.length;
        const gap = maxGap / (len - 1);

        const cards = this.props.cards.map((card, index) => $r('img', {
            src: card, key: index, style: { position: 'absolute', zIndex: index + '', left: '0', bottom: index * gap + 'px' }, width: width, height: height, alt: 'card'
        }));

        return cards;
    }
}

/**
 * Represents the "play cards" "undo" and "undo all" buttons
 */
function ButtonPanel(props) {
    // style of the button in terms of font size
    const btnStyle = getButtonStyle(props.guiScale * 1.4);

    // play button
    const playButton = $r('button', { key: '1', onClick: () => game.finishTurn(), className: props.playAvaliable ? 'btn btn-primary btn-block' : 'btn btn-secondary btn-block', style: btnStyle }, props.playMessage);

    if (props.undoAvaliable) {
        // size of the gap between buttons
        const gap = props.guiScale / 2 + "px";

        // undo button
        const undoButton = $r('div', {
            key: '2', className: 'col-xs-5', style: { padding: gap + " " + gap + " 0 0" }
        }, $r('button', { onClick: () => game.undo(), className: 'btn btn-primary btn-block', style: btnStyle }, "UNDO"));

        // undo all button
        const undoAllButton = $r('div', {
            key: '3', className: 'col-xs-7', style: { padding: gap + " 0 0 0" }
        }, $r('button', { onClick: () => game.undoAll(), className: 'btn btn-primary btn-block', style: btnStyle }, "UNDO ALL"));

        return [playButton, undoButton, undoAllButton];
    }
    else {
        return playButton;
    }
}

/**
 * Represents a panel on the screen with a card and 2 buttons.
 */
function CardPanel(props) {
    const width = props.guiScale * (CARD_WIDTH + 1) + "px";

    const cardWidth = props.guiScale * CARD_WIDTH + "px";
    const cardHeight = props.guiScale * CARD_HEIGHT + "px";

    // card click button
    const cardButtonChildren = [];
    const card = $r('img', { key: '1', src: props.stack.url, width: cardWidth, height: cardHeight, alt: props.stack.name, style: { position: 'absolute', left: '0', top: '0', zIndex: '1' } });

    cardButtonChildren.push(card);
    if (props.stack.size() > 1) {
        // indicator of the size of the stack
        const numberIndicator = $r('span', {
            key: '2', style: {
                backgroundColor: '#fff', position: 'absolute', borderRadius: "3px", left: '0', bottom: '0', padding: '5px 10px', fontSize: props.guiScale * 1.5 + "px", zIndex: '2'
            }
        }, "x" + props.stack.size());
        cardButtonChildren.push(numberIndicator);
    }
    if (!props.stack.allowedToPlay) {
        // make transparent if not allowed to play
        const transparent = $r('img', { key: '3', src: '/static/transparent.png', width: '100%', height: '100%', style: { position: 'absolute', left: '0', top: '0', zIndex: '3' } });
        cardButtonChildren.push(transparent)
    }

    const cardButton = $r('button', {
        style: { width: cardWidth, height: cardHeight, margin: props.guiScale / 2 + "px", display: 'block', position: 'relative' }, className: 'transparent-button', onClick: () => props.stack.playSingle()
    }, cardButtonChildren);

    // help button
    const helpStyle = getButtonStyle(props.guiScale * 1.3);
    helpStyle.float = "left";
    helpStyle.marginLeft = props.guiScale + "px";

    const help = $r('button', { className: 'btn btn-primary', style: helpStyle }, "?");

    // addall button
    const addAllStyle = getButtonStyle(props.guiScale * 1.3);
    addAllStyle.marginRight = props.guiScale + "px";
    addAllStyle.float = "right";

    const addAll = $r('button', {
        className: 'btn btn-primary', style: addAllStyle, onClick: () => props.stack.playAll()
    }, "+ALL");

    // return entire card stack
    return $r('div', { style: { width: width, display: "inline-block" } }, cardButton, help, addAll);
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
            game: game
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
        this.state.game = game;
        this.setState(this.state);
    }

    /**
     * Render the entire game
     */
    render() {
        // discard pile
        const discardHeight = this.state.guiScale * CARD_HEIGHT * 2;
        const discardPile = $r(DiscardPile, { height: discardHeight, guiScale: this.state.guiScale, cards: this.state.game.topCards });
        const discardWrapper = $r('div', { key: 'dp', style: { width: this.state.guiScale * CARD_WIDTH + "px", height: discardHeight, position: 'relative' } }, discardPile);


        // button panel
        let playMessage;
        if (this.state.game.planningCards.length == 0) {
            playMessage = "+" + (this.state.game.pickupAmount == 0 ? '1' : this.state.game.pickupAmount);
        }
        else if (this.state.game.cantPlayReason.length > 0) {
            playMessage = this.state.game.cantPlayReason;
        }
        else {
            playMessage = "PLAY CARDS";
        }

        const buttons = $r(ButtonPanel, { undoAvaliable: this.state.game.planningCards.length > 0, playMessage: playMessage, playAvaliable: this.state.game.yourTurn && this.state.game.cantPlayReason.length == 0, guiScale: this.state.guiScale });
        const buttonsWrapper = $r('div', { key: 'bp', style: { width: this.state.guiScale * CARD_WIDTH * 2.5 + "px" } }, buttons);

        // card scroller
        const scroller = $r(CardScroller, { key: 'cs', cardStacks: this.state.game.yourStacks, guiScale: this.state.guiScale });

        return [discardWrapper, buttonsWrapper, scroller];
    }
}