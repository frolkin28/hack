import React from "react";
import css from './style.css';

export const NotFoundPage = () => (
    <div className={css.body}>
        <img src="http://2fan.ru/upload/000/u1/5/5/68dbb3d3.png" width="20%" />
        <p className={css.status}>404</p>
        <p className={css.text}>Not Found</p>
    </div>
);
