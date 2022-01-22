import * as React from 'react';
import socket from '../../util/websocket';
import ACTION from '../../util/action';
import './style.css';

export const App = () => {
    // React.useEffect(() => {
    //     socket.send({ action: ACTION.JOIN, peer_id: 1 });
    //     socket.onmessage = (event) => {
    //         console.log(event.data);
    //     };
    // });
    return (
        <div>
            <h1>Powered by spaceport</h1>
            <p>^_^</p>
        </div>
    );
}