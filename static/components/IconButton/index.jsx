import React from "react";
import {RoundButton} from "../styled/RoundBtn";
import {FontAwesomeIcon} from "@fortawesome/react-fontawesome";


export const IconButton = ({icon, onClick}) => {
    return (
        <RoundButton onClick={onClick}>
            <FontAwesomeIcon icon={icon} size="2x" />
        </RoundButton>
    )
}