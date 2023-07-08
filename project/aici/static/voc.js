function edit_voc() {
    // '접수하러 가기' 버튼 클릭 시 이동할 페이지 URL을 입력해주세요.
    window.location.href = '../edit_voc/';
}

function toggleDropdown(dropdownId) {
  var dropdown = document.getElementById(dropdownId);
  dropdown.classList.toggle("show");
  if (!dropdown.classList.contains("show")) {
    var dropdownItems = dropdown.getElementsByClassName("dropdown-item");
    for (var i = 0; i < dropdownItems.length; i++) {
      dropdownItems[i].classList.remove("selected");
    }
  }
}

function filterByRepairStatus(status, filterType) {
  var rows = document.getElementsByClassName('tr-table-content');
  for (var i = 0; i < rows.length; i++) {
    var row = rows[i];
    var statusElement = row.getElementsByClassName(filterType)[0];
    var rowStatus = statusElement.innerText;
    if (rowStatus === status) {
      row.style.display = 'table-row';
    } else {
      row.style.display = 'none';
    }
  }

  var dropdownItems = document.getElementsByClassName("dropdown-item");
  for (var i = 0; i < dropdownItems.length; i++) {
    dropdownItems[i].classList.remove("selected");
    if (dropdownItems[i].innerText === status) {
      dropdownItems[i].classList.add("selected");
    }
  }

  toggleDropdown("fixFilterDropdown");
  toggleDropdown("vocFilterDropdown");
}

document.addEventListener("click", function (event) {
  var dropdowns = document.getElementsByClassName("dropdown-menu");
  for (var i = 0; i < dropdowns.length; i++) {
    var dropdown = dropdowns[i];
    if (!dropdown.contains(event.target)) {
      dropdown.classList.remove("show");
    }
  }
});
