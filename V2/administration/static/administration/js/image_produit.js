var produit_image = document.getElementById("image_produit");
var produit_img = document.getElementById("produit-img");


if (produit_image.value != "") {
    produit_img.src = produit_image.value;
}


// LISTENER IMAGE CATEGORIE INTERACTIVE
produit_image.addEventListener('input', function () {
    produit_img.src = this.value;
    produit_img.alt = "Erreur de chargement de l'image."
})