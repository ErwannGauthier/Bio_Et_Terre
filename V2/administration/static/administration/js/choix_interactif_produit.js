var marque = document.getElementById("marque");
var new_marque = document.getElementById("new_marque");
var marque_nom = document.getElementById("marque_nom");

if (marque.value == -1) {
    new_marque.style = "";
    marque_nom.required = true;
} else {
    new_marque.style = "display: none;";
    marque_nom.required = false;
}

marque.addEventListener('click', function () {
    if (this.value == -1) {
        new_marque.style = "";
        marque_nom.required = true;
    } else {
        new_marque.style = "display: none;";
        marque_nom.required = false;
    }
});



var categorie = document.getElementById("categorie");
var new_categorie = document.getElementById("new_categorie");
var categorie_nom = document.getElementById("categorie_nom");
var categorie_tva = document.getElementById("categorie_tva");
var categorie_image = document.getElementById("image_categorie");

if (categorie.value == -1) {
    new_categorie.style = "";
    categorie_nom.required = true;
    categorie_tva.required = true;
    categorie_image.required = true;
} else {
    new_categorie.style = "display: none;";
    categorie_nom.required = false;
    categorie_tva.required = false;
    categorie_image.required = false;
}

categorie.addEventListener('click', function () {
    if (this.value == -1) {
        new_categorie.style = "";
        categorie_nom.required = true;
        categorie_tva.required = true;
        categorie_image.required = true;
    } else {
        new_categorie.style = "display: none;";
        categorie_nom.required = false;
        categorie_tva.required = false;
        categorie_image.required = false;
    }
});



var type = document.getElementById("type");
var solide = document.getElementById("div_solide");
var type_solide = document.getElementById("solide");
var liquide = document.getElementById("div_liquide");
var type_liquide = document.getElementById("liquide");

if (type.value == 1) {
    solide.style = "display: none;";
    type_solide.required = false;
    liquide.style = "display: none;";
    type_liquide.required = false;
} else if (type.value == 2) {
    solide.style = "";
    type_solide.required = true;
    liquide.style = "display: none;";
    type_liquide.required = false;
} else if (type.value == 3) {
    solide.style = "display: none;";
    type_solide.required = false;
    liquide.style = "";
    type_liquide.required = true;
}

type.addEventListener('click', function () {
    if (this.value == 1) {
        solide.style = "display: none;";
        type_solide.required = false;
        liquide.style = "display: none;";
        type_liquide.required = false;
    } else if (this.value == 2) {
        solide.style = "";
        type_solide.required = true;
        liquide.style = "display: none;";
        type_liquide.required = false;
    } else if (this.value == 3) {
        solide.style = "display: none;";
        type_solide.required = false;
        liquide.style = "";
        type_liquide.required = true;
    }
});