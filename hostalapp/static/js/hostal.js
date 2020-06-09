function onlyNum(e) {

  var n = "1234567890"+String.fromCharCode(8)+String.fromCharCode(9);
  var k = (e.which)?e.which:e.keyCode;

  return (n.indexOf(String.fromCharCode(k)) > -1);

}

function setDesktop(uriForm) {

  $("#form-menu").prop("action", uriForm);
  $("#form-menu").submit();

}


function showMessage(msg) {

  $("#modalMessageBody").html(msg);
  $("#modalMessage").modal("show");

}

function erJson() {

  showMessage("No es posible procesar la respuesta recibida.");
  return;

}

function setLogin(user, pass) {

  var dataIn =
    {
      user : user,
      pass : pass,
    };

  $.post(
    "/setLogin",
    {
      data : JSON.stringify(dataIn),
      csrfmiddlewaretoken : $('input[name="csrfmiddlewaretoken"]').val(),
    },
    function (data) {

      alert(data);

      try {

        var rec = JSON.parse(data);

        if (rec.status=="success") {

          $("#formLogin").prop("action", "/"+rec.uri);
          $("#formLogin").submit();

        } else {

          showMessage('Credenciales incorrectas');

        }

      } catch (ex) {

        erJson();

      }

    }
  )
  .fail(
    function (jqXHR, textStatus, errorThrown) {
      console.log("Error "+jqXHR.responseText);
      alert("Se ha producido una excepción.");
    }
  );

}
