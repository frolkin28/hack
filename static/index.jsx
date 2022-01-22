import * as React from "react";
import * as ReactDOM from "react-dom";
import { BrowserRouter } from "react-router-dom"
import {createBrowserHistory} from 'history'

import App from "./components/App";
import {GlobalStyle} from "./components/styled/styles";

const history = createBrowserHistory()

ReactDOM.render((
    <BrowserRouter history={history}>
        <GlobalStyle />
        <App />
    </BrowserRouter>
), document.getElementById('root')
);