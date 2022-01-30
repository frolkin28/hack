import React from "react";
import css from './style.css';
import { Link } from "react-router-dom";
import { useHistory } from "react-router";

export const NotFoundStreamPage = () => {

    const history = useHistory();
    return (
        <div className={css.body}>
            <img src="http://2fan.ru/upload/000/u1/5/5/68dbb3d3.png" width="20%" />
            <p className={css.status}>We haven`t permission</p>
            <p className={css.text}>Please turn camera and microphone on in permission</p>
            <Link to='/'>Back</Link>
        </div>
    )
}
