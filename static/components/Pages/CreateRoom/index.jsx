import React, {useContext, useState} from "react";

import css from './style.css';
import {Input} from "../../styled/Input";
import {Button} from "../../styled/Btn";
import {useHistory, useParams} from "react-router";
import {postRoom} from "../../../api/room";
import {MainContext} from "../../App/context";

export const CreateRoom = () => {
    const {id: roomId} = useParams();
    const history = useHistory();

    const {email: [inputEmail, setInputEmail]} = useContext(MainContext);
    const {name: [inputName, setInputName]} = useContext(MainContext);
    const {organizer: [, setIsOrganizer]} = useContext(MainContext);

    const handleSubmit = (e) => {
        e.preventDefault();
        if(typeof roomId !== "undefined") {
            setIsOrganizer(false);
            history.push(`/room/${roomId}`);
        } else {
            postRoom().then((url) => {
                if (Boolean(url)) {
                    setIsOrganizer(true);
                    history.push(`/room/${url}`);
                }
            })
        }
    };

    return (
        <div className={css.body}>
            <h1 className={css.head}>ChebureckMeet</h1>
            <div className={css.form}>
                <Input
                    placeholder='Email'
                    value={inputEmail}
                    type="email"
                    onChange={event => setInputEmail(event.target.value)}
                />
                <Input
                    placeholder='Name'
                    value={inputName}
                    type="text"
                    required
                    onChange={event => setInputName(event.target.value)}
                />
            </div>
            <Button onClick={handleSubmit}>Go</Button>
        </div>
    )


};