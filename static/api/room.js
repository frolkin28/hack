const API_ROUTE = "http://localhost:8080/api"


export const postRoom = () =>
    fetch(`${API_ROUTE}/rooms`, {
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
