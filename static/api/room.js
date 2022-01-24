export const postRoom = () =>
    fetch('/api/rooms', {
        method: 'POST',
        headers: { "Content-Type": "application/json" },
    })
        .then((response) => {
            return response.json();
        })
        .then((data) => {
            return data.roomId;
        })
        .catch((err) => {
            console.log(`Error create room: ${err}`);
            return ''
        });

export const getRoom = (roomId) =>
    fetch(`/api/rooms/${roomId}`, {
        method: 'GET',
        headers: { "Content-Type": "application/json" },
    })
        .then((response) => {
            return response.json();
        })
        .then((data) => {
            return data.organizerEmail;
        })
        .catch((err) => {
            console.log(err)
            console.log(err.status)
            console.log(`Error get organizer room: ${err}`);
            return ''
        });

export const getRooms = () =>
    fetch(`/api/rooms`, {
        method: 'GET',
        headers: { "Content-Type": "application/json" },
    })
        .then((response) => {
            return response.json();
        })
        .then((data) => {
            return data.map(data => data.roomId);
        })
        .catch((err) => {
            console.log(err)
            console.log(`Error get organizer room: ${err}`);
            return ''
        });