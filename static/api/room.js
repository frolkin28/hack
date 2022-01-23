export const postRoom = () =>
    fetch('/api/rooms', {
        method: 'POST',
        headers: { "Content-Type": "application/json" },
    })
        .then((response) => {
            return response.json();
        })
        .then((data) => {
            return data.room_id;
        })
        .catch((err) => {
            console.log(`Error create room: ${err}`);
            return ''
        });
