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

        const close = $r('button', { onClick: () => { gui.closePopup(); }, className: 'btn btn-primary' }, "Exit");

        return $r('div', { className: 'panel panel-default', style: { left: '25%', right: '25%', top: '25%', width: '50%', height: '50%', position: 'fixed', zIndex: '9999' } }, close);
    }
}