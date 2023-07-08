window.addEventListener("DOMContentLoaded", function () {
  var dateField = document.getElementById("id_date");
  if (!dateField.value) {
    // If the date field is empty, set it to today's date
    var today = new Date().toISOString().split("T")[0];
    dateField.value = today;
  }

  document.getElementById("post-form").addEventListener("submit", function (event) {
    event.preventDefault();
    if (confirm("정말로 접수하시겠습니까?")) {
      this.submit();
    }
  });
});
