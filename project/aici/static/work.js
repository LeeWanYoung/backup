window.addEventListener('load', function() {
    var newUrl = window.location.href.split('?')[0];
    history.replaceState({}, '', newUrl);
});

function search() {
    var startDate = new Date(document.getElementById("start_date").value);
    var endDate = new Date(document.getElementById("end_date").value);
    var errorMessage = document.getElementById("error-message");
    var posts = document.querySelectorAll(".table tbody tr");

    // 기존 검색 결과 숨기기
    for (var i = 0; i < posts.length; i++) {
        posts[i].style.display = "none";
    }

    if (!startDate || !endDate) {
        errorMessage.textContent = "시작일과 종료일을 모두 선택해주세요.";
        errorMessage.style.display = "block";
    } else {
        errorMessage.style.display = "none";

        for (var i = 0; i < posts.length; i++) {
            var postStartDate = new Date(posts[i].querySelector(".start_at").textContent.trim());
            var postEndDate = new Date(posts[i].querySelector(".end_at").textContent.trim());

            if (
                (startDate && (isNaN(startDate.getTime()) || startDate.getTime() !== postStartDate.getTime())) ||
                (endDate && (isNaN(endDate.getTime()) || endDate.getTime() !== postEndDate.getTime()))
            ) {
                posts[i].style.display = "none";
            } else {
                posts[i].style.display = "table-row";
            }
        }
    }
}

document.getElementById("search-button").addEventListener("click", function(event) {
    event.preventDefault(); // 폼 제출 방지
    search();
});