const $r = React.createElement

/**
 * The scroll panel at the bottom which shows all your cards
 */
class CardScroller extends React.Component {

    render() {
        return $r('div', { style: { width: '100%', height: this.props.height, backgroundColor: '#ff0', position: 'fixed', bottom: '0px' } });
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

        this.state = { width: 0, height: 0, guiScale: 0 };
    }

    /**
     * Update the size of the gui when resizing the window
     */
    updateSize = () => {
        const width = window.innerWidth / MIN_WIDTH;
        const height = window.innerHeight / MIN_HEIGHT;
        let guiScale;
        if (width < height) guiScale = width;
        else guiScale = height;
        this.setState({ width: window.innerWidth, height: window.innerHeight, guiScale: guiScale });
    }

    /**
     * Add resize listener
     */
    componentDidMount() {
        window.addEventListener('resize', this.updateSize);
        this.updateSize();
    }

    /**
     * Remove window resize listener
     */
    componentWillUnmount() {
        window.removeEventListener('resize', this.updateSize);
    }

    /**
     * Render the entire game
     */
    render() {
        return $r(CardScroller, { height: this.state.guiScale * (CARD_HEIGHT + 6) });
    }
}