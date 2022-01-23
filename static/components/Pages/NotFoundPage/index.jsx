import React from "react";
import {Link} from "react-router-dom"
import css from './style.css';

export const NotFoundPage = () => (
    <div className={css.body}>
        <p className={css.status}>404</p>
        <p className={css.text}>Not Found</p>
        <Link to={"/join/"} ><p className={css.text}>TRY AGAIN</p></Link>
    </div>
);
