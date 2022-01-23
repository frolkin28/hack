import React from 'react';
import { useEffect } from 'react';
import {
    Route,
    Switch,
    Redirect,
    withRouter,
    Link,
} from "react-router-dom";

import css from './style.css';

import { CreateRoom } from "../Pages/CreateRoom";
import { Room } from "../Pages/Room";
import socket from '../../util/websocket';
import ACTION from '../../util/action';

export const App = () => {
    useEffect(() => {
        socket.on(ACTION.JOIN, (data) => console.log('On', data));
        // socket.off(ACTION.JOIN);
        socket.onopen(() => socket.send(
            { action: ACTION.JOIN, data: { peer_id: 1 } }
        ));
    });

    return (
        <div className="App">
            {/*<Link to="/room">ROOM</Link>*/}
            <Switch path={''} history={history}>
                <Route exact path='/' component={Room} />
                <Route path='/join/' component={CreateRoom} />
                <Route path='/join/:id' component={CreateRoom} />
                <Route path='/room/:id' component={Room} />
                {/*<Route component={NotFoundPage} />*/}
                <Redirect to='/join/' />
            </Switch>
        </div>
    )
};

export default withRouter(App)