$('#btnSend').click(function(){

    if(($('#diamVis').val() == '' && $('#diamEcrou').val() == '') || $('#surepaisseurUsinage').val() == '' || $('#longueur').val() == '' ){
        $('#errorMessage').html('<p>Veuillez remplir tous les champs !</p>');
    }
    else{
        if(document.getElementById('typeFilet1').checked){ // Si le type de filet est métrique 
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
            'lon': $('#longueur').val(),
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

            var element = 0; // 0 = vis, 1 = ecrou
            if(document.getElementById('typeElement2').checked){
                element = 1;
            }
            var data= {
                'dvnu': $('#diamVis').val(),
                'denu': $('#diamEcrou').val(),
                'surep': $('#surepaisseurUsinage').val(),
                'lon': $('#longueur').val(),
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
            'lon': $('#longueur').val(),
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
            'lon': $('#longueur').val(),
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


$('#typeElement').click(function(){      // Afficher le bon champ en fonction du type d'élément (ecrou ou vis) et reset l'autre champ
    $('#questionTextDiv').show();
    if(document.getElementById('typeElement1').checked){
        $('#diamEcrou').val('');
        $('#diamEcrouDiv').hide();
        $('#diamVisDiv').show();

    }
    else if(document.getElementById('typeElement2').checked){
        $('#diamVis').val('');
        $('#diamVisDiv').hide();
        $('#diamEcrouDiv').show();

    }
});



// $('#btnwithgaz').click(function(){
//     if($('#withgazdvnu').val() == '' || $('#withgazdenu').val() == '' || $('#withgazsurep').val() == '' || $('#withgazlon').val() == '' ){
//         $('#messagewithgaz').html('<p>Veuillez remplir tous les champs !</p>');
//     }
//     else{
//         $('#messagewithgaz').html('');

//     }
// });

// $('#btntrap').click(function(){
//     if($('#trapdvnu').val() == '' || $('#trapdenu').val() == '' || $('#trapsurep').val() == '' || $('#traplon').val() == '' ){
//         $('#messagetrap').html('<p>Veuillez remplir tous les champs !</p>');
//     }
//     else{
//         $('#messagetrap').html('');

//     }
// });

// $('#btnrond').click(function(){
//     if($('#trapdvnu').val() == '' || $('#trapdenu').val() == '' || $('#trapsurep').val() == '' || $('#traplon').val() == '' ){
//         $('#messagetrap').html('<p>Veuillez remplir tous les champs !</p>');
//     }
//     else{
//         $('#messagetrap').html('');
//     }
// });

// $('#typeFilet').change(function(){
//     $('#metrique').hide();
//     $('#withgaz').hide();
//     $('#trap').hide();
//     $('#rond').hide();

//     if($('#typeFilet').val() == "1"){
//         $('#metrique').show();
//     }
//     else if ($('#typeFilet').val() == "2"){
//         $('#withgaz').show();
//     }
//     else if ($('#typeFilet').val() == "3"){
//         $('#trap').show();
//     }
//     else{
//         $('#rond').show();
//     }
// });



function AfficherTableau(reponse) {

    var donnees = JSON.parse(reponse);
    var tableau =document.getElementById('tableau');
    compteur = 1;

    if(reponse[0].length == 11){           // Si le type de filet est WithGaz
        if(document.getElementById('typeElement1').checked){    // Si le type d'élément est une vis
            $('#FFecrou').hide();
            // HIDE TOUS LES TRUCS A HIDE
            for(let i=0;i<=reponse.length;i++){
                var row = tableau.insertRow(compteur);

                var cell1 = row.insertCell(0);
                var cell2 = row.insertCell(1);
                var cell3 = row.insertCell(2);
                var cell4 = row.insertCell(4);
                var cell5 = row.insertCell(5);
                var cell6 = row.insertCell(6);
                var cell7 = row.insertCell(7);
                var cell8 = row.insertCell(8);
                var cell9 = row.insertCell(9);


                cell1.innerHTML = reponse[i][0];   // diametre nominal
                cell2.innerHTML = reponse[i][1];   // pas de filet
                cell3.innerHTML = reponse[i][2];   //diametre fond de filet
                cell4.innerHTML = reponse[i][2];   // diametre forage/percage
                cell5.innerHTML = reponse[i][3];   //rayon
                cell6.innerHTML = reponse[i][4];   // diametre sortie outil
                cell7.innerHTML = reponse[i][5];   //hauteur min sortie outil
                cell8.innerHTML = reponse[i][6];   //hauteur max sortie outil
                cell9.innerHTML = reponse[i][7];   //chamfrein

                
            }
            compteur++;
        }
        else if(document.getElementById('typeElement2').checked){    // Si le type d'élément est un ecrou
            $('#FFecrou').hide();
                        // HIDE TOUS LES TRUCS A HIDE
            for(let i=0;i<=reponse.length;i++){
                var row = tableau.insertRow(compteur);

                var cell1 = row.insertCell(0);
                var cell2 = row.insertCell(1);
                var cell3 = row.insertCell(2);
                var cell7 = row.insertCell(7);
                var cell8 = row.insertCell(8);
                var cell9 = row.insertCell(9);
                var cell10 = row.insertCell(10);
                var cell11 = row.insertCell(11);
                var cell12 = row.insertCell(12);


                cell1.innerHTML = reponse[i][0];   // diametre nominal
                cell2.innerHTML = reponse[i][1];   // pas de filet
                cell3.innerHTML = reponse[i][2];   //diametre fond de filet
                cell4.innerHTML = reponse[i][2];   // diametre forage/percage
                cell5.innerHTML = reponse[i][3];   //rayon
                cell9.innerHTML = reponse[i][7];   //chamfrein
                cell10.innerHTML = reponse[i][10];  //diametre entree outil
                cell11.innerHTML = reponse[i][8]; //hauteur min entree outil
                cell12.innerHTML = reponse[i][9]; //hauteur max entree outil
                
            }
            compteur++;
        }
    }






    else if(reponse[0].length == 12){      // Si le type de filet est Metrique
        if(document.getElementById('typeElement1').checked){    // Si le type d'élément est une vis
                        // HIDE TOUS LES TRUCS A HIDE

            for(let i=0;i<=response.length;i++){
                var row = tableau.insertRow(compteur);

                var cell1 = row.insertCell(0);
                var cell2 = row.insertCell(1);
                var cell3 = row.insertCell(2);
                var cell4 = row.insertCell(4);
                var cell5 = row.insertCell(5);
                var cell6 = row.insertCell(6);
                var cell7 = row.insertCell(7);
                var cell8 = row.insertCell(8);
                var cell9 = row.insertCell(9);


                cell1.innerHTML = reponse[i][0];   // diametre nominal
                cell2.innerHTML = reponse[i][1];   // pas de filet
                cell3.innerHTML = reponse[i][2];   //diametre fond de filet
                cell4.innerHTML = reponse[i][3];   // diametre forage/percage
                cell5.innerHTML = reponse[i][4];   //rayon
                cell6.innerHTML = reponse[i][5];   // diametre sortie outil
                cell7.innerHTML = reponse[i][6];   //hauteur min sortie outil
                cell8.innerHTML = reponse[i][7];   //hauteur max sortie outil
                cell9.innerHTML = reponse[i][8];   //chamfrein
                
            }
            compteur++;
        }
        else if(document.getElementById('typeElement2').checked){    // Si le type d'élément est un ecrou
                        // HIDE TOUS LES TRUCS A HIDE

            for(let i=0;i<=response.length;i++){
                var row = tableau.insertRow(compteur);

                var cell1 = row.insertCell(0);
                var cell2 = row.insertCell(1);
                var cell3 = row.insertCell(2);
                var cell4 = row.insertCell(4);
                var cell8 = row.insertCell(8);
                var cell9 = row.insertCell(9);
                var cell10 = row.insertCell(10);
                var cell11 = row.insertCell(11);
                var cell12 = row.insertCell(12);

                cell1.innerHTML = reponse[i][0];   // diametre nominal
                cell2.innerHTML = reponse[i][1];   // pas de filet
                cell3.innerHTML = reponse[i][2];   //diametre fond de filet
                cell4.innerHTML = reponse[i][3];   // diametre forage/percage
                cell5.innerHTML = reponse[i][4];   //rayon
                cell9.innerHTML = reponse[i][8];   //chamfrein
                cell10.innerHTML = reponse[i][11];  //diametre entree outil
                cell11.innerHTML = reponse[i][9]; //hauteur min entree outil
                cell12.innerHTML = reponse[i][10]; //hauteur max entree outil
                
            }
            compteur++;
        }
    }



    else if(reponse[0].length == 13){      // Si le type de filet est Rond
        if(document.getElementById('typeElement1').checked){    // Si le type d'élément est une vis
             // HIDE TOUS LES TRUCS A HIDE
            for(let i=0;i<=response.length;i++){
                var row = tableau.insertRow(compteur);

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
                cell3.innerHTML = reponse[i][2];   //diametre fond de filet vis
                cell4.innerHTML = reponse[i][3];   // diametre fond de filet ecrou
                cell5.innerHTML = reponse[i][4];   // diametre forage/percage
                cell6.innerHTML = reponse[i][5];   //rayon
                cell7.innerHTML = reponse[i][6];   // diametre sortie outil
                cell8.innerHTML = reponse[i][7];   //hauteur min sortie outil
                cell9.innerHTML = reponse[i][8];   //hauteur max sortie outil
                cell10.innerHTML = reponse[i][9];   //chamfrein

            }
            compteur++;
        }
        else if(document.getElementById('typeElement2').checked){    // Si le type d'élément est un ecrou
             // HIDE TOUS LES TRUCS A HIDE
            for(let i=0;i<=response.length;i++){
                var row = tableau.insertRow(compteur);

                var cell1 = row.insertCell(0);
                var cell2 = row.insertCell(1);
                var cell3 = row.insertCell(2);
                var cell4 = row.insertCell(3);
                var cell5 = row.insertCell(4);
                var cell6 = row.insertCell(5);
                var cell10 = row.insertCell(9);
                var cell11 = row.insertCell(10);
                var cell12 = row.insertCell(11);
                var cell13 = row.insertCell(12);

                cell1.innerHTML = reponse[i][0];   // diametre nominal
                cell2.innerHTML = reponse[i][1];   // pas de filet
                cell3.innerHTML = reponse[i][2];   //diametre fond de filet vis
                cell4.innerHTML = reponse[i][3];   // diametre fond de filet ecrou
                cell5.innerHTML = reponse[i][4];   // diametre forage/percage
                cell6.innerHTML = reponse[i][5];   //rayon
                cell10.innerHTML = reponse[i][9];   //chamfrein
                cell11.innerHTML = reponse[i][10];  //diametre entree outil
                cell12.innerHTML = reponse[i][11]; //hauteur min entree outil
                cell13.innerHTML = reponse[i][12]; //hauteur max entree outil
            }
            compteur++;
        }
    }

    else if(reponse[0].length == 14){      // Si le type de filet est Trapézoïdal
        if(document.getElementById('typeElement1').checked){    // Si le type d'élément est une vis
             // HIDE TOUS LES TRUCS A HIDE

            for(let i=0;i<=response.length;i++){
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
                cell3.innerHTML = reponse[i][2];   //diametre fond de filet vis
                cell4.innerHTML = reponse[i][3];   // diametre fond de filet ecrou
                cell5.innerHTML = reponse[i][4];   // diametre forage/percage
                cell6.innerHTML = reponse[i][5];   //rayon
                cell7.innerHTML = reponse[i][7];   // diametre sortie outil
                cell8.innerHTML = reponse[i][8];   //hauteur min sortie outil
                cell9.innerHTML = reponse[i][9];   //hauteur max sortie outil
                cell10.innerHTML = reponse[i][10];   //chamfrein


            }
            compteur++;
        }
        else if(document.getElementById('typeElement2').checked){    // Si le type d'élément est un ecrou
             // HIDE TOUS LES TRUCS A HIDE
            for(let i=0;i<=response.length;i++){
                var cell1 = row.insertCell(0);
                var cell2 = row.insertCell(1);  
                var cell3 = row.insertCell(2);
                var cell4 = row.insertCell(3);
                var cell5 = row.insertCell(4);
                var cell6 = row.insertCell(5);
                var cell10 = row.insertCell(9);
                var cell11 = row.insertCell(10);
                var cell12 = row.insertCell(11);
                var cell13 = row.insertCell(12);
                
                cell1.innerHTML = reponse[i][0];   // diametre nominal
                cell2.innerHTML = reponse[i][1];   // pas de filet
                cell3.innerHTML = reponse[i][2];   //diametre fond de filet vis
                cell4.innerHTML = reponse[i][3];   // diametre fond de filet ecrou
                cell5.innerHTML = reponse[i][4];   // diametre forage/percage
                cell6.innerHTML = reponse[i][5];   //rayon
                cell10.innerHTML = reponse[i][10];   //chamfrein
                cell11.innerHTML = reponse[i][11];  //diametre entree outil
                cell12.innerHTML = reponse[i][12]; //hauteur min entree outil
                cell13.innerHTML = reponse[i][13]; //hauteur max entree outil


            }
            compteur++;
        }
    }
    return 
}