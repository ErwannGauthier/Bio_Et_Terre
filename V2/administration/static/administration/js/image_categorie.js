var categorie_image = document.getElementById("image_categorie");
var categorie_img = document.getElementById("categorie-img");


if (categorie_image.value != "") {
    categorie_img.src = categorie_image.value;
}


// LISTENER IMAGE CATEGORIE INTERACTIVE
categorie_image.addEventListener('input', function () {
    categorie_img.src = this.value;
    categorie_img.alt = "Erreur de chargement de l'image."
})