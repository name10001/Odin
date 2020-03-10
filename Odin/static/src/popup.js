/*

popup.js is for gui elements that go over the top of the main gui

*/

/**
 * Wrapper for popup windows.
 * When requested, a popup may be generated
 */
class Popup extends React.Component {
    constructor(props) {
        super(props);

        this.state = { createComponent: props.popup.createPopup, canClose: props.popup.canClose, closeFunction: props.popup.closeFunction };
    }

    /**
     * Open a new popup
     * @param {Function} createComponent prevent warnings by having key: '1'
     * @param {Boolean} canClose 
     */
    openPopup(popup) {
        this.setState({ createComponent: popup.createPopup, canClose: popup.canClose, closeFunction: popup.closeFunction });
    }

    /**
     * Close the popup
     */
    closePopup(doCloseFunction) {
        if (this.state.closeFunction && doCloseFunction) {
            this.state.closeFunction();
        }
        this.setState({ createComponent: null, canClose: true, closeFunction: undefined });
    }

    render() {
        if (this.state.createComponent) {
            let backgroundDiv;
            // make a background that you can click on to exit
            if (this.state.canClose) {
                backgroundDiv = $r('div', { key: '2', onClick: () => { this.closePopup(true) }, style: { left: '0', top: '0', width: '100%', height: '100%', position: 'fixed', zIndex: '9998', backgroundColor: '#000', opacity: '0.5' } });
            }
            // make a background that prevents you from clicking the background
            else {
                backgroundDiv = $r('div', { key: '2', style: { left: '0', top: '0', width: '100%', height: '100%', position: 'fixed', zIndex: '9998', backgroundColor: '#000', opacity: '0.5' } });
            }
            return [backgroundDiv, this.state.createComponent()];
        }
        else {
            return "";
        }
    }
}

/**
 * Get the dimensions of the window given a ratio such that it fills 80% of the width or height
 * @param {Number} windowRatio 
 */
function getPopupDimensions(windowRatio) {
    const height1 = window.innerHeight * 0.8;
    const height2 = window.innerWidth * 0.8 * windowRatio;

    const height = Math.min(height1, height2);
    const width = height / windowRatio;

    const left = window.innerWidth / 2 - width / 2;
    const top = window.innerHeight / 2 - height / 2;


    return { width, height, left, top };
}

class HelpPopup extends React.Component {
    constructor(props) {
        super(props);
    }

    render() {
        // size calculations
        const dim = getPopupDimensions(12.0 / 10.0);

        const cardWidth = dim.width / 4;


        // header
        const title = $r('span', { key: '1', style: { fontSize: dim.height * 0.05 + 'px', float: 'left' } }, this.props.card.name);
        const close = $r('button', {
            key: '2', onClick: () => { gui.closePopup(false); }, className: 'btn btn-primary', style: {
                display: 'inline-block', float: 'right', fontSize: dim.height * 0.03 + 'px', height: '100%', lineHeight: '100%'
            }
        }, "X");

        const header = $r('div', { key: '1', className: 'card-header', style: { height: dim.height * 0.1 + 'px', padding: '2%' } }, [title, close]);

        // body
        const image = $r('img', { key: '1', alt: this.props.card.name, width: cardWidth, height: cardWidth / CARD_RATIO, src: this.props.card.url });

        const effectTitle = $r('h5', { key: '1', style: { fontSize: dim.height * 0.04 + 'px' } }, "Effects");
        const effect = $r('p', { key: '2', style: { fontSize: dim.height * 0.025 + 'px' } }, this.props.card.effectDescription);
        const compatTitle = $r('h5', { key: '3', style: { fontSize: dim.height * 0.04 + 'px' } }, "Compatibility");
        const compat = $r('p', { key: '4', style: { fontSize: dim.height * 0.025 + 'px' } }, this.props.card.compatibilityDescription);
        const pickupChain = $r('p', { key: '5', style: { fontSize: dim.height * 0.025 + 'px' } }, "Pickup chains: " + (this.props.card.compatiblePickup ? "Compatible" : "Incompatible"));

        const body = $r('div', { key: '2', className: 'card-body' }, [image, effectTitle, effect, compatTitle, compat, pickupChain]);



        // final creation
        return $r('div', { className: 'card', style: { left: dim.left + 'px', top: dim.top + 'px', width: dim.width + 'px', height: dim.height + 'px', position: 'fixed', zIndex: '9999' } }, [header, body]);
    }
}

