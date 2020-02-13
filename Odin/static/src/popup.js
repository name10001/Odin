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
    closePopup() {
        if (this.state.closeFunction) {
            this.state.closeFunction();
        }
        this.setState({ createComponent: null, canClose: true, closeFunction: undefined });
    }

    render() {
        if (this.state.createComponent) {
            let backgroundDiv;
            // make a background that you can click on to exit
            if (this.state.canClose) {
                backgroundDiv = $r('div', { key: '2', onClick: () => { this.closePopup() }, style: { left: '0', top: '0', width: '100%', height: '100%', position: 'fixed', zIndex: '9998' } });
            }
            // make a background that prevents you from clicking the background
            else {
                backgroundDiv = $r('div', { key: '2', style: { left: '0', top: '0', width: '100%', height: '100%', position: 'fixed', zIndex: '9998' } });
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
            key: '2', onClick: () => { gui.closePopup(); }, className: 'btn btn-primary', style: {
                display: 'inline-block', float: 'right', fontSize: dim.height * 0.03 + 'px', height: '100%', lineHeight: '100%'
            }
        }, "X");

        const header = $r('div', { key: '1', className: 'panel-heading', style: { height: dim.height * 0.1 + 'px', padding: '2%' } }, [title, close]);

        // body
        const image = $r('img', { key: '1', alt: this.props.card.name, width: cardWidth, height: cardWidth / CARD_RATIO, src: this.props.card.url });

        const effectTitle = $r('h5', { key: '1', style: { fontSize: dim.height * 0.04 + 'px' } }, "Effects");
        const effect = $r('p', { key: '2', style: { fontSize: dim.height * 0.025 + 'px' } }, this.props.card.effectDescription);
        const compatTitle = $r('h5', { key: '3', style: { fontSize: dim.height * 0.04 + 'px' } }, "Compatibility");
        const compat = $r('p', { key: '4', style: { fontSize: dim.height * 0.025 + 'px' } }, this.props.card.compatibilityDescription);
        const pickupChain = $r('p', { key: '5', style: { fontSize: dim.height * 0.025 + 'px' } }, "Pickup chains: " + (this.props.card.compatiblePickup ? "Compatible" : "Incompatible"));

        const body = $r('div', { key: '2', className: 'panel-body' }, [image, effectTitle, effect, compatTitle, compat, pickupChain]);



        // final creation
        return $r('div', { className: 'panel panel-default', style: { left: dim.left + 'px', top: dim.top + 'px', width: dim.width + 'px', height: dim.height + 'px', position: 'fixed', zIndex: '9999' } }, [header, body]);
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
        const options = this.state.pickedOptions;
        options.push(optionId);
        this.setState({ pickedOptions: options });

        if (this.props.question['number to pick'] == 1) {
            game.pickOption(optionId);
            gui.closePopup();
        }

    }

    /**
     * Confirm your selection of options.
     * This should only work if all options are selected.
     */
    confirmSelection() {
        if (this.props.question['number to pick'] == this.state.pickedOptions.length) {
            game.pickOptions(this.state.pickedOptions);
            gui.closePopup();
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

    render() {
        // size calculations
        const dim = getPopupDimensions(11.0 / 10.0);

        const cardWidth = dim.width / 4;
        const cardHeight = cardWidth / CARD_RATIO;

        // header
        const title = $r('span', { key: '1', style: { fontSize: dim.height * 0.04 + 'px' } }, this.props.question["title"]);
        let innerHeader = title;

        if (this.props.question["allow cancel"]) {
            const close = $r('button', {
                key: '2', onClick: () => { gui.closePopup(); }, className: 'btn btn-primary', style: {
                    display: 'inline-block', float: 'right', fontSize: dim.height * 0.03 + 'px', height: '100%', lineHeight: '100%'
                }
            }, "X");
            innerHeader = [close, title];
        }

        const header = $r('div', { key: '1', className: 'panel-heading', style: { padding: '2%' } }, innerHeader);

        // body
        let body;
        const image = $r('img', { key: '1', width: cardWidth, height: cardHeight, src: this.props.question["image"], style: { float: 'right' } });

        // buttons
        if (this.props.question["type"] == 'buttons') {
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

            body = $r('div', { key: '2', className: 'panel-body', style: { padding: '2%' } }, [image, buttonScroller]);
        }
        // card selector
        else if (this.props.question["type"] == 'cards') {
            // cards you've picked so far
            const pickedCardIds = this.state.pickedOptions;
            const pickedCards = [];
            for (const id of pickedCardIds) {
                pickedCards.push(this.props.question["options"][id]);
            }

            const selectedCards = $r(CardPile, { key: 'sc', height: cardHeight * 1.4, guiScale: cardHeight / CARD_HEIGHT, cards: pickedCards, maxGap: cardHeight * 0.2, alignment: 'bottom-top', grey: false });

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
            const buttonDiv = $r('div', { style: { width: '36%' } }, [confirmButton, undoButton, undoAllButton]);

            // the card scroller
            const cards = [];
            for (const id of Object.keys(this.props.question["options"])) {
                if (id in pickedCardIds) continue;
                cards.push($r('img', { key: id, alt: id, src: game.allCards[this.props.question["options"][id]].url, onClick: () => this.pickOption(id), width: cardWidth, height: cardHeight }));
            }

            const cardDiv = $r('div', { style: { width: dim.width * 0.96 + 'px', overflowX: 'scroll', position: 'absolute', bottom: '0', whiteSpace: 'nowrap' } }, cards);


            body = $r('div', { key: '2', className: 'panel-body', style: { padding: '2%', height: dim.height } }, [image, selectedCards, buttonDiv, cardDiv]);
        }
        // unsupported question type (only if backend question asking is bad)
        else {
            body = $r('div', { key: '2', className: 'panel-body', style: { padding: '2%' } }, "Unsupported question type: " + this.props.question["type"]);
        }

        // final creation
        return $r('div', { className: 'panel panel-default', style: { left: dim.left + 'px', top: dim.top + 'px', width: dim.width + 'px', position: 'fixed', zIndex: '9999' } }, [header, body]);
    }
}