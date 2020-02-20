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

        this.state = { cards: props.cards };
    }

    updateCards(cards) {
        this.setState({ cards });
    }

    render() {
        // calculations such that all cards fit within the stack
        const width = this.props.guiScale * CARD_WIDTH;
        const height = this.props.guiScale * CARD_HEIGHT;
        const totalGap = this.props.height - height;
        const len = this.state.cards.length;
        const gap = Math.min(totalGap / (len - 1), this.props.maxGap);

        const cards = this.state.cards.reduce((result, card, index) => {
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
class ButtonPanel extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            playMessage: props.playMessage,
            playAvaliable: props.playAvaliable,
            undoAvaliable: props.undoAvaliable
        };
    }

    /**
     * Update the buttons
     * @param {*} playMessage message to display on the play button 
     * @param {*} playAvaliable if play button avaliable 
     * @param {*} undoAvaliable if undo buttons avaliable
     */
    update(playMessage, playAvaliable, undoAvaliable) {
        this.setState({ playMessage, playAvaliable, undoAvaliable });
    }

    render() {
        // style of the button in terms of font size
        const btnStyle = getButtonStyle(this.props.guiScale * 1.4);

        // play button
        const playButton = $r('button', this.state.playAvaliable ? { key: '1', onClick: () => game.finishTurn(), className: 'btn btn-primary btn-block', style: btnStyle } : {
            key: '1', disabled: true, className: 'btn btn-primary btn-block', style: btnStyle
        }, this.state.playMessage);

        // size of the gap between buttons
        const gap = this.props.guiScale / 2 + "px";

        // undo button

        const undoButton = $r('div', {
            key: '2', className: 'col-xs-5', style: { padding: gap + " " + gap + " 0 0" }
        }, $r('button', this.state.undoAvaliable ? { onClick: () => game.undo(), className: 'btn btn-primary btn-block', style: btnStyle } : {
            className: 'btn btn-primary btn-block', disabled: true, style: btnStyle
        }, "UNDO"));

        // undo all button
        const undoAllButton = $r('div', {
            key: '3', className: 'col-xs-7', style: { padding: gap + " 0 0 0" }
        }, $r('button', this.state.undoAvaliable ? { onClick: () => game.undoAll(), className: 'btn btn-primary btn-block', style: btnStyle } : {
            className: 'btn btn-primary btn-block', disabled: true, style: btnStyle
        }, "UNDO ALL"));

        return [playButton, undoButton, undoAllButton];
    }


}

/**
 * Represents a singular card button
 * @param {*} props 
 */
function CardButton(props) {
    const cardWidth = props.guiScale * CARD_WIDTH + "px";
    const cardHeight = props.guiScale * CARD_HEIGHT + "px";

    if (props.stack.cardIds.length == 0) {
        return $r('div', { style: { display: 'block', width: cardWidth, height: cardHeight, margin: props.guiScale / 2 + "px", position: 'relative' } });
    }

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
    helpStyle.marginLeft = props.guiScale * 0.8 + "px";

    const help = $r('button', { onClick: () => gui.openPopup(() => $r(HelpPopup, { key: '1', card: game.allCards[props.stack.name] }), true), className: 'btn btn-primary', style: helpStyle }, "?");

    // addall button
    const addAllStyle = getButtonStyle(props.guiScale * 1.3);
    addAllStyle.marginRight = props.guiScale * 0.8 + "px";
    addAllStyle.float = "right";

    const addAll = $r('button', props.stack.allowedToPlay ? {
        className: 'btn btn-primary', style: addAllStyle, onClick: () => props.stack.playAll()
    } : {
            className: 'btn btn-primary', style: addAllStyle, disabled: true
        }, "+ALL");

    // return entire card stack
    return $r('div', { id: 'hand-' + props.stack.name, style: { width: width, display: "inline-block", paddingBottom: props.guiScale / 2 + "px", lineHeight: 'normal', verticalAlign: 'bottom' } }, cardButton, help, addAll);
}

/**
 * Get the position in your hand of a specific card (by card name)
 * @param {*} cardName name of the card, if non-existant then it comes from the centre
 */
