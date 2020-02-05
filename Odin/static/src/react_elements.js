const $r = React.createElement


function getButtonStyle(size) {
    size = Math.floor(size);
    return {
        fontSize: size + "px",
        padding: size * 0.3 + "px " + size * 0.6 + "px ",
        margin: "0"
    };
}

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
            style: { margin: Math.floor(this.props.guiScale / 2) + "px", display: 'block' }, className: 'transparent-button', onClick: () => this.props.stack.playSingle()
        }, $r('img', { src: this.props.stack.url, width: cardWidth, height: cardHeight, alt: this.props.stack.name }));

        // help button
        const helpStyle = getButtonStyle(this.props.guiScale * 1.5);
        helpStyle.marginLeft = Math.floor(this.props.guiScale) + "px";

        const help = $r('button', { className: 'btn btn-primary', style: helpStyle }, "?");

        // addall button
        const addAllStyle = getButtonStyle(this.props.guiScale * 1.5);
        addAllStyle.marginRight = Math.floor(this.props.guiScale) + "px";
        addAllStyle.float = "right";

        const addAll = $r('button', {
            className: 'btn btn-primary', style: addAllStyle, onClick: () => this.props.stack.playAll()
        }, "+All");

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

        this.state = { width: 0, height: 0, guiScale: 0, cardStacks: game.yourStacks };
    }

    animatePlayCards() {
        console.log("TODO: ANIMATE");
        game.finishedEvent();
    }

    updateStacks(cardStacks) {
        this.state.cardStacks = cardStacks;
        this.setState(this.state);
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
     * Add resize listener
     */
    componentDidMount() {
        window.addEventListener('resize', () => {
            this.updateSize()
        });
        this.updateSize();
    }

    /**
     * Render the entire game
     */
    render() {
        return $r(CardScroller, { cardStacks: this.state.cardStacks, guiScale: this.state.guiScale });
    }
}