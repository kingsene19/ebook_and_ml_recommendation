var id = document.getElementById('submit');

id.addEventListener('click', function(ev) {
ev.preventDefault();
  $.ajax({
    type: "POST",
    url: 'http://127.0.0.1:8000/commandes/ajouter/',
    data: {
      csrfmiddlewaretoken: "{{csrf_token}}",
      action: "post",
    },
    success: function (json) {
      window.location.replace("http://127.0.0.1:8000/commandes/paiement_confirme.html");
    }
  });
});