function getHandCardPosition(cardName) {
    let element = document.getElementById('hand-' + cardName);

    if (!element) {
        let x = window.innerWidth / 2 - gui.state.guiScale * CARD_WIDTH;
        let y = window.innerHeight - gui.state.guiScale * (CARD_HEIGHT + 5) - 20;

        return { x, y };

    }

    const bounds = element.getBoundingClientRect();
    let x = bounds.left;
    let y = bounds.top;

    // if off the screen then adjust
    if (x < -gui.state.guiScale * CARD_WIDTH) x = -gui.state.guiScale * CARD_WIDTH;
    if (x > window.innerWidth) x = window.innerWidth;

    return { x, y };

}

/**
 * Get the position of the planning pile
 */
function getPlanningPileBottomPosition() {
    const bounds = document.getElementById('planning-pile').getBoundingClientRect();
    let x = bounds.left;
    let y = bounds.bottom;

    y -= gui.state.guiScale * CARD_HEIGHT;
    return { x, y };

}


/**
 * Get the position of the planning pile
 */
function getPlanningPileTopPosition() {
    const bounds = document.getElementById('planning-pile').getBoundingClientRect();

    let x = bounds.left;
    let y = bounds.bottom;

    y -= gui.state.guiScale * (game.planningCards.length + CARD_HEIGHT);
    if (y < gui.state.guiScale) y = gui.state.guiScale;
    return { x, y };

}


/**
 * Get the position of the discard pile
 */
function getDiscardPilePosition() {
    const bounds = document.getElementById('discard-pile').getBoundingClientRect();
    let x = bounds.left;
    let y = bounds.bottom;

    y -= gui.state.guiScale * CARD_HEIGHT;
    return { x, y };

}
/**
 * Get the position of the deck pile
 */
function getDeckPosition() {
    const bounds = document.getElementById('deck-pile').getBoundingClientRect();
    let x = bounds.left;
    let y = bounds.top;

    return { x, y };

}

function getPlayerPosition(playerId) {
    const bounds = document.getElementById('player-' + playerId).getBoundingClientRect();
    let x = bounds.left;
    let y = bounds.top + (bounds.bottom - bounds.top) / 2;

    return { x, y };
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

        this.state = { hidden: false, cardStacks: props.cardStacks };
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
        this.setState({ hidden: true, cardStacks: this.state.cardStacks });
    }


    unhide() {
        this.setState({ hidden: false, cardStacks: this.state.cardStacks });
    }

    updateStacks(cardStacks) {
        this.setState({ hidden: this.state.hidden, cardStacks });
    }

    /**
     * Render all card stack panels
     */
    render() {
        const panels = this.state.cardStacks.map((stack) =>
            $r(CardPanel, { key: stack.name, guiScale: this.props.guiScale, stack: stack })
        );

        return $r('div', {
            id: 'card-scroller', style: {
                width: '100%', overflowX: 'scroll', textAlign: 'center', whiteSpace: 'nowrap', lineHeight: this.props.guiScale * (CARD_HEIGHT + 5) + 'px',
                position: 'absolute', bottom: '0px', display: this.state.hidden ? 'none' : 'block'
            }
        }, panels);
    }
}


/**
 * Contains simple text with information about the current turn.
 * Consisting of:
 * - Who's turn it is.
 * - Pickup chain (if any)
 */
class InfoPanel extends React.Component {

    constructor(props) {
        super(props);

        this.state = {
            turnString: props.turnString,
            pickupAmount: props.pickupAmount
        };
    }

    /**
     * Update info panel
     * @param {*} turnString message at the top of the screen 
     * @param {*} pickupAmount pickup amount
     */
    update(turnString, pickupAmount) {
        this.setState({ turnString, pickupAmount });
    }

    render() {
        const turnString = $r('span', { key: '1', style: { color: "#fff", display: 'inline-block', verticalAlign: 'middle', fontSize: this.props.fontSize, float: 'left' } }, this.state.turnString);

        if (this.state.pickupAmount > 0) {
            const pickupString = $r('span', { key: '2', style: { color: "#fff", fontSize: this.props.fontSize, float: 'right' } }, '+' + this.state.pickupAmount);

            return [turnString, pickupString];
        }

        return turnString;
    }
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

