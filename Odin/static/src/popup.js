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

        this.state = { createComponent: props.createComponent, canClose: props.canClose };
    }

    /**
     * Open a new popup
     * @param {Function} createComponent prevent warnings by having key: '1'
     * @param {Boolean} canClose 
     */
    openPopup(createComponent, canClose) {
        this.setState({ createComponent, canClose });
    }

    /**
     * Close the popup
     */
    closePopup() {
        this.setState({ createComponent: null, canClose: true });
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

class HelpPopup extends React.Component {
    constructor(props) {
        super(props);
    }

    render() {
        // size calculations
        const windowRatio = 12.0 / 10.0;

        const height1 = window.innerHeight * 0.8;
        const height2 = window.innerWidth * 0.8 * windowRatio;

        const height = Math.min(height1, height2);
        const width = height / windowRatio;

        const left = window.innerWidth / 2 - width / 2;
        const top = window.innerHeight / 2 - height / 2;

        const cardWidth = width / 4;


        // header
        const close = $r('button', {
            key: '1', onClick: () => { gui.closePopup(); }, className: 'btn btn-primary', style: {
                display: 'inline-block', float: 'right', fontSize: height * 0.03 + 'px', height: '100%', lineHeight: '100%'
            }
        }, "X");
        const title = $r('span', { key: '2', style: { fontSize: height * 0.05 + 'px', float: 'left' } }, this.props.card.name);

        const header = $r('div', { key: '1', className: 'panel-heading', style: { height: height * 0.1 + 'px', padding: '2%'} }, [close, title]);

        // body
        const image = $r('img', { key: '1', alt: this.props.card.name, width: cardWidth, height: cardWidth / CARD_RATIO, src: this.props.card.url });

        const effectTitle = $r('h5', {key: '1', style: {fontSize: height * 0.04 + 'px'}}, "Effects");
        const effect = $r('p', {key: '2', style: {fontSize: height * 0.025 + 'px'}}, this.props.card.effectDescription);
        const compatTitle = $r('h5', {key: '3', style: {fontSize: height * 0.04 + 'px'}}, "Compatibility");
        const compat = $r('p', {key: '4', style: {fontSize: height * 0.025 + 'px'}}, this.props.card.compatibilityDescription);
        const pickupChain = $r('p', {key: '5', style: {fontSize: height * 0.025 + 'px'}}, "Pickup chains: " + (this.props.card.compatiblePickup ? "Compatible" : "Incompatible"));

        const body = $r('div', { key: '2', className: 'panel-body' }, [image, effectTitle, effect, compatTitle, compat, pickupChain]);



        // final creation
        return $r('div', { className: 'panel panel-default', style: { left: left + 'px', top: top + 'px', width: width + 'px', height: height + 'px', position: 'fixed', zIndex: '9999' } }, [header, body]);
    }
}