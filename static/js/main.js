// Bevestigingsdialoog bij verwijderen (F50)
document.addEventListener("DOMContentLoaded", function () {
  document.querySelectorAll(".confirm-delete").forEach(function (form) {
    form.addEventListener("submit", function (e) {
      if (!confirm("Weet je zeker dat je dit wilt verwijderen?")) {
        e.preventDefault();
      }
    });
  });

  // Flash messages automatisch sluiten na 5 seconden
  document.querySelectorAll(".alert.alert-dismissible").forEach(function (alert) {
    setTimeout(function () {
      var bsAlert = bootstrap.Alert.getOrCreateInstance(alert);
      bsAlert.close();
    }, 5000);
  });
});
