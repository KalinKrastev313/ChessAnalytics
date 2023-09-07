
function allowDrop(ev) {
    ev.preventDefault();
}

function drag(ev) {
    ev.dataTransfer.setData("text", ev.target.id);
}

async function drop(ev) {
    ev.preventDefault();
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
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
    if (data.is_legal){
        if (data.is_promotion != true){
            let newSquare = document.getElementById(goes_to)
            newSquare.innerHTML = ""
            let pieceImage = document.getElementById(pieceID)

            newSquare.appendChild(pieceImage)
        }
    }else if (data.is_promotion == true) {

        const promotionChoiceContainer = document.createElement('div')

        const knightChoice = createPromotionChoiceDiv('knight', 'black', comes_from, goes_to)
        const bishopChoice = createPromotionChoiceDiv('bishop', 'black', comes_from, goes_to)
        const rookChoice = createPromotionChoiceDiv('rook', 'black', comes_from, goes_to)
        const queenChoice = createPromotionChoiceDiv('queen', 'black', comes_from, goes_to)

        promotionChoiceContainer.appendChild(knightChoice)
        promotionChoiceContainer.appendChild(bishopChoice)
        promotionChoiceContainer.appendChild(rookChoice)
        promotionChoiceContainer.appendChild(queenChoice)

        const page = document.getElementsByClassName('wrapper')[0]
        page.appendChild(promotionChoiceContainer)
    }
}

function createPromotionChoiceDiv(piece_type, piece_color, comes_from, goes_to){
    const choiceDiv = document.createElement('div')
    const pieceImage = document.createElement('img')
    pieceImage.src = `/static/pieces/cburnett/${piece_type}-${piece_color}.png`
    choiceDiv.appendChild(pieceImage);
    choiceDiv.onclick = sendPromotionChoice
    choiceDiv.id = piece_type + comes_from + goes_to
    return choiceDiv
}

function sendPromotionChoice(event){
    console.log(this.id)

}