class QuestionPopup extends React.Component {
    constructor(props) {
        super(props);

        this.state = { pickedOptions: [] };
    }

    /**
     * When you pick one of the options on the window
     * @param {*} optionId 
     */
    pickOption(optionId) {
        if (this.props.question['number to pick'] <= this.state.pickedOptions.length) return;

        const options = this.state.pickedOptions;
        options.push(optionId);
        this.setState({ pickedOptions: options });

        if (this.props.question['number to pick'] == 1) {
            game.pickOption(optionId);
            gui.closePopup(false);
        }

    }

    /**
     * Confirm your selection of options.
     * This should only work if all options are selected.
     */
    confirmSelection() {
        if (this.props.question['number to pick'] == this.state.pickedOptions.length) {
            game.pickOptions(this.state.pickedOptions);
            gui.closePopup(false);
        }

    }

    /**
     * Undo 1 selection
     */
    undo() {
        const options = this.state.pickedOptions;
        options.length--;
        this.setState({ pickedOptions: options });
    }

    /**
     * Undo all your selections
     */
    undoAll() {
        this.setState({ pickedOptions: [] });
    }

    /**
     * Add resize listener
     */
    componentDidMount() {
        if (this.props.question['type'] != 'cards') return;

        const id = 'option-card-scroller';
        // IE9, Chrome, Safari, Opera
        document.getElementById(id).addEventListener("mousewheel", (e) => scrollHorizontally(e, id, 120), false);
        // Firefox
        document.getElementById(id).addEventListener("DOMMouseScroll", (e) => scrollHorizontally(e, id, 120), false);
    }

