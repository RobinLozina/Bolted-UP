/* Adding a class to the header element when the user scrolls down the page. */
window.onload = function() {
    window.addEventListener('scroll', function(e) {
        if(window.pageYOffset>90){
            this.document.querySelector('header').classList.add('is-scrolling');
        }
        else{
            this.document.querySelector('header').classList.remove('is-scrolling');
        }
    });
};

/* Adding a class of is-active to the hamburger and mobile-nav when the hamburger is clicked. */
$('#hamburger').on('click', function() {
    $('#hamburger').toggleClass('is-active');
    $('#mobile-nav').toggleClass('is-active');
});

/* Adding a click event to the mobile nav links. When the links are clicked, the hamburger icon is
toggled to an active state and the mobile nav is toggled to an active state. */
$('#mobile-nav a').on('click', function() {
    $('#hamburger').toggleClass('is-active');
    $('#mobile-nav').toggleClass('is-active');
});



/* Sending data to the server and receiving a response. */
$('#btnSend').off().on('click',function(){
    
    /* Checking if the diamVis and diamEcrou are empty and if the surepaisseurUsinage and longueur are
    empty. If they are empty, it will display an error message. */
    if(($('#diamVis').val() == '' && $('#diamEcrou').val() == '') || $('#surepaisseurUsinage').val() == '' || $('#longueur').val() == '' ){
        $('#errorMessage').html('<h4>Veuillez remplir tous les champs !</h4>');
        $('#tableau').find("tr:gt(0)").remove();
        $('#resultatTableau').hide();

    }
    else{
        /* Sending a POST request to the server. */
        if(document.getElementById('typeFilet1').checked){ // Si le type de filet est métrique 
            console.log("Metrique");
            var typePas = 0; 
            if(document.getElementById('typePas2').checked){        
                typePas = 1;
                console.log("Pas fin");
            }
            var quality = 0; 
            if(document.getElementById('typeProduction2').checked){
                quality = 1;
                console.log("Qualité");
            }
            var element = 0; // 0 = vis, 1 = ecrou
            if(document.getElementById('typeElement2').checked){
                element = 1;
                console.log("Ecrou");
            }
           var data = {
            'dvnu': $('#diamVis').val(),
            'denu': $('#diamEcrou').val(),
            'surep': $('#surepaisseurUsinage').val(),
            'long': $('#longueur').val(),
            'pas' : typePas,
            'quality' : quality,
            'element' : element

            };
            $.ajax({
                url: '/GetMetrique',
                type: 'POST',
                data: JSON.stringify(data),

                success: function(reponse){
                    $('#tableau').html(AfficherTableau(reponse));
                }
            });
        }

        else if(document.getElementById('typeFilet2').checked){ // Si le type de filet est Withworth ou Gaz
            console.log("Withworth");
            var element = 0; // 0 = vis, 1 = ecrou
            if(document.getElementById('typeElement2').checked){
                element = 1;
            }
            var data= {
                'dvnu': $('#diamVis').val(),
                'denu': $('#diamEcrou').val(),
                'surep': $('#surepaisseurUsinage').val(),
                'long': $('#longueur').val(),
                'element' : element
            };

            $.ajax({
                url: '/GetWithGaz',
                type: 'POST',
                data: JSON.stringify(data),

                success: function(reponse){
                    $('#tableau').html(AfficherTableau(reponse));
                }
            });
        }

        

        else if(document.getElementById('typeFilet3').checked){ // Si le type de filet est Trapézoïdal
            console.log("Trapeze");
            var typePas = 0;
            if(document.getElementById('typePas2').checked){
                typePas = 1;
            }
            var quality = 0;
            if(document.getElementById('typeProduction2').checked){
                quality = 1;
            }
            var element = 0; // 0 = vis, 1 = ecrou
            if(document.getElementById('typeElement2').checked){
                element = 1;
            }
            
           var data = {
            'dvnu': $('#diamVis').val(),
            'denu': $('#diamEcrou').val(),
            'surep': $('#surepaisseurUsinage').val(),
            'long': $('#longueur').val(),
            'pas' : typePas,
            'quality' : quality,
            'element' : element
            };
            
            $.ajax({
                url: '/GetTrapeze',
                type: 'POST',
                data: JSON.stringify(data),

                success: function(reponse){
                    $('#tableau').html(AfficherTableau(reponse));
                }
            });
        }

        

        else {                                                  // Si le type de filet est Rond
            console.log("Rond");
            var typePas = 0;
            if(document.getElementById('typePas2').checked){
                typePas = 1;
            }
            var quality = 0;
            if(document.getElementById('typeProduction2').checked){
                quality = 1;
            }
            var element = 0; // 0 = vis, 1 = ecrou
            if(document.getElementById('typeElement2').checked){
                element = 1;
            }
            
           var data = {
            'dvnu': $('#diamVis').val(),
            'denu': $('#diamEcrou').val(),
            'surep': $('#surepaisseurUsinage').val(),
            'long': $('#longueur').val(),
            'pas' : typePas,
            'quality' : quality,
            'element' : element
            };
            
            $.ajax({
                url: '/GetRond',
                type: 'POST',
                data: JSON.stringify(data),

                success: function(reponse){
                    $('#tableau').html(AfficherTableau(reponse));
                }
            });

        }
    }
});


