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

let socket;

try {
    socket = new WebSocketWrapper('ws://' + window.location.host + '/api/ws');
} catch {
    socket = new WebSocketWrapper('wss://' + window.location.host + '/api/ws');
}

socket.socket.onopen = () => console.log('== Socket opened');
socket.socket.onclose = () => console.log('== Socket closed');

export default socket;
