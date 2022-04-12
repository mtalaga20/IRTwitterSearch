/*

*/

// requests
const get = async (url, params) => {
    return fetch(url + '?' + (new URLSearchParams(params)).toString(), {
        method: 'GET'
    }).then(res => res.json())
}

const post = async(url, params) => {
    return fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(params)
    }).then(res => res.json())
}

// function to execute once every second
window.onload = async function updateClock() {
    let url = 'http://localhost:8000/query'
    let params = {
        query: 'cats and dogs'
    }

    const result = await post(url, params).catch(err => console.log("Err: " + err))
    document.body.innerHTML = '<h1>Date: ' + (new Date()) + ' -- "' + result.ranked_results + '"</h1>'
    setTimeout(updateClock, 1000)
}