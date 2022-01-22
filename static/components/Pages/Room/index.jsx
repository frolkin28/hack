import * as React from "react";
import {useEffect, useRef, useState} from "react";
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


export const Room = () => {
    // const [localStream, setLocalStream] = useState(null);
    // let remoteStream = null;
    //
    // const videoEl = useRef(null)

    // useEffect(() => {
    //     if (!videoEl) {
    //         return
    //     }
    //     navigator.mediaDevices.getUserMedia({video:true})
    //         .then(stream => {
    //             setLocalStream(stream)
    //             let video = videoEl.current
    //             video.srcObject = stream
    //             video.play()
    //         })
    // }, [videoEl])
    //
    const stopVideo = () => {
        console.log('stop');
        // setLocalStream(null);
    }


    return (
        <div className={css.body}>
            {/*<IconButton icon={faMinus} />*/}

            <div className={css.bodyPeoples}>
                <div className={css.person} />
                {/*    <video ref={videoEl} />*/}
                {/*</div>*/}
                <div className={css.person}>adвsd</div>
                <div className={css.person}>adвsd</div>
                <div className={css.person}>adвsd</div>
                <div className={css.person}>adвsd</div>
                <div className={css.person}>adasd</div>
                <div className={css.person}>adasd</div>

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