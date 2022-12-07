$('#btnmetrique').click(function(){
    if($('#metriquedvnu').val() == '' || $('#metriquedenu').val() == '' || $('#metriquesurep').val() == '' || $('#metriquelon').val() == '' ){
        $('#messagemet').html('<p>Veuillez remplir tous les champs !</p>');
    }
    else{
        $('#messagemet').html('');



    }
});

$('#btnwithgaz').click(function(){
    if($('#withgazdvnu').val() == '' || $('#withgazdenu').val() == '' || $('#withgazsurep').val() == '' || $('#withgazlon').val() == '' ){
        $('#messagewithgaz').html('<p>Veuillez remplir tous les champs !</p>');
    }
    else{
        $('#messagewithgaz').html('');

    }
});

$('#btntrap').click(function(){
    if($('#trapdvnu').val() == '' || $('#trapdenu').val() == '' || $('#trapsurep').val() == '' || $('#traplon').val() == '' ){
        $('#messagetrap').html('<p>Veuillez remplir tous les champs !</p>');
    }
    else{
        $('#messagetrap').html('');

    }
});

$('#btnrond').click(function(){
    if($('#trapdvnu').val() == '' || $('#trapdenu').val() == '' || $('#trapsurep').val() == '' || $('#traplon').val() == '' ){
        $('#messagetrap').html('<p>Veuillez remplir tous les champs !</p>');
    }
    else{
        $('#messagetrap').html('');
    }
});

$('#typeFilet').change(function(){
    $('#metrique').hide();
    $('#withgaz').hide();
    $('#trap').hide();
    $('#rond').hide();

    if($('#typeFilet').val() == "1"){
        $('#metrique').show();
    }
    else if ($('#typeFilet').val() == "2"){
        $('#withgaz').show();
    }
    else if ($('#typeFilet').val() == "3"){
        $('#trap').show();
    }
    else{
        $('#rond').show();
    }
});

function AfficherTableau(reponse) {

    var donnees = JSON.parse(reponse);
    var tab = '<thead><tr><th>Données</th>';

    for (var k = 0; k < donnees.length; k++) {
        tab += '<th>Proposition ' + (k + 1) + '</th>';
    }
    
    tab +='</tr></thead><tbody>';

    var i = 0;
    var j = 0;

    for ( i; i < donnees.length; i++) {
        tab += '<tr>';

        while(donnes[i][j] != null) {
            tab += '<td>' + donnees[i][j] + '</td>';
            j++;
        }
        tab += '</tr>';
    }

    tab += '</tbody>';

    return tab
}