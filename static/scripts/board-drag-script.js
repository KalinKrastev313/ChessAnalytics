
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
    var pieceID = ev.dataTransfer.getData("text");
    var comes_from = pieceID.slice(-2);
    var goes_to = ev.target.id.slice(-2)
    const headersForMakingAMove = {

        method: "POST",
        headers: {'X-CSRFToken': csrftoken, 'Content-Type': 'application/json'},
        body: JSON.stringify({comes_from, goes_to}),
        mode: 'same-origin'
    }
    console.log(comes_from)
    console.log(goes_to)
    console.log(JSON.stringify(headersForMakingAMove, null, 2));
    let res =  await fetch(BASE_URL, headersForMakingAMove)
    let unparsedData = await res.json()
    var data = JSON.parse(unparsedData);
    console.log(data)
    console.log(data.is_legal)
    if (data.is_legal){
        if (data.is_promotion != true){
            let newSquare = document.getElementById(goes_to)
            newSquare.innerHTML = ""
            let pieceImage = document.getElementById(pieceID)

            newSquare.appendChild(pieceImage)
        }

    }
}