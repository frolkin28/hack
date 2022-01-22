import React, {useState} from "react";

import css from './style.css';
import {Input} from "../../styled/Input";
import {Button} from "../../styled/Btn";

export const CreateRoom = () => {
    const [inputEmail, setInputEmail] = useState('');
    const [inputName, setInputName] = useState('');

    const handleSubmit = (e) => {
        e.preventDefault();
        console.log(inputEmail);
        console.log(inputName);
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