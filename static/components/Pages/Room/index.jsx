import * as React from "react";
import {useEffect, useRef, useState} from "react";
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


function layout(clientsNumber = 1) {
    const pairs = Array.from({length: clientsNumber})
        .reduce((acc, next, index, arr) => {
            if (index % 2 === 0) {
                acc.push(arr.slice(index, index + 2));
            }

            return acc;
        }, []);

    const rowsNumber = pairs.length;
    const height = `${100 / rowsNumber}%`;

    return pairs.map((row, index, arr) => {

        if (index === arr.length - 1 && row.length === 1) {
            return [{
                width: '100%',
                height,
            }];
        }

        return row.map(() => ({
            width: '50%',
            height,
        }));
    }).flat();
}


export const Room = () => {
    const {id: roomID} = useParams();
    const {clients, provideMediaRef} = userRtcConnection(roomID);
    const videoLayout = layout(clients.length);


    const stopVideo = () => {
        console.log('stop');
    }


    return (
        <div className={css.body}>
            {/*<IconButton icon={faMinus} />*/}

            <div className={css.bodyPeoples}>
                {clients.map((clientID, index) => (
                    <div
                        className={css.person}
                        style={videoLayout[index]}
                        key={clientID}
                        id={clientID}
                    >
                        <video
                            width='100%'
                            height='100%'
                            ref={instance => {
                                provideMediaRef(clientID, instance);
                            }}
                            autoPlay
                            muted={clientID === 'LOCAL_VIDEO'}
                        />
                    </div>
                ))}
            </div>

            <div className={css.listPeoples}>
                <ul className={css.border}>
                    <li>Элемент списка</li>
                    <li>Элемент списка</li>
                    <li>Элемент списка</li>
                    <li>Элемент списка</li>
                    <li>Элемент списка</li>
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