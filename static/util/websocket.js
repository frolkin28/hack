import ACTION from '../util/action';


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


export const reconnectSocket = (peerId, roomId) => {
    console.log('LOG: Socket closed, reconnecting ...');
    const socket = createSocket();
    socket.onopen = () => {
        socket.send({
            action: ACTION.RECONNECT,
            data: {
                peerId,
                roomId
            }
        });
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
    socket.onopen = () => console.log('LOG: Socket opened');
    socket.onclose = (peerId, roomId) => reconnectSocket(peerId, roomId);
    window.socket = socket;
    return socket;
}


export const getExistingSocket = () => {
    if (window.socket) {
        return window.socket;
    }
    console.log('LOG: No socket presents');
    return null;
}