$('#typeFilet').click(function(){        // Afficher le bon champ en fonction du type de filet et reset l'autre champ
    if(document.getElementById('typeFilet2').checked){
        $('#typePasDiv').hide();
        $('#typeProdDiv').hide();
        $('#typePas1').prop('checked', false);
        $('#typePas2').prop('checked', false);
        $('#typeProduction1').prop('checked', false);
        $('#typeProduction2').prop('checked', false);
    }
    else{
        $('#typePasDiv').show();
        $('#typeProdDiv').show();
    }
});


$('#typeElement1').click(function(){      // Afficher le bon champ en fonction du type d'élément (ecrou ou vis) et reset l'autre champ
    $('#questionTextDiv').show();
    if(document.getElementById('typeElement1').checked){
        if(document.getElementById('typeFilet2').checked==false){
            $('#diamEcrou').val('');
            $('#diamEcrouDiv').hide();
            $('#diamVisDiv').show();
            $('#typePasDiv').show();
            $('#typeProdDiv').show();
        }
        else{
            $('#diamEcrou').val('');
            $('#diamEcrouDiv').hide();
            $('#diamVisDiv').show();
            $('#typePasDiv').hide();
            $('#typeProdDiv').hide();
        }

    }
    else if(document.getElementById('typeElement2').checked){
        if(document.getElementById('typeFilet2').checked==false){
            $('#diamVis').val('');
            $('#diamVisDiv').hide();
            $('#diamEcrouDiv').show();
            $('#typePasDiv').show();
            $('#typeProdDiv').show();
        }
        else{
            $('#diamVis').val('');
            $('#diamVisDiv').hide();
            $('#diamEcrouDiv').show();
            $('#typePasDiv').hide();
            $('#typeProdDiv').hide();
        }

    }
});


$('#typeElement2').click(function(){      // Afficher le bon champ en fonction du type d'élément (ecrou ou vis) et reset l'autre champ
    $('#questionTextDiv').show();
    if(document.getElementById('typeElement1').checked){
        if(document.getElementById('typeFilet2').checked==false){
            $('#diamEcrou').val('');
            $('#diamEcrouDiv').hide();
            $('#diamVisDiv').show();
            $('#typePasDiv').show();
            $('#typeProdDiv').show();
        }
        else{
            $('#diamEcrou').val('');
            $('#diamEcrouDiv').hide();
            $('#diamVisDiv').show();
            $('#typePasDiv').hide();
            $('#typeProdDiv').hide();
        }

    }
    else if(document.getElementById('typeElement2').checked){
        if(document.getElementById('typeFilet2').checked==false){
            $('#diamVis').val('');
            $('#diamVisDiv').hide();
            $('#diamEcrouDiv').show();
            $('#typePasDiv').show();
            $('#typeProdDiv').show();
        }
        else{
            $('#diamVis').val('');
            $('#diamVisDiv').hide();
            $('#diamEcrouDiv').show();
            $('#typePasDiv').hide();
            $('#typeProdDiv').hide();
        }

    }
});





/*
  It creates a table with the data from the JSON response
  @param reponse - the JSON response from the server
 */
