class WebSocketWrapper {
    constructor(url) {
        this.socket = new WebSocket(url);
        this.actionMap = {}

        this.socket.onmessage = (event) => {
            const data = JSON.parse(event.data);
            const action = data.action;
            const callBack = this.actionMap[action];
            if (callBack) callBack(data.data);
        };

        this.onopen = this.onopen.bind(this);
        this.onerror = this.onerror.bind(this);
        this.send = this.send.bind(this);
        this.on = this.on.bind(this);
        this.off = this.off.bind(this);
    }

    onopen(callBack) {
        this.socket.onopen = callBack;
    }

    onerror(callBack) {
        this.socket.onerror = callBack;
    }

    send(data) {
        this.socket.send(JSON.stringify(data));
    }

    on(action, callBack) {
        this.actionMap[action] = callBack;
    }

    off(action) {
        delete this.actionMap[action];
    }
}


const socket = new WebSocketWrapper('ws://' + window.location.host + '/api/ws');

export default socket;