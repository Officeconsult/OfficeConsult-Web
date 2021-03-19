function atRequest(){
    $.ajax({
        url: 'https://api.airtable.com/v0/appPu05N346JHlDTg/Utviklere',
        beforeSend: function(xhr) {
             xhr.setRequestHeader("Authorization", "Bearer " + currentCRMKey)
        }, success: function(data){
            alert(data);
            //process the JSON data etc
        }
    })
}
