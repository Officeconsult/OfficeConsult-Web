$("#CRM-Key-set-btn").click(function () {
    var key = $("#CRM-Key-input-field").val();
    setCookie("crmkey", key, 10);
  });
  
  $("#CRM-Key-check-btn").click(function () {
    alert(getCookie("crmkey"));
  });
  