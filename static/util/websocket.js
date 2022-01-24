import ReconnectingWebSocket from 'reconnecting-websocket';
import ACTION from '../util/action';


class WebSocketWrapper {
    constructor(url) {
        this.socket = new ReconnectingWebSocket(url);
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
        this.socket.send(JSON.stringify(data));
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

    try {
        socket = new WebSocketWrapper('ws://' + window.location.host + '/api/ws');
    } catch {
        socket = new WebSocketWrapper('wss://' + window.location.host + '/api/ws');
    }
    socket.socket.onopen = () => {
        console.log('LOG: Socket opened');
        socket.socket.send(JSON.stringify({
            action: ACTION.RECONNECT,
            data: {
                peerId,
                roomId
            }
        }));
    }
    socket.socket.onclose = () => console.log('LOG: Socket closed');
    window.socket = socket;
    return socket;
}

const getExistingSocket = () => {
    if (window.socket) {
        return socket;
    }
    console.log('LOG: No socket');
    return null;
}