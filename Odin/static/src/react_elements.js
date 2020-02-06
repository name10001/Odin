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
 * Represents a pile of cards. The pile should be contained within a div of a specific height, all cards are aligned to fit within the div.
 * The top of the pile should be the last card in the array.
 */
class CardPile extends React.Component {
    constructor(props) {
        super(props);
    }

    render() {
        // calculations such that all cards fit within the stack
        const width = this.props.guiScale * CARD_WIDTH;
        const height = this.props.guiScale * CARD_HEIGHT;
        const totalGap = this.props.height - height;
        const len = this.props.cards.length;
        const gap = Math.min(totalGap / (len - 1), this.props.maxGap);

        const cards = this.props.cards.reduce((result, card, index) => {
            if (this.props.grey) {
                // greyed out card
                const cardStyle = { position: 'absolute', zIndex: index * 2 + '', left: '0' };
                const greyCardStyle = { position: 'absolute', zIndex: index * 2 + 1 + '', left: '0' };

                if (this.props.alignment == 'bottom-bottom') {
                    cardStyle.bottom = index * gap + 'px';
                    greyCardStyle.bottom = index * gap + 'px';
                }
                else if (this.props.alignment == 'bottom-top') {
                    cardStyle.top = index * gap + 'px';
                    greyCardStyle.top = index * gap + 'px';
                }
                else if (this.props.alignment == 'top-top') {
                    cardStyle.top = (len - 1 - index) * gap + 'px';
                    greyCardStyle.top = (len - 1 - index) * gap + 'px';
                }
                else if (this.props.alignment == 'top-bottom') {
                    cardStyle.bottom = (len - 1 - index) * gap + 'px';
                    greyCardStyle.bottom = (len - 1 - index) * gap + 'px';
                }
                result.push(
                    $r('img', {
                        src: card, key: index + '', style: cardStyle, width: width, height: height
                    }),
                    $r('img', {
                        src: '/static/transparent.png', key: index + 't', style: greyCardStyle, width: width, height: height
                    })
                );

            }
            else {
                // regular card
                const cardStyle = { position: 'absolute', zIndex: index + '', left: '0' };

                if (this.props.alignment == 'bottom-bottom') {
                    cardStyle.bottom = index * gap + 'px';
                }
                else if (this.props.alignment == 'bottom-top') {
                    cardStyle.top = index * gap + 'px';
                }
                else if (this.props.alignment == 'top-top') {
                    cardStyle.top = (len - 1 - index) * gap + 'px';
                }
                else if (this.props.alignment == 'top-bottom') {
                    cardStyle.bottom = (len - 1 - index) * gap + 'px';
                }

                result.push(
                    $r('img', {
                        src: card, key: index, style: cardStyle, width: width, height: height
                    })
                );
            }

            return result;
        }, []);

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
    const playButton = $r('button', props.playAvaliable ? { key: '1', onClick: () => game.finishTurn(), className: 'btn btn-primary btn-block', style: btnStyle } : {
        key: '1', disabled: true, className: 'btn btn-primary btn-block', style: btnStyle
    }, props.playMessage);

    // size of the gap between buttons
    const gap = props.guiScale / 2 + "px";

    // undo button

    const undoButton = $r('div', {
        key: '2', className: 'col-xs-5', style: { padding: gap + " " + gap + " 0 0" }
    }, $r('button', props.undoAvaliable ? { onClick: () => game.undo(), className: 'btn btn-primary btn-block', style: btnStyle } : {
        className: 'btn btn-primary btn-block', disabled: true, style: btnStyle
    }, "UNDO"));

    // undo all button
    const undoAllButton = $r('div', {
        key: '3', className: 'col-xs-7', style: { padding: gap + " 0 0 0" }
    }, $r('button', props.undoAvaliable ? { onClick: () => game.undoAll(), className: 'btn btn-primary btn-block', style: btnStyle } : {
        className: 'btn btn-primary btn-block', disabled: true, style: btnStyle
    }, "UNDO ALL"));

    return [playButton, undoButton, undoAllButton];
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

    const cardProps = {
        style: { width: cardWidth, height: cardHeight, margin: props.guiScale / 2 + "px", display: 'block', position: 'relative' }, className: 'transparent-button',
    }
    if (props.stack.allowedToPlay) {
        cardProps.onClick = () => props.stack.playSingle();
    }
    else {
        cardProps.disabled = true;
    }

    const cardButton = $r('button', cardProps, cardButtonChildren);

    // help button
    const helpStyle = getButtonStyle(props.guiScale * 1.3);
    helpStyle.float = "left";
    helpStyle.marginLeft = props.guiScale + "px";

    const help = $r('button', { className: 'btn btn-primary', style: helpStyle }, "?");

    // addall button
    const addAllStyle = getButtonStyle(props.guiScale * 1.3);
    addAllStyle.marginRight = props.guiScale + "px";
    addAllStyle.float = "right";

    const addAll = $r('button', props.stack.allowedToPlay ? {
        className: 'btn btn-primary', style: addAllStyle, onClick: () => props.stack.playAll()
    } : {
            className: 'btn btn-primary', style: addAllStyle, disabled: true
        }, "+ALL");

    // return entire card stack
    return $r('div', { style: { width: width, display: "inline-block", paddingBottom: props.guiScale / 2 + "px" } }, cardButton, help, addAll);
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

        return $r('div', { id: 'card-scroller', style: { width: '100%', overflowX: 'scroll', textAlign: 'center', whiteSpace: 'nowrap', position: 'fixed', bottom: '0px' } }, panels);
    }
}

