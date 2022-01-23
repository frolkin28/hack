import * as React from "react";
import {useContext, useEffect, useRef, useState} from "react";
import {useParams} from "react-router";
import {
    faMicrophone,
    faMicrophoneSlash,
    faMinus,
    faPhoneSlash,
    faVideo,
    faVideoSlash
} from "@fortawesome/free-solid-svg-icons";

import css from './style.css';
import {IconButton} from "../../IconButton";
import userRtcConnection from "../../../hooks/userRtcConnection";
import socket from "../../../util/websocket";
import ACTION from "../../../util/action";
import {MainContext} from "../../App/context";
import {Redirect} from "react-router-dom";


export const Room = () => {
    const {id: roomId} = useParams();
    const {email: [inputEmail]} = useContext(MainContext);
    const {name: [inputName]} = useContext(MainContext);
    const {organizer: [isOrganizer]} = useContext(MainContext);

    if (!Boolean(inputEmail) && !Boolean(inputName)) {
        return <Redirect to={`/join/${roomId}`} />
    }

    const {clients, provideMediaRef} = userRtcConnection(roomId);

    const stopVideo = () => {
        console.log('stop');
    }

    window.onbeforeunload = function () {
        socket.send({ action: ACTION.LEAVE, data: {roomId} });
        return "Do you really want to close?";
    };
    console.log(clients);
    return (
        <div className={css.body}>
            <div className={css.bodyPeoples}>
                {clients.map((client) => (
                    <div
                        className={css.person}
                        key={client.peerId}
                        id={client.peerId}
                    >
                        <video
                            width='100%'
                            height='100%'
                            ref={instance => {
                                provideMediaRef(client.peerId, instance);
                            }}
                            autoPlay
                            muted={client.email === inputEmail}
                        />
                        <p>{client.name}</p>
                    </div>
                ))}
            </div>

            <div className={css.listPeoples}>
                <ul className={css.border}>
                    {clients.map((client) => (
                        <li className={css.name} key={client.peerId} >
                            {client.name.slice(0, 8)}
                            {isOrganizer ? <IconButton icon={faMinus} small /> : null}
                        </li>
                    ))}
                </ul>
            </div>

            <div className={css.footer}>
                {true
                    ? <IconButton icon={faMicrophone} />
                    : <IconButton icon={faMicrophoneSlash} />
                }
                {true
                    ? <IconButton icon={faVideo} onClick={stopVideo}/>
                    : <IconButton icon={faVideoSlash} />
                }
                <IconButton icon={faPhoneSlash}/>
            </div>
        </div>
    );
};