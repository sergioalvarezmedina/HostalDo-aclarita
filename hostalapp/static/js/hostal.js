
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

      var rec=JSON.parse(data);

    }

  );

}

//function showModificarEstado(habitacionId) {

//  if (confirm("¿Esta seguro de Modificar la habitación seleccionada?")) {

    //unsetHabitacion1(habitacionId);

//  }

//}

function unsetHabitacion1(habitacionId) {

  var sel={};

  var index=0;
  $("input[name='sel']:checked").each(
    function(){
      sel[index++]=$(this).val();
    }
  );

  $.post(
    "/unsetHabitacion",
    {
      sel : JSON.stringify(sel),
      csrfmiddlewaretoken : $('input[name="csrfmiddlewaretoken"]').val(),
    },

    function (data) {

      try {

        var rec=JSON.parse(data);

        if (rec.status=="success") {

          location.reload();

        } else {

          showMessage(rec.msg);

        }

      } catch (ex) {

        erJson();

      }

    }

  );

}



function showHabitacionEliminar(habitacionId) {

  if (confirm("¿Esta seguro de eliminar la habitación seleccionada?")) {

    unsetHabitacion(habitacionId);

  }


}

function showHabitacionEstado(habitacionId) {

  if (confirm("¿Esta seguro de cambiar el estado de la habitación seleccionada?")) {

    setHabitacionEstado(habitacionId);

  }


}


function unsetHabitacion(habitacionId) {

  var sel={};

  var index=0;
  $("input[name='sel']:checked").each(
    function(){
      sel[index++]=$(this).val();
    }
  );

  $.post(
    "/unsetHabitacion",
    {
      sel : JSON.stringify(sel),
      csrfmiddlewaretoken : $('input[name="csrfmiddlewaretoken"]').val(),
    },

    function (data) {

      try {

        var rec=JSON.parse(data);

        if (rec.status=="success") {

          location.reload();

        } else {

          showMessage(rec.msg);

        }

      } catch (ex) {

        erJson();

      }

    }

  );

}

function setHabitacionEstado(habitacionId) {

  var sel={};

  var index=0;
  $("input[name='sel']:checked").each(
    function(){
      sel[index++]=$(this).val();
    }
  );

  $.post(
    "/setHabitacioEstado",
    {
      sel : JSON.stringify(sel),
      estado : $("#estado").val(),
      csrfmiddlewaretoken : $('input[name="csrfmiddlewaretoken"]').val(),
    },

    function (data) {

      try {

        var rec=JSON.parse(data);

        if (rec.status=="success") {

          location.reload();

        } else {

          showMessage(rec.msg);

        }

      } catch (ex) {

        erJson();

      }

    }

  );

}

function getComuna(regionId, objId) {

  var dataIn =
    {
      regionId : regionId,
    };

  $.post(
    "/getComunaList",
    {
      data : JSON.stringify(dataIn),
      csrfmiddlewaretoken : $('input[name="csrfmiddlewaretoken"]').val(),
    },
    function (data) {

      try {

        var rec = JSON.parse(data);

        if (rec.status=="success") {

          $("#"+objId).html(rec.html);

        } else {

          showMessage(rec.msg);

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

function validaOrganismo() {

  var error='';

  if ($.trim($("#rol_empresa").val())=="") {
    error='- Rut empresa es obligatorio.';
  }
  if ($("#comunaId").val()=="0" || $("#regionId").val()=="0") {
    error='- Comuna de la empresa es obligatorio.';
  }
  if ($.trim($("#nombre_fantasia").val())=="") {
    error='- Rut empresa es obligatorio.';
  }
  if ($.trim($("#nombre_persona").val())=="") {
    error='- Nombre de contacto es obligatorio.';
  }
  if ($.trim($("#Ap_paterno").val())=="") {
    error='- Apellido paterno contacto es obligatorio.';
  }

  if (error!='') {

    alert('Se han encontrado los siguientes problemas de validación:\n'+error);
    return false;

  }

}

function getClienteRut(rut) {

  $("#rut").prop("disabled", true);
  $("#nombre_persona").prop("disabled", true);
  $("#apellido").prop("disabled", true);
  $("#cargo").prop("disabled", true);

  var dataIn =
    {
      rut : rut,
    };

  $.post(
    "/getClienteRut",
    {
      data : JSON.stringify(dataIn),
      csrfmiddlewaretoken : $('input[name="csrfmiddlewaretoken"]').val(),
    },
    function (data) {

      try {

        var rec = JSON.parse(data);

        if (rec.status=="success") {

          $("#msg").html("Se han recuperado los datos del empleado especificado.");
          $("#msg").fadeIn("slow").delay(3000).fadeOut("slow");

          $("#nombre_persona").val(rec.nombres);
          $("#apellido").val(rec.paterno);
          $("#cargo").val(rec.cargo);

        } else {

          $("#msg").html("<b>El rut consultado no fu&eacute; hallado.</b>");
          $("#msg").fadeIn("slow").delay(3000).fadeOut("slow");

        }

        $("#rut").prop("disabled", false);
        $("#nombre_persona").prop("disabled", false);
        $("#apellido").prop("disabled", false);
        $("#cargo").prop("disabled", false);
        $("#nombre_persona").focus();

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

function validaInsertEmpleado() {

  if ($.trim($("#rut").val())=="" ||
        $.trim($("#nombre_persona").val())=="" ||
        $.trim($("#apellido").val())=="" ||
        $.trim($("#cargo").val())=="") {

      alert("Para incluir un empleado en la orden de compra se requieren todos los datos del formulario.");
      return false;

  }

}