    render() {

        // size calculations
        const dim = getPopupDimensions(11.0 / 10.0);

        const cardWidth = dim.width / 5;
        const cardHeight = cardWidth / CARD_RATIO;

        // header
        const title = $r('span', { key: '1', style: { fontSize: dim.height * 0.04 + 'px' } }, this.props.question["title"]);
        let innerHeader = title;

        if (this.props.question["allow cancel"]) {
            const close = $r('button', {
                key: '2', onClick: () => { gui.closePopup(true); }, className: 'btn btn-primary', style: {
                    display: 'inline-block', float: 'right', fontSize: dim.height * 0.03 + 'px', height: '100%', lineHeight: '100%'
                }
            }, "X");
            innerHeader = [close, title];
        }

        const header = $r('div', { key: '1', className: 'card-header', style: { padding: '2%', borderColor: '#ccc' } }, innerHeader);

        // body
        let body;

        // buttons
        if (this.props.question["type"] == 'buttons') {
            const image = $r('img', { key: '1', width: cardWidth, height: cardHeight, src: this.props.question["image"], style: { float: 'right' } });
            const buttons = [];

            for (const optionId of Object.keys(this.props.question["options"])) {
                const optionString = this.props.question["options"][optionId];

                const button = $r('button', {
                    key: optionId, onClick: () => this.pickOption(optionId), className: 'btn btn-primary btn-block',
                    style: {
                        fontSize: dim.height * 0.03 + 'px'
                    }
                }, optionString);

                buttons.push(button);
            }

            const buttonScroller = $r('div', { key: '2', style: { width: '70%', height: cardHeight * 2 + 'px', overflowY: 'auto' } }, buttons);

            body = $r('div', { key: '2', className: 'card-body', style: { padding: '2%'} }, [image, buttonScroller]);
        }
        // card selector
        else if (this.props.question["type"] == 'cards') {

            const elements = [];

            const pickedCardIds = this.state.pickedOptions;

            if (this.props.question["number to pick"] > 1) {
                // cards you've picked so far
                const pickedCards = [];
                for (const id of pickedCardIds) {
                    const name = this.props.question["options"][id];
                    const url = game.allCards[name].url;
                    pickedCards.push(url);
                }

                const selectedCards = $r(CardPile, { height: cardHeight * 1.4, guiScale: cardHeight / CARD_HEIGHT, cards: pickedCards, maxGap: cardHeight * 0.2, alignment: 'bottom-top', grey: false });

                // confirm button
                const confirmProps = { key: 'cb', className: 'btn btn-primary btn-block', style: { fontSize: dim.height * 0.03 + 'px' } };
                if (this.props.question['number to pick'] == this.state.pickedOptions.length) {
                    confirmProps.onClick = () => this.confirmSelection();
                }
                else {
                    confirmProps.disabled = true;
                }

                const confirmButton = $r('button', confirmProps, 'Confirm');

                // undo button
                const undoProps = { key: 'ub', className: 'btn btn-primary btn-block', style: { fontSize: dim.height * 0.03 + 'px' } };
                if (this.state.pickedOptions.length > 0) {
                    undoProps.onClick = () => this.undo();
                }
                else {
                    undoProps.disabled = true;
                }

                const undoButton = $r('button', undoProps, 'Undo');

                // undo all button
                const undoAllProps = { key: 'uab', className: 'btn btn-primary btn-block', style: { fontSize: dim.height * 0.03 + 'px' } };
                if (this.state.pickedOptions.length > 0) {
                    undoAllProps.onClick = () => this.undoAll();
                }
                else {
                    undoAllProps.disabled = true;
                }

                const undoAllButton = $r('button', undoAllProps, 'Undo All');

                // button div
                const buttonDiv = $r('div', { key: '3', style: { width: '50%', float: 'right' } }, [confirmButton, undoButton, undoAllButton]);

                elements.push($r('div', { key: '4', style: { float: 'left', left: cardWidth / 2 + 'px', position: 'relative' } }, selectedCards));
                elements.push(buttonDiv);
            }
            else {
                dim.top += cardHeight * 0.6;
            }

            // generate card stacks
            const cardStacks = [];
            const nameIndices = {};

            for (const id of Object.keys(this.props.question["options"])) {
                if (pickedCardIds.includes(id)) continue;

                const name = this.props.question["options"][id];
                const url = game.allCards[name].url;

                if (name in nameIndices) {
                    const stack = nameIndices[name];
                    stack.addCard(id);
                }
                else {
                    const stack = new CardStack(id, name, url, true);
                    cardStacks.push(stack);
                    nameIndices[name] = stack;
                }
            }

            // generate card buttons
            const cardButtons = [];
            for (const stack of cardStacks) {
                const button = $r(CardButton, { guiScale: cardWidth / CARD_WIDTH, stack, clickFunction: () => this.pickOption(stack.cardIds[0]) });
                cardButtons.push($r('div', { key: stack.name, style: { display: 'inline-block' } }, button));
            }

            const cardDiv = $r('div', { key: '2', id: 'option-card-scroller', style: { width: dim.width * 0.96 + 'px', overflowX: 'scroll', position: 'absolute', bottom: '0', whiteSpace: 'nowrap' } }, cardButtons);
            elements.push(cardDiv);

            body = $r('div', { key: '2', className: 'card-body', style: { padding: '2%', height: (this.props.question["number to pick"] == 1 ? cardHeight * 1.3 : dim.height * 0.8) + 'px', position: 'relative' } }, elements);
        }
        // unsupported question type (only if backend question asking is bad)
        else {
            body = $r('div', { key: '2', className: 'card-body', style: { padding: '2%' } }, "Unsupported question type: " + this.props.question["type"]);
        }

        // final creation
        return $r('div', { className: 'card', style: { left: dim.left + 'px', top: dim.top + 'px', width: dim.width + 'px', position: 'fixed', zIndex: '9999' } }, [header, body]);
    }
}