import React from 'react';
import {
    useEffect,
    useRef,
    useCallback, useContext,
} from 'react';
import freeice from 'freeice';
import ACTION from '../util/action';
import { MainContext } from "../components/App/context";
import { useHistory } from "react-router";
import logMessage from '../util/logging';
import getIceServers from '../util/iceServers';


export const MEDIA_STREAM_STATE = {
    ON: true,
    OFF: false,
}


export default function userRtcConnection(roomId, socket) {
    const { email: [inputEmail] } = useContext(MainContext);
    const { name: [inputName] } = useContext(MainContext);
    const { organizer: [isOrganizer] } = useContext(MainContext);
    const { clients: [clients, setClients] } = useContext(MainContext);
    const history = useHistory();


    const addNewClient = useCallback((newClient, cb) => {
        setClients(list => {
            if (!list.includes(newClient)) {
                return [...list, newClient]
            }

            return list;
        }, cb);
    }, [clients, setClients]);

    const peerConnections = useRef({});
    const localMediaStream = useRef(null);
    const peerMediaElements = useRef({
        [inputEmail]: null,
    });

    useEffect(() => {
        const handleNewPeer = async ({ client, createOffer }) => {
            const peerId = client.peerId;
            logMessage(`Peed ${peerId} invoked handleNewPeer`);
            if (peerId in peerConnections.current) {
                return console.warn(`Already connected to peer ${peerId}`);
            }
            const servers = getIceServers();
            const pc_constraints = {"optional": [{"DtlsSrtpKeyAgreement": true}]};

            peerConnections.current[peerId] = new RTCPeerConnection(servers, pc_constraints);
            peerConnections.current[peerId].onicecandidate = event => {
                if (event.candidate) {
                    logMessage('Inside if | before RELAY_ICE');
                    socket.send({
                        action: ACTION.RELAY_ICE,
                        data: {
                            peerId,
                            roomId,
                            iceCandidate: event.candidate
                        }
                    });
                } else {
                    logMessage('No Ice Candidate');
                }
            }

            let tracksNumber = 0;
            peerConnections.current[peerId].ontrack = ({ streams: [remoteStream] }) => {
                tracksNumber++

                if (tracksNumber === 2) {
                    tracksNumber = 0;
                    addNewClient(client, () => {
                        if (peerMediaElements.current[peerId]) {
                            peerMediaElements.current[peerId].srcObject = remoteStream;
                        } else {
                            let settled = false;
                            const interval = setInterval(() => {
                                if (peerMediaElements.current[peerId]) {
                                    peerMediaElements.current[peerId].srcObject = remoteStream;
                                    settled = true;
                                }

                                if (settled) {
                                    clearInterval(interval);
                                }
                            }, 1000);
                        }
                    });
                }
            }

            localMediaStream.current.getTracks().forEach(track => {
                peerConnections.current[peerId].addTrack(track, localMediaStream.current);
            });

            logMessage(`Before createOffer=${createOffer}`);

            if (createOffer) {
                const offer = await peerConnections.current[peerId].createOffer();

                logMessage(`Sending createOffer=${createOffer}`);
                await peerConnections.current[peerId].setLocalDescription(offer);

                socket.send({
                    action: ACTION.RELAY_SDP,
                    data: {
                        peerId,
                        roomId,
                        sessionDescription: offer
                    }
                });
            }
        }

        socket.on(ACTION.ADD_PEER, handleNewPeer);

        return () => {
            socket.off(ACTION.ADD_PEER);
        }
    }, []);

    useEffect(() => {
        async function setRemoteMedia({ peerId, sessionDescription: remoteDescription }) {
            await peerConnections.current[peerId]?.setRemoteDescription(
                new RTCSessionDescription(remoteDescription)
            );

            if (remoteDescription.type === 'offer') {
                const answer = await peerConnections.current[peerId].createAnswer();

                await peerConnections.current[peerId].setLocalDescription(answer);

                socket.send({
                    action: ACTION.RELAY_SDP,
                    data: {
                        peerId,
                        roomId,
                        sessionDescription: answer
                    }
                });
            }
        }

        socket.on(ACTION.SESSION_DESCRIPTION, setRemoteMedia)

        return () => {
            socket.off(ACTION.SESSION_DESCRIPTION);
        }
    }, []);

    useEffect(() => {
        socket.on(ACTION.ICE_CANDIDATE, ({ peerId, iceCandidate }) => {
            peerConnections.current[peerId]?.addIceCandidate(
                new RTCIceCandidate(iceCandidate)
            );
        });

        return () => {
            socket.off(ACTION.ICE_CANDIDATE);
        }
    }, []);

    useEffect(() => {
        const handleRemovePeer = ({ peerId }) => {
            if (peerConnections.current[peerId]) {
                peerConnections.current[peerId].close();
            }

            delete peerConnections.current[peerId];
            delete peerMediaElements.current[peerId];

            setClients(list => list.filter(el => el.peerId !== peerId));
        };

        socket.on(ACTION.REMOVE_PEER, handleRemovePeer);

        return () => {
            socket.off(ACTION.REMOVE_PEER);
        }
    }, []);

    useEffect(() => {
        const handleClientDeleted = ({ peerId }) => {
            if (inputEmail === peerId) {
                history.push('/');
            }
        };

        socket.on(ACTION.CLIENT_DELETED, handleClientDeleted);

        return () => {
            socket.off(ACTION.CLIENT_DELETED);
        }
    }, []);

    useEffect(() => {
        async function startCapture() {
            try {
                localMediaStream.current = await navigator.mediaDevices.getUserMedia({
                    audio: true,
                    video: {
                        width: 1280,
                        height: 720,
                    }
                });
            } catch (err) {
                return history.push('/permission/')
            }


            addNewClient({ email: inputEmail, peerId: inputEmail, name: inputName, isOrganizer }, () => {
                const localVideoElement = peerMediaElements.current[inputEmail];

                if (localVideoElement) {
                    localVideoElement.volume = 0;
                    localVideoElement.srcObject = localMediaStream.current;
                }
            });
        }

        startCapture()
            .then(() => socket.send({
                action: ACTION.JOIN,
                data: {
                    roomId, client: {
                        'peerId': inputEmail, 'name': inputName, 'email': inputEmail, isOrganizer
                    }
                }
            }))
            .catch(e => console.error('Error getting userMedia:', e));

        if (localMediaStream.current === null) {
            return
        }
        return () => {
            localMediaStream.current.getTracks().forEach(track => track.stop());
            socket.send({ action: ACTION.LEAVE, data: { roomId } });
            setClients(list => list.filter(el => el.email !== inputEmail));
        };
    }, [roomId]);

    const provideMediaRef = useCallback((id, node) => {
        peerMediaElements.current[id] = node;
    }, []);

    const controlMediaStream = useCallback((microphoneState, videoState) => {
        const localStream = localMediaStream.current;

        if (microphoneState === MEDIA_STREAM_STATE.ON) {
            if (localStream && localMediaStream.current.getAudioTracks().length) {
                localMediaStream.current.getAudioTracks()[0].enabled = true
            }
        } else if (microphoneState === MEDIA_STREAM_STATE.OFF) {
            if (localStream && localMediaStream.current.getAudioTracks().length) {
                localMediaStream.current.getAudioTracks()[0].enabled = false
            }
        }

        if (videoState === MEDIA_STREAM_STATE.ON) {
            if (
                localMediaStream.current &&
                localMediaStream.current.getVideoTracks().length > 0
            ) {
                localMediaStream.current.getVideoTracks()[0].enabled = true
            }
        } else if (videoState === MEDIA_STREAM_STATE.OFF) {
            if (
                localMediaStream.current &&
                localMediaStream.current.getVideoTracks().length > 0
            ) {
                localMediaStream.current.getVideoTracks()[0].enabled = false
            }
        }
    });

    return {
        provideMediaRef,
        controlMediaStream,
    };
}