function PlayerPanel(props) {
    return props.player.name + "/" + props.player.nCards;
}

/**
 * A list of panels containing information about each player in order of their turn
 */
class PlayerListPanel extends React.Component {
    constructor(props) {
        super(props);
    }

    render() {
        const nPlayers = this.props.players.length;

        if (nPlayers == 0) {
            return "";
        }

        const maxHeight = this.props.guiScale * 5;
        const maxGap = this.props.guiScale * 2;

        const totalHeight = maxGap + nPlayers * (maxGap + maxHeight);

        const scale = 1;
        if (maxHeight > this.props.height) scale = this.props.height / totalHeight;

        const panels = [];

        let i = this.props.turn;

        do {
            const player = this.props.players[i];
            panels.push($r(PlayerPanel, {key: i, player, width: i == this.props.turn ? this.props.width * 0.9 : this.props.width, height: maxHeight * scale, gap: maxGap * scale}))

            i += this.props.direction;
            if (i < 0) i = game.players.length - 1;
            else if (i >= game.players.length) i = 0;
        } while (i != this.props.turn);

        return panels;
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

        // card scroller
        const scroller = $r(CardScroller, { key: 'cs', cardStacks: this.state.game.yourStacks, guiScale: this.state.guiScale });

        // calculating how the central componants should be arranged
        const cardWidth = this.state.guiScale * CARD_WIDTH;
        const cardHeight = this.state.guiScale * CARD_HEIGHT;
        const gapSize = this.state.guiScale * 1.2;

        const buttonsWidth = cardWidth * 2 + gapSize;
        const buttonsHeight = this.state.guiScale * 6.2;

        const playerListWidth = cardWidth * 2.8;

        const containerHeight = this.state.height - (this.state.guiScale * (CARD_HEIGHT + 5) + 25);
        const containerWidth = buttonsWidth + gapSize + playerListWidth;

        // discard pile
        const discardHeight = this.state.guiScale * CARD_HEIGHT * 1.4;
        const discardPile = $r(CardPile, { height: discardHeight, guiScale: this.state.guiScale, cards: this.state.game.topCards, maxGap: discardHeight / 3, alignment: 'top-bottom', grey: true });
        const discardWrapper = $r('div', { key: 'dp', style: { width: cardWidth + "px", height: discardHeight, position: 'absolute', bottom: buttonsHeight + gapSize + 'px' } }, discardPile);

        // planning pile
        const planningHeight = containerHeight - buttonsHeight - gapSize * 2;
        const planningPile = $r(CardPile, { height: planningHeight, guiScale: this.state.guiScale, cards: this.state.game.planningCards, maxGap: this.state.guiScale, alignment: 'bottom-bottom', grey: false });
        const planningWrapper = $r('div', { key: 'pp', style: { width: cardWidth + "px", height: planningHeight, position: 'absolute', bottom: buttonsHeight + gapSize + 'px', left: cardWidth + gapSize + 'px' } }, planningPile);

        // deck
        const deckTop = (containerHeight - discardHeight - buttonsHeight - gapSize - cardHeight) / 2;
        const deckImage = $r('img', { src: '/static/cards/back.png', key: 'di', style: { width: cardWidth + 'px', height: cardHeight + 'px', position: 'absolute', top: deckTop + 'px' } });

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

        const buttons = $r(ButtonPanel, {
            undoAvaliable: this.state.game.planningCards.length > 0 && this.state.game.yourTurn, playMessage: playMessage, playAvaliable: this.state.game.yourTurn && this.state.game.cantPlayReason.length == 0, guiScale: this.state.guiScale
        });
        const buttonsWrapper = $r('div', { key: 'bp', style: { position: 'absolute', bottom: '0', width: buttonsWidth + "px" } }, buttons);

        // player list
        const playerList = $r(PlayerListPanel, { width: playerListWidth, height: containerHeight, players: this.state.game.players, turn: this.state.game.turn, skip: this.state.game.skip, direction: this.state.game.direction });
        const playerListWrapper = $r('div', { key: 'plp', style: { position: 'absolute', right: '0', width: playerListWidth, height: containerHeight } }, playerList);

        // container to hold everything in the UI
        const container = $r('div', {
            key: 'ctr', style: { margin: 'auto', position: 'relative', width: containerWidth + 'px', height: containerHeight + 'px' }
        }, [deckImage, discardWrapper, planningWrapper, buttonsWrapper, playerListWrapper]);

        return [container, scroller];
    }
}