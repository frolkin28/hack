import React from "react";
import PulseLoader from "react-spinners/PulseLoader";
import css from './style.css';

export const Spinner = (props) => {
    return (
        <div className={css.spinner}>
            <PulseLoader
                size={30}
                color={"#c7f2ff"}
                loading={props.visible}
            />
        </div>
    )
}