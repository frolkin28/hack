import React from "react";
import {RoundButton, SmallRoundButton} from "../styled/RoundBtn";
import {FontAwesomeIcon} from "@fortawesome/react-fontawesome";


export const IconButton = ({icon, onClick, small=false}) => {
    if (small) {
        return (
            <SmallRoundButton onClick={onClick}>
                <FontAwesomeIcon icon={icon} size="1x" />
            </SmallRoundButton>
        )
    }
    return (
        <RoundButton onClick={onClick}>
            <FontAwesomeIcon icon={icon} size="2x" />
        </RoundButton>
    )
}