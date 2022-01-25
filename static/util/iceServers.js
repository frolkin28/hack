const getIceServers = () => {
    return {
        'iceServers': [
            {
                'url': 'stun:stun.l.google.com:19302'
            },
            {
                'url': 'stun:stun1.l.google.com:19302'
            },
            {
                'url': 'stun:stun2.l.google.com:19302'
            },
            {
                'url': 'stun:stun3.l.google.com:19302'
            },
            {
                'url': 'stun:stun4.l.google.com:19302'
            },
            {
                'url': 'stun:stun.ekiga.net'
            },
            {
                'url': 'stun:stun.ideasip.com'
            },
            {
                'url': 'stun:stun.schlund.de'
            },
            {
                'url': 'stun:stun.stunprotocol.org:3478'
            },
            {
                'url': 'stun:stun.voiparound.com'
            },
            {
                'url': 'stun:stun.voipbuster.com'
            },
            {
                'url': 'stun:stun.voipstunt.com'
            },
            {
                'url': 'stun:stun.voxgratia.org'
            },
            {
                'url': 'turn:192.158.29.39:3478?transport=udp',
                'credential': 'JZEOEt2V3Qb0y27GRntt2u2PAYA=',
                'username': '28224511:1379330808'
            },
            {
                'url': 'turn:192.158.29.39:3478?transport=tcp',
                'credential': 'JZEOEt2V3Qb0y27GRntt2u2PAYA=',
                'username': '28224511:1379330808'
            },
            {
                'url': 'turn:numb.viagenie.ca',
                'credential': 'muazkh',
                'username': 'webrtc@live.com'
            },
        ],
        // 'iceCandidatePoolSize': 10
    };
}


export default getIceServers;