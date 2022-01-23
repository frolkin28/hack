import React from 'react';
import {
    Route,
    Switch,
    Redirect,
    withRouter,
} from "react-router-dom"

import {CreateRoom} from "../Pages/CreateRoom";
import {Room} from "../Pages/Room";
import {NotFoundPage} from "../Pages/NotFoundPage";

export const App = () => (
    <div className="App">
        {/*<Link to="/room">ROOM</Link>*/}
        <Switch path={''} history={history}>
            <Route path='/join/' component={CreateRoom} />
            <Route path='/join/:id' component={CreateRoom} />
            <Route path='/room/:id' component={Room} />
            <Route component={NotFoundPage} />
            <Redirect to='/join/' />
            <Redirect from="/" to="/join/" />
        </Switch>
    </div>
);

export default withRouter(App)