import React, { Component } from 'react';
import {
    Route,
    Switch,
    Redirect,
    withRouter,
    Link
} from "react-router-dom"

import css from './style.css';

import {CreateRoom} from "../Pages/CreateRoom";
import {Room} from "../Pages/Room";


class App extends Component {
    render() {
        const { history } = this.props

        return (
            <div className="App">
                {/*<Link to="/room">ROOM</Link>*/}
                <Switch>
                    <Route history={history} path='/home' component={CreateRoom} />
                    <Route history={history} path='/room' component={Room} />
                    <Redirect from='/' to='/home'/>
                </Switch>
            </div>
        );
    }
}

export default withRouter(App)