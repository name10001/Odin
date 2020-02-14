/*

gui.js has all the code for the main parts of the gui that you can interact with.


*/

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
 * Represents a singular card button
 * @param {*} props 
 */
function CardButton(props) {
    const cardWidth = props.guiScale * CARD_WIDTH + "px";
    const cardHeight = props.guiScale * CARD_HEIGHT + "px";

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
        cardProps.onClick = props.clickFunction;
    }
    else {
        cardProps.disabled = true;
    }

    return $r('button', cardProps, cardButtonChildren);;
}

/**
 * Represents a panel on the screen with a card and 2 buttons.
 */
function CardPanel(props) {
    const width = props.guiScale * (CARD_WIDTH + 1) + "px";

    const cardButton = $r(CardButton, { guiScale: props.guiScale, stack: props.stack, clickFunction: () => props.stack.playSingle() });

    // help button
    const helpStyle = getButtonStyle(props.guiScale * 1.3);
    helpStyle.float = "left";
    helpStyle.marginLeft = props.guiScale + "px";

    const help = $r('button', { onClick: () => gui.openPopup(() => $r(HelpPopup, { key: '1', card: game.allCards[props.stack.name] }), true), className: 'btn btn-primary', style: helpStyle }, "?");

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
function scrollHorizontally(e, id, amount) {
    e = window.event || e;
    var delta = Math.max(-1, Math.min(1, (e.wheelDelta || -e.detail)));
    document.getElementById(id).scrollLeft -= (delta * amount); // Multiplied by 40
}

/**
 * The scroll panel at the bottom which shows all your cards
 */
class CardScroller extends React.Component {
    constructor(props) {
        super(props);

        this.state = { hidden: false };
    }

    /**
     * Add resize listener
     */
    componentDidMount() {
        const id = 'card-scroller'
        // IE9, Chrome, Safari, Opera
        document.getElementById(id).addEventListener("mousewheel", (e) => scrollHorizontally(e, id, 80), false);
        // Firefox
        document.getElementById(id).addEventListener("DOMMouseScroll", (e) => scrollHorizontally(e, id, 80), false);
    }

    hide() {
        this.setState({ hidden: true });
    }


    unhide() {
        this.setState({ hidden: false });
    }
    /**
     * Render all card stack panels
     */
    render() {
        const panels = this.props.cardStacks.map((stack) =>
            $r(CardPanel, { key: stack.url, guiScale: this.props.guiScale, stack: stack })
        );

        return $r('div', { id: 'card-scroller', style: { width: '100%', overflowX: 'scroll', textAlign: 'center', whiteSpace: 'nowrap', position: 'fixed', bottom: '0px', display: this.state.hidden ? 'none' : 'block' } }, panels);
    }
}


/**
 * Contains simple text with information about the current turn.
 * Consisting of:
 * - Who's turn it is.
 * - Pickup chain (if any)
 * @param {*} props 
 */
function InfoPanel(props) {
    const turnString = $r('span', { key: '1', style: { color: "#fff", display: 'inline-block', verticalAlign: 'middle', fontSize: props.fontSize, float: 'left' } }, props.turnString);

    if (props.pickupAmount > 0) {
        const pickupString = $r('span', { key: '2', style: { color: "#fff", fontSize: props.fontSize, float: 'right' } }, '+' + props.pickupAmount);

        return [turnString, pickupString];
    }

    return turnString;
}

/**
 * A singular player panel, consisting of a heading and a body.
 * The heading contains the player name and number of cards
 * The body contains other information about the player such as the effects they have and the number of cards they will pickup.
 * @param {*} props 
 */
function PlayerPanel(props) {
    const fontSize = props.height * 0.3;
    const smallFontSize = props.height * 0.2;
    const headingHeight = props.height * 0.5 + 'px';
    const bodyHeight = props.height * 0.5 + 'px';
    const imageSize = props.height * 0.25 + 'px';

    // heading contains the player name and number of cards
    const name = $r('span', { key: 'l', style: { fontSize: fontSize + 'px', float: 'left', display: 'inline-block', verticalAlign: 'middle' } }, props.player.name);
    const nCards = $r('span', { key: 'r', style: { fontSize: fontSize + 'px', float: 'right', display: 'inline-block', verticalAlign: 'middle' } }, props.player.nCards);

    // make the heading blue if the person is you
    const headingStyle = { height: headingHeight, lineHeight: headingHeight, padding: '0 ' + fontSize + 'px' };

    if (props.isYou) {
        headingStyle.backgroundColor = '#4f94cc';
        headingStyle.color = "#fff";
    }
    const heading = $r('div', { key: '1', className: 'panel-heading', style: headingStyle }, [name, nCards]);

    // body contains all the effects the player has
    const effectStyle = { fontSize: smallFontSize + 'px', display: 'inline-block', verticalAlign: 'middle' };

    const effects = [];

    if (props.player.nPickup > 0) { // pickup amount
        effects.push($r('span', { key: 'pu', style: effectStyle }, '+' + props.player.nPickup));
        effects.push($r('span', { key: 'pug', style: { width: props.height * 0.1 + 'px', display: 'inline-block' } }));
    }


    // other effects
    for (effect of props.player.effects) {
        // effect image
        effects.push($r('img', { key: effect['url'], src: effect['url'], alt: 'effect', width: imageSize, height: imageSize, style: effectStyle }));
        if (effect['amount left'] > 1) {
            effects.push($r('span', { key: effect['url'] + 'a', style: { width: props.height * 0.05 + 'px', display: 'inline-block' } }));
            effects.push($r('span', { key: effect['url'] + 'ag', style: effectStyle }, 'x' + effect['amount left']));
        }
        effects.push($r('span', { key: effect['url'] + 'g', style: { width: props.height * 0.1 + 'px', display: 'inline-block' } }));
    }


    const body = $r('div', { key: '2', className: 'panel-body', style: { height: bodyHeight, lineHeight: bodyHeight, overflow: 'hidden', padding: '0 ' + fontSize + 'px' } }, effects);

    return [heading, body];
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

        const maxHeight = this.props.guiScale * 4.5;
        const maxGap = this.props.guiScale * 0.8;

        const totalHeight = maxGap + nPlayers * (maxGap + maxHeight);

        let scale = 1;
        if (maxHeight > this.props.height) scale = this.props.height / totalHeight;

        const panels = [];

        let i = this.props.turn;

        do {
            const player = this.props.players[i];

            const panelWidth = i == this.props.turn ? this.props.width : this.props.width * 0.9;

            const playerPanel = $r(PlayerPanel, { player, width: panelWidth, height: maxHeight * scale, isYou: player.id == this.props.yourId });

            panels.push($r('div', {
                key: i, className: 'panel panel-default', style: {
                    width: panelWidth + 'px', height: maxHeight * scale + 'px', margin: maxGap * scale + 'px 0 0 0', display: 'inline-block', textAlign: 'left', position: 'relative'
                }
            }, playerPanel))

            i += this.props.direction;
            if (i < 0) i = game.players.length - 1;
            else if (i >= game.players.length) i = 0;
        } while (i != this.props.turn);

        return panels;
    }

}

