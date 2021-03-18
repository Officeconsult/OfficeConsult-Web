$("#CRM-Key-set-btn").click(function () {
  var key = $("#CRM-Key-input-field").val();
  setCookie("crmkey", key, 10);
});

$("#CRM-Key-check-btn").click(function () {
  var currentCookie = getCookie("crmkey");
  if(currentCookie == null){
    alert("Could not find a valid cookie.");
  }else{
    alert(currentCookie);
  }
});

$("#CRM-Key-delete-btn").click(function () {
  eraseCookie("crmkey");
})