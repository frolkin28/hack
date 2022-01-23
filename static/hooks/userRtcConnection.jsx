import {
    useEffect,
    useRef,
    useCallback, useContext,
} from 'react';
import freeice from 'freeice';
import useStateWithCallback from './useStateWithCallback';
import socket from '../util/websocket';
import ACTION from '../util/action';
import {MainContext} from "../components/App/context";


export default function userRtcConnection(roomId) {
    const {email: [inputEmail]} = useContext(MainContext);
    const {name: [inputName]} = useContext(MainContext);

    const [clients, updateClients] = useStateWithCallback([]);

    const addNewClient = useCallback((newClient, cb) => {
        updateClients(list => {
            if (!list.includes(newClient)) {
                return [...list, newClient]
            }

            return list;
        }, cb);
    }, [clients, updateClients]);

    const peerConnections = useRef({});
    const localMediaStream = useRef(null);
    const peerMediaElements = useRef({
        [inputEmail]: null,
    });

    useEffect(() => {
        const handleNewPeer = async ({ client, createOffer }) => {
            const peerId = client.peerId;
            if (peerId in peerConnections.current) {
                return console.warn(`Already connected to peer ${peerId}`);
            }

            peerConnections.current[peerId] = new RTCPeerConnection({
                iceServers: freeice(),
            });

            peerConnections.current[peerId].onicecandidate = event => {
                if (event.candidate) {
                    socket.send({
                        action: ACTION.RELAY_ICE,
                        data: {
                            peerId,
                            roomId,
                            iceCandidate: event.candidate
                        }
                    });
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

            if (createOffer) {
                const offer = await peerConnections.current[peerId].createOffer();

                await peerConnections.current[peerId].setLocalDescription(offer);
                console.log(peerId)
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

            updateClients(list => list.filter(c => c !== peerId));
        };

        socket.on(ACTION.REMOVE_PEER, handleRemovePeer);

        return () => {
            socket.off(ACTION.REMOVE_PEER);
        }
    }, []);

    useEffect(() => {
        async function startCapture() {
            localMediaStream.current = await navigator.mediaDevices.getUserMedia({
                audio: true,
                video: {
                    width: 1280,
                    height: 720,
                }
            });

            addNewClient({email: inputEmail, peerId: inputEmail, name: inputName}, () => {
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
                data: { roomId, client: {
                        'peerId': inputEmail, 'name': inputName, 'email': inputEmail
                    }}
            }))
            .catch(e => console.error('Error getting userMedia:', e));

        return () => {
            localMediaStream.current.getTracks().forEach(track => track.stop());

            socket.send({ action: ACTION.LEAVE, data: {roomId} });
            const clientsCopy = clients.filter(client => client.email !== inputEmail);
            console.log(clientsCopy);
            updateClients(clientsCopy)
        };
    }, [roomId]);

    const provideMediaRef = useCallback((id, node) => {
        peerMediaElements.current[id] = node;
    }, []);

    return {
        clients,
        provideMediaRef
    };
}