'use server'

// const SERVER_PORT = process.env.VL_SERVER_PORT;
const SERVER_PORT = 9998;
console.log('api SERVER_PORT:', SERVER_PORT);

export async function syncState(timeStamp: number) {
    console.log('syncState', timeStamp);
    const res = await fetch(`http://localhost:${SERVER_PORT}`, {
        'headers': {
            'timeStamp': timeStamp.toString()
        }
    })
    .then(async response => {
        let data = await response.json();
        console.log('syncState =>', data);
        return data;
    })
    .catch(error => {
        console.log(error);
        return {
            'time': 0,
            'data': {}
        };
    });
    return res;
}