function AfficherTableau(reponse) {

    console.log("AFFICHER TAB");
    /* Parsing the JSON response and then creating a table with the data. */
    $('#resultatTableau').show();
    var reponse = JSON.parse(reponse);
    var tableau =document.getElementById("tableau");
    console.log(reponse);
    console.log(reponse[0]);

            
    $('#tableau').find("tr:gt(0)").remove();    // Supprimer toutes les lignes sauf la première
    

    /* Checking if the response is empty. If it is, it hides the result and displays an error message.
    If it is not empty, it clears the error message. */
    if(reponse.length==0){
        console.log("tout vide");
        $('errorMessage').show();
        $('#errorMessage').html('<h4>Aucun résultat trouvé !</h4>'); 
        $('#resultatTableau').hide()
        return;
    }
    else{
        console.log("pas vide");
        $('errorMessage').hide();
        $('#errorMessage').html('');
    }


    if(reponse[0].length == 11){           // Si le type de filet est WithGaz
        console.log("WithGaz");
        if(document.getElementById('typeElement1').checked){    // Si le type d'élément est une vis
            console.log("Vis WITHGAZ");
            $('#FFecrou').hide();
            $('#diamSortieEcrou').hide();
            $('#hauteurMinEcrou').hide();       
            $('#hauteurMaxEcrou').hide();
            $('#diamSortieVis').show();
            $('#hauteurMinVis').show();
            $('#hauteurMaxVis').show();
            $('#chanfrein').show();
            // HIDE TOUS LES TRUCS A HIDE
            for(let i=0;i<=reponse.length;i++){
                var row = tableau.insertRow();

                var cell1 = row.insertCell(0);
                var cell2 = row.insertCell(1);
                var cell3 = row.insertCell(2);
                var cell4 = row.insertCell(3);
                var cell5 = row.insertCell(4);
                var cell6 = row.insertCell(5);
                var cell7 = row.insertCell(6);
                var cell8 = row.insertCell(7);
                var cell9 = row.insertCell(8);


                cell1.innerHTML = Math.round(reponse[i][0]*1000)/1000;   // diametre nominal
                cell2.innerHTML = Math.round(reponse[i][1]*1000)/1000;   // pas de filet
                cell3.innerHTML = Math.round(reponse[i][2]*1000)/1000;   //diametre fond de filet
                cell4.innerHTML = Math.round(reponse[i][2]*1000)/1000;   // diametre forage/percage
                cell5.innerHTML = Math.round(reponse[i][3]*1000)/1000;   //rayon
                cell6.innerHTML = Math.round(reponse[i][4]*1000)/1000;   // diametre sortie outil
                cell7.innerHTML = Math.round(reponse[i][5]*1000)/1000;   //hauteur min sortie outil
                cell8.innerHTML = Math.round(reponse[i][6]*1000)/1000;   //hauteur max sortie outil
                cell9.innerHTML = Math.round(reponse[i][7]*1000)/1000;   //chanfrein

                
            }
            
        }
        else if(document.getElementById('typeElement2').checked){    // Si le type d'élément est un ecrou
            console.log("Ecrou WITHGAZ");
            $('#FFecrou').hide();
            $('#diamSortieVis').hide();
            $('#hauteurMinVis').hide();
            $('#hauteurMaxVis').hide();
            $('#chanfrein').hide();
            $('#diamSortieEcrou').show();
            $('#hauteurMinEcrou').show();
            $('#hauteurMaxEcrou').show();
            for(let i=0;i<=reponse.length;i++){
                var row = tableau.insertRow();

                var cell1 = row.insertCell(0);
                var cell2 = row.insertCell(1);
                var cell3 = row.insertCell(2);
                var cell7 = row.insertCell(3);
                var cell8 = row.insertCell(4);
                var cell10 = row.insertCell(5);
                var cell11 = row.insertCell(6);
                var cell12 = row.insertCell(7);


                cell1.innerHTML = Math.round(reponse[i][0]*1000)/1000;   // diametre nominal
                cell2.innerHTML = Math.round(reponse[i][1]*1000)/1000;   // pas de filet
                cell3.innerHTML = Math.round(reponse[i][2]*1000)/1000;   //diametre fond de filet
                cell7.innerHTML = Math.round(reponse[i][2]*1000)/1000;   // diametre forage/percage
                cell8.innerHTML = Math.round(reponse[i][3]*1000)/1000;   //rayon
                cell10.innerHTML = Math.round(reponse[i][10]*1000)/1000;  //diametre entree outil
                cell11.innerHTML = Math.round(reponse[i][8]*1000)/1000; //hauteur min entree outil
                cell12.innerHTML = Math.round(reponse[i][9]*1000)/1000; //hauteur max entree outil
                
            }
            
        }
    }






    else if(reponse[0].length == 12){      // Si le type de filet est Metrique
        console.log("METRIQUE");
        if(document.getElementById('typeElement1').checked){    // Si le type d'élément est une vis
            console.log("VIS METRIQUE ")
                        // HIDE TOUS LES TRUCS A HIDE
            $('#FFecrou').hide();
            $('#diamSortieEcrou').hide();
            $('#hauteurMinEcrou').hide();
            $('#hauteurMaxEcrou').hide();
            $('#diamSortieVis').show();
            $('#hauteurMinVis').show();
            $('#hauteurMaxVis').show();
            $('#chanfrein').show();
            for(let i=0;i<=reponse.length;i++){
                var row = tableau.insertRow();

                var cell1 = row.insertCell(0);
                var cell2 = row.insertCell(1);
                var cell3 = row.insertCell(2);
                var cell4 = row.insertCell(3);
                var cell5 = row.insertCell(4);
                var cell6 = row.insertCell(5);
                var cell7 = row.insertCell(6);
                var cell8 = row.insertCell(7);
                var cell9 = row.insertCell(8);


                cell1.innerHTML = reponse[i][0];   // diametre nominal
                cell2.innerHTML = reponse[i][1];   // pas de filet
                cell3.innerHTML = Math.round(reponse[i][2]*1000)/1000;   //diametre fond de filet
                cell4.innerHTML = Math.round(reponse[i][3]*1000)/1000;   // diametre forage/percage
                cell5.innerHTML = Math.round(reponse[i][4]*1000)/1000;   //rayon
                cell6.innerHTML = Math.round(reponse[i][5]*1000)/1000;   // diametre sortie outil
                cell7.innerHTML = Math.round(reponse[i][6]*1000)/1000;   //hauteur min sortie outil
                cell8.innerHTML = Math.round(reponse[i][7]*1000)/1000;   //hauteur max sortie outil
                cell9.innerHTML = Math.round(reponse[i][8]*1000)/1000;   //chanfrein
                
            }
            
        }
        else if(document.getElementById('typeElement2').checked){    // Si le type d'élément est un ecrou
            console.log("ECROU METRIQUE");
            $('#FFecrou').hide();
            $('#diamSortieVis').hide();
            $('#hauteurMinVis').hide();
            $('#hauteurMaxVis').hide();
            $('#chanfrein').hide();
            $('#diamSortieEcrou').show();
            $('#hauteurMinEcrou').show();
            $('#hauteurMaxEcrou').show();

            for(let i=0;i<=reponse.length;i++){
                var row = tableau.insertRow();

                var cell1 = row.insertCell(0);
                var cell2 = row.insertCell(1);
                var cell3 = row.insertCell(2);
                var cell4 = row.insertCell(3);
                var cell5 = row.insertCell(4);
                var cell10 = row.insertCell(5);
                var cell11 = row.insertCell(6);
                var cell12 = row.insertCell(7);

                cell1.innerHTML = reponse[i][0];   // diametre nominal
                cell2.innerHTML = reponse[i][1];   // pas de filet
                cell3.innerHTML = Math.round(reponse[i][2]*1000)/1000;   //diametre fond de filet
                cell4.innerHTML = Math.round(reponse[i][3]*1000)/1000;   // diametre forage/percage
                cell5.innerHTML = Math.round(reponse[i][4]*1000)/1000;   //rayon
                cell10.innerHTML = Math.round(reponse[i][11]*1000)/1000;  //diametre entree outil
                cell11.innerHTML = Math.round(reponse[i][9]*1000)/1000; //hauteur min entree outil
                cell12.innerHTML = Math.round(reponse[i][10]*1000)/1000; //hauteur max entree outil
                
            }
            
        }
    }



    else if(reponse[0].length == 13){      // Si le type de filet est Rond
        console.log("ROND")
        if(document.getElementById('typeElement1').checked){    // Si le type d'élément est une vis
            console.log("VIS ROND")
             // HIDE TOUS LES TRUCS A HIDE
            $('#FFecrou').show(); 
            $('#diamSortieEcrou').hide();
            $('#hauteurMinEcrou').hide();
            $('#hauteurMaxEcrou').hide();
            $('#diamSortieVis').show();
            $('#hauteurMinVis').show();
            $('#hauteurMaxVis').show();
            $('#chanfrein').show();
            for(let i=0;i<=reponse.length;i++){
                var row = tableau.insertRow();

                var cell1 = row.insertCell(0);
                var cell2 = row.insertCell(1);
                var cell3 = row.insertCell(2);
                var cell4 = row.insertCell(3);
                var cell5 = row.insertCell(4);
                var cell6 = row.insertCell(5);
                var cell7 = row.insertCell(6);
                var cell8 = row.insertCell(7);
                var cell9 = row.insertCell(8);
                var cell10 = row.insertCell(9);
              


                cell1.innerHTML = reponse[i][0];   // diametre nominal
                cell2.innerHTML = reponse[i][1];   // pas de filet
                cell3.innerHTML = Math.round(reponse[i][2]*1000)/1000;   //diametre fond de filet vis
                cell4.innerHTML = Math.round(reponse[i][3]*1000)/1000;   // diametre fond de filet ecrou
                cell5.innerHTML = Math.round(reponse[i][4]*1000)/1000;   // diametre forage/percage
                cell6.innerHTML = Math.round(reponse[i][5]*1000)/1000;   //rayon
                cell7.innerHTML = Math.round(reponse[i][6]*1000)/1000;   // diametre sortie outil
                cell8.innerHTML = Math.round(reponse[i][7]*1000)/1000;   //hauteur min sortie outil
                cell9.innerHTML = Math.round(reponse[i][8]*1000)/1000;   //hauteur max sortie outil
                cell10.innerHTML = Math.round(reponse[i][9]*1000)/1000;   //chanfrein

            }
            
        }
        else if(document.getElementById('typeElement2').checked){    // Si le type d'élément est un ecrou
            console.log("ECROU ROND")
             // HIDE TOUS LES TRUCS A HIDE
            $('#FFecrou').show(); 
            $('#diamSortieVis').hide();
            $('#hauteurMinVis').hide();
            $('#hauteurMaxVis').hide();
            $('#chanfrein').hide();
            $('#diamSortieEcrou').show();
            $('#hauteurMinEcrou').show();
            $('#hauteurMaxEcrou').show();
            for(let i=0;i<=reponse.length;i++){
                var row = tableau.insertRow();

                var cell1 = row.insertCell(0);
                var cell2 = row.insertCell(1);
                var cell3 = row.insertCell(2);
                var cell4 = row.insertCell(3);
                var cell5 = row.insertCell(4);
                var cell6 = row.insertCell(5);
                var cell11 = row.insertCell(6);
                var cell12 = row.insertCell(7);
                var cell13 = row.insertCell(8);

                cell1.innerHTML = reponse[i][0];   // diametre nominal
                cell2.innerHTML = reponse[i][1];   // pas de filet
                cell3.innerHTML = Math.round(reponse[i][2]*1000)/1000;   //diametre fond de filet vis
                cell4.innerHTML = Math.round(reponse[i][3]*1000)/1000;   // diametre fond de filet ecrou
                cell5.innerHTML = Math.round(reponse[i][4]*1000)/1000;   // diametre forage/percage
                cell6.innerHTML = Math.round(reponse[i][5]*1000)/1000;  //rayon
                cell11.innerHTML = Math.round(reponse[i][12]*1000)/1000;  //diametre entree outil
                cell12.innerHTML = Math.round(reponse[i][10]*1000)/1000; //hauteur min entree outil
                cell13.innerHTML = Math.round(reponse[i][11]*1000)/1000; //hauteur max entree outil
            }
            
        }
    }

    else if(reponse[0].length == 14){      // Si le type de filet est Trapézoïdal
        console.log("TRAPEZOIDALE")
        if(document.getElementById('typeElement1').checked){    // Si le type d'élément est une vis
            console.log("VIS TRAP")
             // HIDE TOUS LES TRUCS A HIDE
            $('#FFecrou').show(); 
            $('#diamSortieEcrou').hide();
            $('#hauteurMinEcrou').hide();
            $('#hauteurMaxEcrou').hide();
            $('#diamSortieVis').show();
            $('#hauteurMinVis').show();
            $('#hauteurMaxVis').show();
            $('#chanfrein').show();
            for(let i=0;i<=reponse.length;i++){
                var row = tableau.insertRow();

                var cell1 = row.insertCell(0);
                var cell2 = row.insertCell(1);  
                var cell3 = row.insertCell(2);
                var cell4 = row.insertCell(3);
                var cell5 = row.insertCell(4);
                var cell6 = row.insertCell(5);
                var cell7 = row.insertCell(6);
                var cell8 = row.insertCell(7);
                var cell9 = row.insertCell(8);
                var cell10 = row.insertCell(9);
                
   
                
                cell1.innerHTML = reponse[i][0];   // diametre nominal
                cell2.innerHTML = reponse[i][1];   // pas de filet
                cell3.innerHTML = Math.round(reponse[i][2]*1000)/1000;   //diametre fond de filet vis
                cell4.innerHTML = Math.round(reponse[i][3]*1000)/1000;   // diametre fond de filet ecrou
                cell5.innerHTML = Math.round(reponse[i][4]*1000)/1000;   // diametre forage/percage
                cell6.innerHTML = Math.round(reponse[i][5]*1000)/1000;   //rayon
                cell7.innerHTML = Math.round(reponse[i][7]*1000)/1000;   // diametre sortie outil
                cell8.innerHTML = Math.round(reponse[i][8]*1000)/1000;   //hauteur min sortie outil
                cell9.innerHTML = Math.round(reponse[i][9]*1000)/1000;   //hauteur max sortie outil
                cell10.innerHTML = Math.round(reponse[i][10]*1000)/1000;   //chanfrein


            }
            
        }
        else if(document.getElementById('typeElement2').checked){    // Si le type d'élément est un ecrou
            console.log("ECROU TRAP")
             // HIDE TOUS LES TRUCS A HIDE
            $('#FFecrou').show(); 
            $('#diamSortieVis').hide();
            $('#hauteurMinVis').hide();
            $('#hauteurMaxVis').hide();
            $('#chanfrein').hide();
            $('#diamSortieEcrou').show();
            $('#hauteurMinEcrou').show();
            $('#hauteurMaxEcrou').show();
            for(let i=0;i<=reponse.length;i++){
                var row = tableau.insertRow();

                var cell1 = row.insertCell(0);
                var cell2 = row.insertCell(1);  
                var cell3 = row.insertCell(2);
                var cell4 = row.insertCell(3);
                var cell5 = row.insertCell(4);
                var cell6 = row.insertCell(5);
                var cell11 = row.insertCell(6);
                var cell12 = row.insertCell(7);
                var cell13 = row.insertCell(8);
                

                cell1.innerHTML = reponse [i][0];   // diametre nominal
                cell2.innerHTML = reponse [i][1];   // pas de filet
                cell3.innerHTML = Math.round(reponse[i][2]*1000)/1000;   //diametre fond de filet vis
                cell4.innerHTML = Math.round(reponse[i][3]*1000)/1000;   // diametre fond de filet ecrou
                cell5.innerHTML = Math.round(reponse[i][4]*1000)/1000;  // diametre forage/percage
                cell6.innerHTML = Math.round(reponse[i][5]*1000)/1000;   //rayon
                cell11.innerHTML = Math.round(reponse[i][13]*1000)/1000;  //diametre entree outil
                cell12.innerHTML = Math.round(reponse[i][11]*1000)/1000; //hauteur min entree outil
                cell13.innerHTML = Math.round(reponse[i][12]*1000)/1000; //hauteur max entree outil

            }
            
        }
    }

    return 
}

window.setTimeout(function() {
    $("#popup").show();
}, 50000);


$('#popupButton').click(function(){
    window.open("https://paypal.me/RobinLozina?country.x=BE&locale.x=fr_FR", "_blank","toolbar=no,titlebar=no,top=200,left=500,width=600,height=600");
    $('#popup').hide();
});


$('#buttonEmail').click(function(){
    email= $('#email').val();
    if(email == "Rick Astley"){
        window.open("https://www.youtube.com/watch?v=dQw4w9WgXcQ", "_blank");
    }
    window.open("mailto:r.lozina@student.helmo.be?subject=Bug report&body=" + email, "_blank");
});


/* Icon on click */
$('#linkedin').click(function(){
    window.open("https://linkedin.com/in/robin-lozina-405363253", "_blank");
});

$('#github').click(function(){
    window.open("https://github.com/RobinLozina", "_blank");
});

$('#paypal').click(function(){
    window.open("https://paypal.me/RobinLozina?country.x=BE&locale.x=fr_FR", "_blank","toolbar=no,titlebar=no,top=200,left=500,width=600,height=600");
});

