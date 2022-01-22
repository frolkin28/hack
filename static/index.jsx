import * as React from "react";
import * as ReactDOM from "react-dom";
import { BrowserRouter } from "react-router-dom"
import {createBrowserHistory} from 'history'

import App from "./components/App";

const history = createBrowserHistory()

ReactDOM.render((
    <BrowserRouter history={history}>
        <App/>
    </BrowserRouter>
), document.getElementById('root')
);