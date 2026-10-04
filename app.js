/* Adding a class to the header element when the user scrolls down the page. */
window.addEventListener("scroll", function () {
  document.querySelector("header").classList.toggle("is-scrolling", window.scrollY > 90);
});

/* Toggling the hamburger and mobile-nav when the hamburger or a mobile nav link is clicked. */
$("#hamburger, #mobile-nav a").on("click", function () {
  $("#hamburger, #mobile-nav").toggleClass("is-active");
});

// Route du serveur pour chaque type de filet (typeFilet1..4)
const ROUTES = {
  typeFilet1: "/GetMetrique",
  typeFilet2: "/GetWithGaz",
  typeFilet3: "/GetTrapeze",
  typeFilet4: "/GetRond",
};

/* Sending data to the server and receiving a response. */
$("#btnSend")
  .off()
  .on("click", function () {
    if (
      ($("#diamVis").val() == "" && $("#diamEcrou").val() == "") ||
      $("#surepaisseurUsinage").val() == "" ||
      $("#longueur").val() == ""
    ) {
      $("#errorMessage").html("<h4>Veuillez remplir tous les champs !</h4>");
      $("#tableau").find("tr:gt(0)").remove();
      $("#resultatTableau").hide();
      return;
    }

    const data = {
      dvnu: $("#diamVis").val(), // diametre vis non usiné
      denu: $("#diamEcrou").val(), // diametre ecrou non usiné
      surep: $("#surepaisseurUsinage").val(),
      long: $("#longueur").val(),
      pas: $("#typePas2").is(":checked") ? 1 : 0,
      quality: $("#typeProduction2").is(":checked") ? 1 : 0,
      element: $("#typeElement2").is(":checked") ? 1 : 0, // 0 = vis, 1 = ecrou
    };

    $.ajax({
      url: ROUTES[$("input[name=filet]:checked").attr("id")] || "/GetRond",
      type: "POST",
      data: JSON.stringify(data),
      success: AfficherTableau,
    });
  });

$("#typeFilet").click(function () {
  // Pas de choix de pas ni de qualité pour le Whitworth : on cache et on reset
  const whitworth = $("#typeFilet2").is(":checked");
  $("#typePasDiv, #typeProdDiv").toggle(!whitworth);
  if (whitworth) {
    $("#typePas1, #typePas2, #typeProduction1, #typeProduction2").prop("checked", false);
  }
});

$("#typeElement1, #typeElement2").click(function () {
  // Afficher le bon champ en fonction du type d'élément (ecrou ou vis) et reset l'autre champ
  const ecrou = $("#typeElement2").is(":checked");
  $("#questionTextDiv").show();
  $(ecrou ? "#diamVis" : "#diamEcrou").val("");
  $("#diamVisDiv").toggle(!ecrou);
  $("#diamEcrouDiv").toggle(ecrou);
  $("#typePasDiv, #typeProdDiv").toggle(!$("#typeFilet2").is(":checked"));
});

/* Index des valeurs de la réponse à afficher dans chaque colonne du tableau,
   selon le nombre de valeurs par ligne (= type de filet) et le type d'élément. */
const COLONNES = {
  11: { vis: [0, 1, 2, 2, 3, 4, 5, 6, 7], ecrou: [0, 1, 2, 2, 3, 10, 8, 9] }, // Whitworth / Gaz
  12: { vis: [0, 1, 2, 3, 4, 5, 6, 7, 8], ecrou: [0, 1, 2, 3, 4, 11, 9, 10] }, // Métrique
  13: { vis: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9], ecrou: [0, 1, 2, 3, 4, 5, 12, 10, 11] }, // Rond
  14: { vis: [0, 1, 2, 3, 4, 5, 7, 8, 9, 10], ecrou: [0, 1, 2, 3, 4, 5, 13, 11, 12] }, // Trapézoïdal
};

/*
  It fills the table with the data from the JSON response
  @param reponse - the JSON response from the server
 */
function AfficherTableau(reponse) {
  reponse = JSON.parse(reponse);
  $("#tableau").find("tr:gt(0)").remove(); // Supprimer toutes les lignes sauf la première

  if (reponse.length == 0) {
    $("#errorMessage").html("<h4>Aucun résultat trouvé !</h4>");
    $("#resultatTableau").hide();
    return;
  }
  $("#errorMessage").html("");
  $("#resultatTableau").show();

  const ecrou = $("#typeElement2").is(":checked");
  $("#FFecrou").toggle(reponse[0].length >= 13); // seuls Rond et Trapézoïdal ont un fond de filet ecrou
  $("#diamSortieVis, #hauteurMinVis, #hauteurMaxVis, #chanfrein").toggle(!ecrou);
  $("#diamSortieEcrou, #hauteurMinEcrou, #hauteurMaxEcrou").toggle(ecrou);

  const colonnes = COLONNES[reponse[0].length][ecrou ? "ecrou" : "vis"];
  const tableau = document.getElementById("tableau");
  reponse.forEach(function (ligne) {
    const row = tableau.insertRow();
    colonnes.forEach(function (j) {
      row.insertCell().textContent = Math.round(ligne[j] * 1000) / 1000;
    });
  });
}

window.setTimeout(function () {
  $("#popup").show();
}, 3000);

$("#buttonEmail").click(function () {
  const email = $("#email").val();
  if (email == "Rick Astley") {
    window.open("https://www.youtube.com/watch?v=dQw4w9WgXcQ", "_blank");
  }
  window.open(
    "mailto:r.lozina@student.helmo.be?subject=Bug report&body=" + email,
    "_blank"
  );
});

/* Icon on click */
$("#linkedin").click(function () {
  window.open("https://linkedin.com/in/robin-lozina-405363253", "_blank");
});

$("#github").click(function () {
  window.open("https://github.com/RobinLozina", "_blank");
});

$("#paypal").click(function () {
  window.open(
    "https://paypal.me/RobinLozina?country.x=BE&locale.x=fr_FR",
    "_blank",
    "toolbar=no,titlebar=no,top=200,left=500,width=600,height=600"
  );
});
