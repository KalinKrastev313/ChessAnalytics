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
    const headersForMakingAMove = createHeaderForMakingAMove(csrftoken, comes_from, goes_to)

    let res = await fetch(BASE_URL, headersForMakingAMove)
    let unparsedData = await res.json()
    var data = JSON.parse(unparsedData);
    console.log(data)
    if (data.is_legal) {
        if (data.is_promotion != true) {
            performNonPromotionMove(goes_to, pieceID)
        }
    } else if (data.is_promotion == true) {
        createPromotionChoiceContainer(comes_from, goes_to, data.piece_color)
    }
}

function createPromotionChoiceDiv(piece_type, piece_color, comes_from, goes_to) {
    const choiceDiv = document.createElement('div')
    const pieceImage = document.createElement('img')
    var colorWord = turnBoolColorToWord(piece_color)
    pieceImage.src = `/static/pieces/cburnett/${piece_type}-${colorWord}.png`

    let piece_code = getPieceCode(piece_type, piece_color)
    choiceDiv.appendChild(pieceImage);
    choiceDiv.onclick = sendPromotionChoice
    choiceDiv.id = comes_from + goes_to + piece_code
    return choiceDiv
}

function turnBoolColorToWord(color){
    if (color){
        return 'white'
    }else {
        return 'black'
    }
}
async function sendPromotionChoice(event) {
    const moveInfo = this.id
    var comes_from = moveInfo.slice(0, 2)
    var goes_to = moveInfo.slice(2, 4)
    var promotes_to = moveInfo[4]
    console.log(comes_from)
    console.log(goes_to)
    console.log(promotes_to)
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    var headersForMakingAMove = createHeaderForMakingAMove(csrftoken, comes_from, goes_to, promotes_to)
    let res = await fetch(BASE_URL, headersForMakingAMove)
    let unparsedData = await res.json()
    var data = JSON.parse(unparsedData);
    console.log(data)
    if (data.is_legal && data.is_promotion){
        var initialSquare = document.getElementById(comes_from)
        initialSquare.innerHTML = ''

        var endSquare = document.getElementById(goes_to)
        var promotedPiece = document.createElement('img')
        var piece_type = getPieceNameFromCode(promotes_to)
        var colorWord = turnBoolColorToWord(data.piece_color)
        promotedPiece.src = `/static/pieces/cburnett/${piece_type}-${colorWord}.png`
        endSquare.appendChild(promotedPiece)
    }
}

function createHeaderForMakingAMove(csrftoken, comes_from, goes_to, promotes_to = null) {
    return {
        method: "POST",
        headers: {'X-CSRFToken': csrftoken, 'Content-Type': 'application/json'},
        body: JSON.stringify({comes_from, goes_to, promotes_to}),
        mode: 'same-origin'
    }
}

function performNonPromotionMove(goes_to, pieceID) {
    let newSquare = document.getElementById(goes_to)
    newSquare.innerHTML = ""
    let pieceImage = document.getElementById(pieceID)

    newSquare.appendChild(pieceImage)
}

function createPromotionChoiceContainer(comes_from, goes_to, color) {

    const promotionChoiceContainer = document.createElement('div')

    const knightChoice = createPromotionChoiceDiv('knight', color, comes_from, goes_to)
    const bishopChoice = createPromotionChoiceDiv('bishop', color, comes_from, goes_to)
    const rookChoice = createPromotionChoiceDiv('rook', color, comes_from, goes_to)
    const queenChoice = createPromotionChoiceDiv('queen', color, comes_from, goes_to)

    promotionChoiceContainer.appendChild(knightChoice)
    promotionChoiceContainer.appendChild(bishopChoice)
    promotionChoiceContainer.appendChild(rookChoice)
    promotionChoiceContainer.appendChild(queenChoice)

    const page = document.getElementsByClassName('wrapper')[0]
    page.appendChild(promotionChoiceContainer)
}

function getPieceCode(pieceType, color) {
    const pieceMapping = {
        true: {
            'knight': 'N',
            'bishop': 'B',
            'rook': 'R',
            'queen': 'Q'
        },
        false: {
            'knight': 'n',
            'bishop': 'b',
            'rook': 'r',
            'queen': 'q'
        }
    }
    return pieceMapping[color][pieceType]
}

function getPieceNameFromCode(piece_code){
    const pieceNamesMapping = {
        'n': 'knight',
        'b': 'bishop',
        'r': 'rook',
        'q': 'queen',
        'k': 'king'
    }
    return pieceNamesMapping[piece_code.toLowerCase()]
}