/**
 * Represents the chat window, chat input field and send button
 */
class ChatWindow extends React.Component {
    constructor(props) {
        super(props);

        this.state = { chat: props.chat, message: "" };

        this.endOfChat = React.createRef();

        this.handleChange = this.handleChange.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);
    }

    /**
     * Update the chat message
     * @param {*} event 
     */
    handleChange(event) {
        this.setState({ chat: this.state.chat, message: event.target.value });
    }

    /**
     * Submission of new chat message
     * @param {*} event 
     */
    handleSubmit(event) {
        game.sendChat(this.state.message);
        this.setState({ chat: this.state.chat, message: '' });
        event.preventDefault();
    }

    scrollToBottom() {
        this.endOfChat.current.scrollIntoView({ behavior: 'smooth' });
    }

    componentDidMount() {
        this.scrollToBottom();
    }

    componentDidUpdate() {
        this.scrollToBottom();
    }

    /**
     * Update the chat and scroll to the bottom
     * @param {*} chat 
     */
    updateChat(chat) {
        this.setState({ chat, message: this.state.message });
    }

    render() {
        const fontSize = this.props.guiScale + 'px';

        // message dialog window
        const allMessages = [];
        let i = 0;
        allMessages.push($r('p', { key: i++, style: { color: '#999' } }, "-- Beginning of chat --"));

        for (const chat of this.state.chat) {
            allMessages.push($r('p', { key: i++ }, [
                $r('span', { key: 'player', style: { color: '#2e6da4', fontWeight: 'bold' } }, chat['player'] + ": "),
                chat['message']
            ]));
        }
        allMessages.push($r('div', { ref: this.endOfChat }));

        const dialog = $r('div', { key: '1', id: 'chat-window', style: { overflowY: 'scroll', height: '70%', display: 'block', fontSize } }, allMessages);

        // footer
        const inputStyle = { height: '100%', fontSize, padding: this.props.guiScale / 2 + 'px ' + this.props.guiScale + 'px' };

        const chatEntry = $r('input', { key: '2', type: 'text', className: 'form-control', placeholder: 'Your message...', style: inputStyle, required: true, onChange: this.handleChange, value: this.state.message });
        const chatSubmit = $r('span', { key: '3', className: 'input-group-btn' }, $r('button', { type: 'submit', className: 'btn btn-primary', style: inputStyle }, "Send"));

        const chatForm = $r('form', { onSubmit: this.handleSubmit, style: { height: '30%' } }, $r('div', { className: 'input-group', style: { height: '100%' } }, [chatEntry, chatSubmit]));

        return $r('div', { className: 'panel-body', style: { height: '100%', padding: this.props.guiScale * 0.75 + 'px' } }, [dialog, chatForm]);
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

        this.chatRef = React.createRef();
        this.cardsRef = React.createRef();
        this.popupRef = React.createRef();
        this.popup = { createPopup: null, canClose: true };

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
        eventHandler.finishedEvent();
    }

    /**
     * Animate playing cards
     */
    animateFinishPlayCards() {
        console.log("TODO: ANIMATE");
        eventHandler.finishedEvent();
    }

    /**
     * Animate playing cards
     */
    animateUndoAll() {
        console.log("TODO: ANIMATE");
        eventHandler.finishedEvent();
    }

    /**
     * Animate playing cards
     */
    animatePickupFromDeck() {
        console.log("TODO: ANIMATE");
        eventHandler.finishedEvent();
    }

    /**
     * Animate playing cards
     */
    animateRemoveCards() {
        console.log("TODO: ANIMATE");
        eventHandler.finishedEvent();
    }

    /**
     * Animate playing cards
     */
    animatePickupFromPlayer() {
        console.log("TODO: ANIMATE");
        eventHandler.finishedEvent();
    }

    /**
     * Animate playing cards
     */
    animatePlayerPickup() {
        console.log("TODO: ANIMATE");
        eventHandler.finishedEvent();
    }

    /**
     * Animate playing cards
     */
    animatePlayerCardTransfer() {
        console.log("TODO: ANIMATE");
        eventHandler.finishedEvent();
    }

    /**
     * Animate playing cards
     */
    animateUndo() {
        console.log("TODO: ANIMATE");
        eventHandler.finishedEvent();
    }

    /**
     * Animate playing cards
     */
    animateRemoveCardsToPlayer() {
        console.log("TODO: ANIMATE");
        eventHandler.finishedEvent();
    }

    /**
     * Animate playing cards
     */
    animatePlayerRemove() {
        console.log("TODO: ANIMATE");
        eventHandler.finishedEvent();
    }

    /**
     * Update the size of the gui when resizing the window
     */
    updateSize() {
        // stop the document from resizing due to the onscreen keyboard, also hide the card scroller
        if ($(document.activeElement).prop('type') == 'text' && typeof window.orientation !== 'undefined' && this.state.height > window.innerHeight) {
            this.state.width = window.innerWidth;
            this.state.height = window.innerHeight;
            this.cardsRef.current.hide();
            return;
        }

        const width = window.innerWidth / MIN_WIDTH;
        const height = window.innerHeight / MIN_HEIGHT;

        let guiScale;
        if (width < height) guiScale = width;
        else guiScale = height;

        this.state.width = window.innerWidth;
        this.state.height = window.innerHeight;
        this.state.guiScale = guiScale;


        if (this.cardsRef.current) {
            this.cardsRef.current.unhide();

        }
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
     * Update the chat
     * @param {*} chat 
     */
    updateChat(chat) {
        this.chatRef.current.updateChat(chat);
    }

    /**
     * Open a popup window
     * @param {*} createPopup 
     */
    openPopup(createPopup, canClose, closeFunction) {
        this.popup = { createPopup, canClose, closeFunction };

        this.popupRef.current.openPopup(this.popup);
    }

    /**
     * Close the current popup window
     */
    closePopup(doCloseFunction) {
        this.popupRef.current.closePopup(doCloseFunction);
    }

    /**
     * Render the entire game
     */
    render() {

        // card scroller
        const scroller = $r(CardScroller, { key: 'cs', cardStacks: this.state.game.yourStacks, guiScale: this.state.guiScale, ref: this.cardsRef });

        // popup
        const popup = $r(Popup, { key: 'pop', ref: this.popupRef, popup: this.popup });

        // calculating how the central componants should be arranged
        const cardWidth = this.state.guiScale * CARD_WIDTH;
        const cardHeight = this.state.guiScale * CARD_HEIGHT;
        const gapSize = this.state.guiScale * 1.2;

        const buttonsWidth = cardWidth * 2 + gapSize;
        const buttonsHeight = this.state.guiScale * 6.2;

        const playerListWidth = cardWidth * 2.6;

        const chatWindowHeight = this.state.guiScale * 10;

        const containerHeight = this.state.height - (this.state.guiScale * (CARD_HEIGHT + 5) + 25);
        const containerWidth = buttonsWidth + gapSize * 2 + playerListWidth;

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

        // info panel
        const infoHeight = this.state.guiScale * 4;
        const infoPanel = $r(InfoPanel, { fontSize: this.state.guiScale * 1.2, turnString: this.state.game.turnString, pickupAmount: this.state.game.pickupAmount });
        const infoWrapper = $r('div', { style: { width: playerListWidth, height: infoHeight + 'px', lineHeight: infoHeight + 'px', position: 'absolute', right: '0', top: '0' } }, infoPanel);

        // player list
        const playerListHeight = containerHeight - infoHeight - chatWindowHeight - gapSize;
        const playerList = $r(PlayerListPanel, {
            width: playerListWidth, height: playerListHeight, guiScale: this.state.guiScale, players: this.state.game.players,
            turn: this.state.game.turn, skip: this.state.game.skip, direction: this.state.game.direction, yourId: this.state.game.yourId
        });
        const playerListWrapper = $r('div', { key: 'plp', style: { position: 'absolute', textAlign: 'right', right: '0', top: infoHeight + 'px', width: playerListWidth, height: playerListHeight } }, playerList);

        // chat window
        const chatWindow = $r(ChatWindow, { ref: this.chatRef, width: playerListWidth, height: chatWindowHeight, guiScale: this.state.guiScale, chat: this.state.game.chat });
        const chatWindowWrapper = $r('div', {
            key: 'cw', className: 'panel panel-default', style: { position: 'absolute', width: playerListWidth, height: chatWindowHeight, right: '0', bottom: '0', margin: '0' }
        }, chatWindow);


        // container to hold everything in the UI
        const container = $r('div', {
            key: 'ctr', style: { margin: 'auto', position: 'relative', width: containerWidth + 'px', height: containerHeight + 'px' }
        }, [deckImage, discardWrapper, planningWrapper, buttonsWrapper, infoWrapper, playerListWrapper, chatWindowWrapper]);

        return [container, scroller, popup];
    }
}