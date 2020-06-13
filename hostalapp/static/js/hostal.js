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

      try {

        var rec = JSON.parse(data);

        if (rec.status=="success") {

          $("#formLogin").prop("action", rec.uri+"/");
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

function getOCEmpleados(ocId) {

  alert(ocId);

  var dataIn =
    {
      ocId : ocId,
    };

  $.post(
    "/getOCEmpleados",
    {
      data : JSON.stringify(dataIn),
      csrfmiddlewaretoken : $('input[name="csrfmiddlewaretoken"]').val(),
    },
    function (data) {

      alert(data);

      try {

        var rec = JSON.parse(data);

        if (rec.status=="success") {

          $("#modalOCEmpleadosBody").html(rec.html);

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

function selectElementMove(origenId, destinoId) {

  var sel=new Array();

  $("#"+origenId+" option").each(

    function (indice, valor) {

      if ($(this).prop("selected")) {

        el = { id : $(this).val(), text : $(this).text() };
        sel.push(el);
        $(this).remove();

      }

    }

  );

  $(sel).each(
    function (indice, valor) {

      $('#'+destinoId).append('<option value="'+valor.id+'">'+valor.text+'</option>');

    }
  )

}

function getPlatosSeleccion(objId) {

  $.post(

    "/getPlatosSeleccion",

    {
      csrfmiddlewaretoken : $('input[name="csrfmiddlewaretoken"]').val(),
    },

    function (data) {

      var rec=JSON.parse(data);

      // eliminando todos los items uno por uno
      $("#"+objId+" option").each(
        function (indice, valor) {
          $(this).remove();
        }
      );

      // recorriendo elementos recibidos en json e insertando al select
      $(rec).each(
        function (indice, valor) {
          $("#"+objId).append('<option value="'+valor.id+'">'+valor.nombre+'</option>');
        }
      );

      // ocultar engranaje
      $("#NuevaMinutaPladoSpin").fadeOut("slow");
      // mostrar selecciòn
      $("#NuevaMinutaPladoEdit").fadeIn("slow");

    }

  );


}
