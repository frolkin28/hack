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
import { NotFoundPage } from "../Pages/NotFoundPage";
import { CreateRoom } from "../Pages/CreateRoom";
import { Room } from "../Pages/Room";



export const App = () => {

    return (
        <div className="App">
            {/*<Link to="/room">ROOM</Link>*/}
            <Switch path={''} history={history}>
                <Route exact path='/' component={CreateRoom} />
                <Route path='/join/:id' component={CreateRoom} />
                <Route path='/room/:id' component={Room} />
                <Route component={NotFoundPage} />
                <Redirect to='/join/' from='/' />
            </Switch>
        </div>
    )
};

export default withRouter(App)