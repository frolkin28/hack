import React, {useContext, useState} from "react";

import css from './style.css';
import {Input} from "../../styled/Input";
import {Button} from "../../styled/Btn";
import {useHistory, useParams} from "react-router";
import {postRoom} from "../../../api/room";
import {MainContext} from "../../App/context";
import {Link} from "react-router-dom";

export const CreateRoom = () => {
    const {id: roomId} = useParams();
    const history = useHistory();
    const [errors, setErrors] = useState('')

    const {email: [inputEmail, setInputEmail]} = useContext(MainContext);
    const {name: [inputName, setInputName]} = useContext(MainContext);
    const {organizer: [, setIsOrganizer]} = useContext(MainContext);

    const HandleInputEmail = (value) => {
        setInputEmail(value);
        const emailValid = value.match(/^([\w.%+-]+)@([\w-]+\.)+([\w]{2,})$/i);
        setErrors(emailValid ? '' : 'Invalid email.');
    }

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
            <h2><Link to='/' className={css.head}>ChebureckMeet</Link></h2>
            <div className={css.form}>
                <Input
                    placeholder='Email'
                    value={inputEmail}
                    type="email"
                    onChange={event => HandleInputEmail(event.target.value)}
                />
                <Input
                    placeholder='Name'
                    value={inputName}
                    type="text"
                    required
                    onChange={event => setInputName(event.target.value)}
                />
            </div>
            <p className={css.error}>{errors}</p>
            <Button onClick={handleSubmit} disabled={Boolean(errors)}>Go</Button>
        </div>
    )


};