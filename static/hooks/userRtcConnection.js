import {
    useEffect,
    useRef,
    useCallback,
    useState
} from 'react';
import freeice from 'freeice';
import useStateWithCallback from './useStateWithCallback';
import socket from '../util/websocket';
import ACTION from '../util/action';

export const LOCAL_VIDEO = 'LOCAL_VIDEO';


export default function userRtcConnection(roomID) {
    const [clients, updateClients] = useStateWithCallback([]);
    const [clients, updateClients] = useState([]);

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
        [LOCAL_VIDEO]: null,
    });

    useEffect(() => {
        const handleNewPeer = async ({ peerID, createOffer }) => {
            if (peerID in peerConnections.current) {
                return console.warn(`Already connected to peer ${peerID}`);
            }

            peerConnections.current[peerID] = new RTCPeerConnection({
                iceServers: freeice(),
            });

            peerConnections.current[peerID].onicecandidate = event => {
                if (event.candidate) {
                    socket.send({
                        action: ACTION.RELAY_ICE,
                        data: {
                            peerID,
                            iceCandidate: event.candidate
                        }
                    });
                }
            }

            let tracksNumber = 0;
            peerConnections.current[peerID].ontrack = ({ streams: [remoteStream] }) => {
                tracksNumber++

                if (tracksNumber === 2) {
                    tracksNumber = 0;
                    addNewClient(peerID, () => {
                        if (peerMediaElements.current[peerID]) {
                            peerMediaElements.current[peerID].srcObject = remoteStream;
                        } else {
                            let settled = false;
                            const interval = setInterval(() => {
                                if (peerMediaElements.current[peerID]) {
                                    peerMediaElements.current[peerID].srcObject = remoteStream;
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
                peerConnections.current[peerID].addTrack(track, localMediaStream.current);
            });

            if (createOffer) {
                const offer = await peerConnections.current[peerID].createOffer();

                await peerConnections.current[peerID].setLocalDescription(offer);

                socket.send({
                    action: ACTION.RELAY_SDP,
                    data: {
                        peerID,
                        sessionDescription
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
        async function setRemoteMedia({ peerID, sessionDescription: remoteDescription }) {
            await peerConnections.current[peerID]?.setRemoteDescription(
                new RTCSessionDescription(remoteDescription)
            );

            if (remoteDescription.type === 'offer') {
                const answer = await peerConnections.current[peerID].createAnswer();

                await peerConnections.current[peerID].setLocalDescription(answer);

                socket.send({
                    action: ACTION.RELAY_SDP,
                    data: {
                        peerID,
                        sessionDescription
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
        socket.on(ACTION.ICE_CANDIDATE, ({ peerID, iceCandidate }) => {
            peerConnections.current[peerID]?.addIceCandidate(
                new RTCIceCandidate(iceCandidate)
            );
        });

        return () => {
            socket.off(ACTION.ICE_CANDIDATE);
        }
    }, []);

    useEffect(() => {
        const handleRemovePeer = ({ peerID }) => {
            if (peerConnections.current[peerID]) {
                peerConnections.current[peerID].close();
            }

            delete peerConnections.current[peerID];
            delete peerMediaElements.current[peerID];

            updateClients(list => list.filter(c => c !== peerID));
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

            addNewClient(LOCAL_VIDEO, () => {
                const localVideoElement = peerMediaElements.current[LOCAL_VIDEO];

                if (localVideoElement) {
                    localVideoElement.volume = 0;
                    localVideoElement.srcObject = localMediaStream.current;
                }
            });
        }

        startCapture()
            .then(() => socket.send({
                action: ACTION.JOIN,
                data: { roomID }
            }))
            .catch(e => console.error('Error getting userMedia:', e));

        return () => {
            localMediaStream.current.getTracks().forEach(track => track.stop());

            socket.send({ action: ACTION.LEAVE, data: {} });
        };
    }, [roomID]);

    const provideMediaRef = useCallback((id, node) => {
        peerMediaElements.current[id] = node;
    }, []);

    return {
        clients,
        provideMediaRef
    };
}