var updateBtns = document.getElementsByClassName('update-cart')

for (i = 0; i < updateBtns.length; i++) {
    updateBtns[i].addEventListener('click', function () {
        var quantite;
        try {
            quantite = parseInt(document.getElementById("quantite").value);
        } catch {
            quantite = 1;
        }
        var productId = this.dataset.product
        var action = this.dataset.action
        //console.log("ID: ", productId, "\nAction: ", action, "\nQuantite: ", quantite)

        //console.log("User: ", user)
        if (user === "AnonymousUser") {
            //console.log("Pas connecté")
        } else {
            updateUserOrder(productId, action, quantite)
        }
    })
}

function updateUserOrder(productId, action, quantite) {
    //var url = 'update_item/'

    fetch(urlUpdateItem, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken,
            },
            body: JSON.stringify({
                'productId': productId,
                'action': action,
                'quantite': quantite
            })
        })

        .then((response) => {
            return response.json()
        })

        .then((data) => {
            console.log('data:', data)
            location.reload()
        })
}