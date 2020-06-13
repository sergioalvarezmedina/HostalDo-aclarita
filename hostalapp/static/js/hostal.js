
function onlyNum(e) {

  var n = "1234567890"+String.fromCharCode(8)+String.fromCharCode(9);
  var k = (e.which)?e.which:e.keyCode;

  return (n.indexOf(String.fromCharCode(k)) > -1);

}

function showProcess(msg) {

  $("#modalProcessBody").html(msg);
  $("#modalProcess").modal("show");

}

function hideProcess() {

  $("#modalProcess").modal("hide");

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

function getPlatosSeleccion(origenId, destinoId) {

  $.post(

    "/getPlatosSeleccion",

    {
      csrfmiddlewaretoken : $('input[name="csrfmiddlewaretoken"]').val(),
    },

    function (data) {

      var rec=JSON.parse(data);


      cleanSelect(origenId);
      cleanSelect(destinoId);
      // recorriendo elementos recibidos en json e insertando al select
      $(rec).each(
        function (indice, valor) {
          $("#"+origenId).append('<option value="'+valor.id+'">'+valor.nombre+'</option>');
        }
      );

      // ocultar engranaje
      $("#NuevaMinutaPladoSpin").fadeOut("slow");
      // mostrar selecciòn
      $("#NuevaMinutaPladoEdit").fadeIn("slow");

    }

  );


}

function cleanSelect(objId) {

  $("#"+objId+" option").each(
    function (indice, valor) {
      $(this).remove();
    }
  );

}

function setMinuta(selId) {

  var sel=new Array();

  $("#"+selId+" option").each(

    function (indice, valor) {

      el = { id : $(this).val(), text : $(this).text() };
      sel.push(el);
      $(this).remove();

    }

  );

  if (!sel.length || sel.length==0) {

    alert("Para proceder con el registro de la nueva minuta se requiere como mìnimo la inclusión de un plato.");
    return;

  }

  $("#NuevaMinutaCerrar").prop("disabled", true);
  $("#NuevaMinutaGuardar").prop("disabled", true);

  $("#NuevaMinutaPladoEdit").html("Guardando minuta... ");
  $("#NuevaMinutaPladoEdit").fadeOut("slow");
  $("#NuevaMinutaPladoSpin").fadeIn("slow");

  $.post(

    "/setMinutaPlatos",

    {
      data : sel,
      csrfmiddlewaretoken : $('input[name="csrfmiddlewaretoken"]').val(),
    },

    function (data) {

      alert(data);

      var rec=JSON.parse(data);

    }

  );

}