        this.state = {
            players: this.props.players,
            yourId: this.props.yourId,
            direction: this.props.direction,
            turn: this.props.turn,
            skip: this.props.skip
        }
    }

    /**
     * Update the player list panel
     * @param {*} players list of players
     * @param {*} yourId your id
     * @param {*} direction direction of turn
     * @param {*} turn current turn index
     * @param {*} skip number of players to skip
     */
    update(players, yourId, direction, turn, skip) {
        this.setState({
            players, yourId, direction, turn, skip
        });
    }

    render() {
        const nPlayers = this.state.players.length;

        if (nPlayers == 0) {
            return "";
        }

        const maxHeight = this.props.guiScale * 4.5;
        const maxGap = this.props.guiScale * 0.8;

        const totalHeight = maxGap + nPlayers * (maxGap + maxHeight);

        let scale = 1;
        if (maxHeight > this.props.height) scale = this.props.height / totalHeight;

        const panels = [];

        let i = this.state.turn;

        do {
            const player = this.props.players[i];

            const panelWidth = i == this.state.turn ? this.props.width : this.props.width * 0.9;

            const playerPanel = $r(PlayerPanel, { player, width: panelWidth, height: maxHeight * scale, isYou: player.id == this.state.yourId });

            panels.push($r('div', {
                key: i, id: 'player-' + player.id, className: 'panel panel-default', style: {
                    width: panelWidth + 'px', height: maxHeight * scale + 'px', margin: maxGap * scale + 'px 0 0 0', display: 'inline-block', textAlign: 'left', position: 'relative'
                }
            }, playerPanel))

            i += this.state.direction;
            if (i < 0) i = nPlayers - 1;
            else if (i >= nPlayers) i = 0;
        } while (i != this.state.turn);

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
        this.animationHandler = React.createRef();
        this.planPileRef = React.createRef();
        this.discardRef = React.createRef();
        this.buttonsRef = React.createRef();
        this.infoRef = React.createRef();
        this.playersRef = React.createRef();
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
    animatePlayCards(cards, fromDeck) {
        if (!fromDeck) {
            for (const card of cards) {
                card['startPos'] = getHandCardPosition(card['name']);
            }
        }

        this.playCardAnimation('play-cards', cards, (card) => {
            if (!fromDeck) game.removeCard(card.id);
            if (card.update) this.getCardScroller().updateStacks(game.yourStacks);
        }, (card) => {
            game.planningCards.push(card);
            if (card.update) this.getPlanningPile().updateCards(game.planningCards.map((card) => card['url']));
        }, getDeckPosition(), getPlanningPileTopPosition(), '/static/sounds/card_play.mp3', this.state.guiScale * CARD_WIDTH, this.state.guiScale * CARD_HEIGHT);
    }

    /**
     * Animate cards moving from planning pile to discard pile
     */
    animateFinishPlayCards(cards) {
        this.playCardAnimation('finish-play-cards', cards, (card) => {
            game.planningCards.splice(0, 1);
            if (card.update) this.getPlanningPile().updateCards(game.planningCards.map((card) => card['url']));
        }, (card) => {
            game.topCards.splice(0, 1);
            game.topCards.push(card.url);

            if (card.update) this.getDiscardPile().updateCards(game.topCards);
        }, getPlanningPileBottomPosition(), getDiscardPilePosition(), '/static/sounds/card_play.mp3', this.state.guiScale * CARD_WIDTH, this.state.guiScale * CARD_HEIGHT);
    }



    /**
     * Animate undo all
     */
    animateUndoAll() {
        const cards = game.planningCards.slice();

        for (const card of cards) {
            card['endPos'] = getHandCardPosition(card['name']);
        }

        this.playCardAnimation('undo-cards', cards, (card) => {
            game.planningCards.pop();
            if (card.update) this.getPlanningPile().updateCards(game.planningCards.map((card) => card['url']));
        }, (card) => {
            game.addCard(card.id, card.name, card.url, false);
            if (card.update) this.getCardScroller().updateStacks(game.yourStacks);
        }, getPlanningPileBottomPosition(), null, '/static/sounds/card_pickup.mp3', this.state.guiScale * CARD_WIDTH, this.state.guiScale * CARD_HEIGHT, 200, true);
    }

    /**
     * Animate single undo
     */
    animateUndo() {
        const card = game.planningCards.pop();
        this.getPlanningPile().updateCards(game.planningCards.map((card) => card['url']));

        this.playCardAnimation('undo-cards', [card], () => { }, () => { }, getPlanningPileTopPosition(), getHandCardPosition(card['name']),
            '/static/sounds/card_pickup.mp3', this.state.guiScale * CARD_WIDTH, this.state.guiScale * CARD_HEIGHT);
    }

    /**
     * Animate pickup cards
     */
    animatePickupFromDeck(cards) {

        this.playCardAnimation('add-cards', cards, () => { }, (card) => {
            game.addCard(card.id, card.name, card.url, false);
            if (card.update) this.getCardScroller().updateStacks(game.yourStacks);
        }, getDeckPosition(), getHandCardPosition(null), '/static/sounds/card_pickup.mp3', this.state.guiScale * CARD_WIDTH, this.state.guiScale * CARD_HEIGHT, 500);
    }

    /**
     * Animate remove cards
     */
    animateRemoveCards(cards) {
        for (const card of cards) {
            card['startPos'] = getHandCardPosition(card['name']);
        }

        this.playCardAnimation('remove-cards', cards, (card) => {
            game.removeCard(card.id);
            if (card.update) this.getCardScroller().updateStacks(game.yourStacks);
        }, (card) => { }, getDeckPosition(), getDeckPosition(), '/static/sounds/card_play.mp3', this.state.guiScale * CARD_WIDTH, this.state.guiScale * CARD_HEIGHT, 350);
    }

    /**
     * Animate pickup from player
     */
    animatePickupFromPlayer(cards, from) {
        const width = this.state.guiScale * CARD_WIDTH / 2;
        const height = this.state.guiScale * CARD_HEIGHT / 2;

        const position = getPlayerPosition(from);
        position.y -= height / 2;

        const midPosition = { x: position.x - width * 2, y: position.y };
        const midPosition2 = { x: midPosition.x - width, y: midPosition.y - height };

        this.playCardAnimation('add-cardsA', cards, () => { }, () => { }, position, midPosition, undefined, width, height, 300, false, 0, false);
        this.playCardAnimation('add-cardsB', cards, () => { }, (card) => {
            game.addCard(card.id, card.name, card.url, false);

            if (card.update) this.getCardScroller().updateStacks(game.yourStacks);
        }, midPosition2, getHandCardPosition(null), '/static/sounds/card_pickup.mp3', this.state.guiScale * CARD_WIDTH, this.state.guiScale * CARD_HEIGHT, 400, false, 300);
    }

    /**
     * Animate give cards to player
     */
    animateRemoveCardsToPlayer(cards, to) {
        // deep clone the cards
        const cards2 = [];

        for (const card of cards) {
            cards2.push({ 'startPos': getHandCardPosition(card['name']), 'name': card['name'], 'id': card['id'], 'url': card['url'] });
        }

        const width = this.state.guiScale * CARD_WIDTH / 2;
        const height = this.state.guiScale * CARD_HEIGHT / 2;

        const position = getPlayerPosition(to);
        position.y -= height / 2;

        const midPosition = { x: position.x - width * 2, y: position.y };
        const midPosition2 = { x: midPosition.x - width, y: midPosition.y - height };

        this.playCardAnimation('remove-cardsA', cards2, (card) => {
            game.removeCard(card.id);
            if (card.update) this.getCardScroller().updateStacks(game.yourStacks);
        }, (card) => { }, getHandCardPosition(null), midPosition2, undefined, this.state.guiScale * CARD_WIDTH, this.state.guiScale * CARD_HEIGHT, 400, false, 0, false);
        this.playCardAnimation('remove-cardsB', cards, () => { }, () => { }, midPosition, position, '/static/sounds/card_play.mp3', width, height, 300, false, 400);
    }

    /**
     * Animate playing cards
     */
    animatePlayerPickup(player, count) {
        const cards = [];
        for (let i = 0; i < count; i++) {
            cards.push({ id: player + "_" + count, name: '', url: '/static/cards/back.png' });
        }

        const width = this.state.guiScale * CARD_WIDTH / 2;
        const height = this.state.guiScale * CARD_HEIGHT / 2;

        const position = getPlayerPosition(player);
        position.y -= height / 2;

        this.playCardAnimation('player-pickup', cards, () => { }, () => { }, getDeckPosition(), position, '/static/sounds/card_pickup.mp3', width, height);

    }

    /**
     * Animate player removing cards
     */
    animatePlayerRemove(player, count) {
        const cards = [];
        for (let i = 0; i < count; i++) {
            cards.push({ id: player + "_" + count, name: '', url: '/static/cards/back.png' });
        }

        const width = this.state.guiScale * CARD_WIDTH / 2;
        const height = this.state.guiScale * CARD_HEIGHT / 2;

        const position = getPlayerPosition(player);
        position.y -= height / 2;

        this.playCardAnimation('player-pickup', cards, () => { }, () => { }, position, getDeckPosition(), '/static/sounds/card_play.mp3', width, height);
    }

    /**
     * Animate playing cards
     */
    animatePlayerCardTransfer(from, to, count) {
        const cards = [];
        for (let i = 0; i < count; i++) {
            cards.push({ id: player + "_" + count, name: '', url: '/static/cards/back.png' });
        }

        const width = this.state.guiScale * CARD_WIDTH / 2;
        const height = this.state.guiScale * CARD_HEIGHT / 2;

        const fromPos = getPlayerPosition(from);
        fromPos.y -= height / 2;

        const toPos = getPlayerPosition(to);
        toPos.y -= height / 2;

        const midPos = { x: fromPos.x - width * 2, y: (fromPos.y + toPos.y) / 2 };

        this.playCardAnimation('player-transferA', cards, () => { }, () => { }, fromPos, midPos, undefined, width, height, 200, false, 0, false);
        this.playCardAnimation('player-transferB', cards, () => { }, () => { }, midPos, toPos, '/static/sounds/card_pickup.mp3', width, height, 200, false, 200);
    }

    /**
     * Play an animation of cards moving from one end of the screen to another
     * @param {String} id Identification of the animation
     * @param {Array} cards Array of cards
     * @param {Function} moveStartFunction function to call when a card starts moving
     * @param {Function} moveEndFunction function to call when a card starts moving
     * @param {*} startPos Starting position 
     * @param {*} endPos Ending position
     * @param {Number} cardWidth width of the cards
     * @param {Number} cardHeight height of the cards
     * @param {Number} travelTime time for a card to travel from the start to the end (ms)
     * @param {Number} gap gap between each card beginning to move
     * @param {Boolean} reverse if the z-depth of each card should be reversed
     * @param {Number} delay ms delay before the animation starts
     * @param {Number} finishEvent if eventHandler.finishedEvent() should be called
     */
    playCardAnimation(id, cards, moveStartFunction, moveEndFunction, startPos, endPos, sound, cardWidth, cardHeight, travelTime = 200, reverse = false, delay = 0, finishEvent = true) {
        let maxWaitTime = travelTime * 6;
        let gap = (maxWaitTime - maxWaitTime * Math.exp(-0.1 * cards.length)) / cards.length;

        // minimum gap between sounds is 50ms
        /*const minSoundGap = 50;
        if (gap >= minSoundGap) {
            for (const card of cards) {
                card['sound'] = sound;
            }
        }
        else {
            // prevent too many sounds from being played at the same time
            let i = minSoundGap;

            for (const card of cards) {
                if (i >= minSoundGap) {
                    card['sound'] = sound;
                    i -= 50;
                }
                i += gap;
            }

        }*/

        // generate unique id
        while (this.getAnimationHandler().hasAnimation(id)) {
            id += "_";
        }

        this.getAnimationHandler().playAnimation(id, () => $r(CardAnimation, {
            key: id, id, moveStartFunction, moveEndFunction, startPos, endPos, cardWidth, cardHeight, cards, travelTime, gap, reverse, sound, delay, finishEvent
        }), finishEvent ? () => eventHandler.finishedEvent() : () => { });

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
        this.getPlanningPile().updateCards(game.planningCards.map((card) => card['url']));
        this.getCardScroller().updateStacks(game.yourStacks);
        this.getDiscardPile().updateCards(game.topCards);
        this.getPlayerList().update(game.players, game.yourId, game.direction, game.turn, game.skip);
        this.getButtons().update(game.getPlayButtonMessage(), game.playAvaliable(), game.undoAvaliable());
        this.getInfoPanel().update(game.turnString, game.pickupAmount);
    }

    /**
     * Get the animation handler object
     */
    getAnimationHandler() {
        return this.animationHandler.current;
    }

    /**
     * Get the card scroller object
     */
    getCardScroller() {
        return this.cardsRef.current;
    }

    /**
     * Get the planning pile object
     */
    getPlanningPile() {
        return this.planPileRef.current;
    }

    /**
     * Get the discard pile object
     */
    getDiscardPile() {
        return this.discardRef.current;
    }

    /**
     * Get the button objects
     */
    getButtons() {
        return this.buttonsRef.current;
    }

    /**
     * Get the info panel
     */
    getInfoPanel() {
        return this.infoRef.current;
    }

    /**
     * Get the player list panel
     */
    getPlayerList() {
        return this.playersRef.current;
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

        // animation handler
        const animationHandler = $r(AnimationHandler, { key: 'ani', ref: this.animationHandler });

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
        const discardPile = $r(CardPile, { height: discardHeight, guiScale: this.state.guiScale, cards: this.state.game.topCards, maxGap: discardHeight / 3, alignment: 'top-bottom', grey: true, ref: this.discardRef });
        const discardWrapper = $r('div', { key: 'dp', id: 'discard-pile', style: { width: cardWidth + "px", height: discardHeight, position: 'absolute', bottom: buttonsHeight + gapSize + 'px' } }, discardPile);

        // planning pile
        const planningHeight = containerHeight - buttonsHeight - gapSize * 2;
        const planningCards = this.state.game.planningCards.map((card) => card['url']);
        const planningPile = $r(CardPile, {
            height: planningHeight, guiScale: this.state.guiScale, cards: planningCards,
            maxGap: this.state.guiScale, alignment: 'bottom-bottom', grey: false, ref: this.planPileRef
        });
        const planningWrapper = $r('div', {
            key: 'pp', id: 'planning-pile', style: {
                width: cardWidth + "px", height: planningHeight, position: 'absolute', bottom: buttonsHeight + gapSize + 'px', left: cardWidth + gapSize + 'px'
            }
        }, planningPile);

        // deck
        const deckTop = (containerHeight - discardHeight - buttonsHeight - gapSize - cardHeight) / 2;
        const deckImage = $r('img', { src: '/static/cards/back.png', id: 'deck-pile', key: 'di', style: { width: cardWidth + 'px', height: cardHeight + 'px', position: 'absolute', top: deckTop + 'px' } });

        // button panel


        const buttons = $r(ButtonPanel, {
            undoAvaliable: this.state.game.undoAvaliable(), playMessage: this.state.game.getPlayButtonMessage(),
            playAvaliable: this.state.game.playAvaliable(), guiScale: this.state.guiScale, ref: this.buttonsRef
        });
        const buttonsWrapper = $r('div', { key: 'bp', style: { position: 'absolute', bottom: '0', width: buttonsWidth + "px" } }, buttons);

        // info panel
        const infoHeight = this.state.guiScale * 4;
        const infoPanel = $r(InfoPanel, { fontSize: this.state.guiScale * 1.2, turnString: this.state.game.turnString, pickupAmount: this.state.game.pickupAmount, ref: this.infoRef });
        const infoWrapper = $r('div', { style: { width: playerListWidth, height: infoHeight + 'px', lineHeight: infoHeight + 'px', position: 'absolute', right: '0', top: '0' } }, infoPanel);

        // player list
        const playerListHeight = containerHeight - infoHeight - chatWindowHeight - gapSize;
        const playerList = $r(PlayerListPanel, {
            width: playerListWidth, height: playerListHeight, guiScale: this.state.guiScale, players: this.state.game.players,
            turn: this.state.game.turn, skip: this.state.game.skip, direction: this.state.game.direction, yourId: this.state.game.yourId, ref: this.playersRef
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

        return [container, scroller, popup, animationHandler];
    }
}