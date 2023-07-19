BASE_URL = "http://127.0.0.1:8000/fenreader/"

function allowDrop(ev) {
    ev.preventDefault();
}

function drag(ev) {
    ev.dataTransfer.setData("text", ev.target.id);
}

async function drop(ev) {
    ev.preventDefault();
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    console.log(csrftoken)
    var comes_from = ev.dataTransfer.getData("text").slice(-2);
    var goes_to = ev.target.id
    const headersForMakingAMove = {
        method: "POST",
        headers: {'X-CSRFToken': csrftoken},
        body: JSON.stringify({comes_from, goes_to}),
        mode: 'same-origin'
    }
    let res = await fetch(BASE_URL, headersForMakingAMove)


}