import ReconnectingWebSocket from 'reconnecting-websocket';
import ACTION from '../util/action';


class WebSocketWrapper {
    constructor(url) {
        this.socket = new ReconnectingWebSocket(url, [], {
            minReconnectionDelay: 100,
            maxReconnectionDelay: 1000,
        });
        this.actionMap = {}

        this.socket.onmessage = (event) => {
            const data = JSON.parse(event.data);
            const action = data.action;
            const callBack = this.actionMap[action];
            if (callBack) callBack(data.data);
        };

        this.onopen = this.onopen.bind(this);
        this.onclose = this.onclose.bind(this);
        this.onerror = this.onerror.bind(this);
        this.send = this.send.bind(this);
        this.on = this.on.bind(this);
        this.off = this.off.bind(this);
    }

    onopen(callBack) {
        this.socket.onopen = callBack;
    }

    onclose(callBack) {
        this.socket.onclose = callBack;
    }

    onerror(callBack) {
        this.socket.onerror = callBack;
    }

    send(data) {
        const strData = JSON.stringify(data);
        this.socket.send(strData);
    }

    on(action, callBack) {
        this.actionMap[action] = callBack;
    }

    off(action) {
        delete this.actionMap[action];
    }
}



export const createSocket = (peerId, roomId) => {
    let socket = getExistingSocket();
    if (socket) {
        return socket;
    }

    let wsProtocol = 'ws://';
    if (window.location.protocol === 'https:') {
        wsProtocol = 'wss://';
    }
    socket = new WebSocketWrapper(wsProtocol + window.location.host + '/api/ws');

    socket.socket.onopen = () => {
        const data = JSON.stringify({
            action: ACTION.RECONNECT,
            data: {
                peerId,
                roomId
            }
        });
        socket.socket.send(data);
    }
    window.socket = socket;
    return socket;
}

const getExistingSocket = () => {
    if (window.socket) {
        return socket;
    }
    return null;
}

export const closeWebSocket = () => {
    delete window.socket;
}