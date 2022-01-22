const socket = new WebSocket('ws://' + window.location.host + '/api/ws');

export default socket;