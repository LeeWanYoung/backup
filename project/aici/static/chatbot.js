var typingBool = false;
var typingIdx = 0;

var typingTxt = $(".typing-txt").text();

typingTxt = typingTxt.split("");

if (typingBool == false) {
  typingBool = true;
  var tyInt = setInterval(typing, 100);
}

function typing() {
  if (typingIdx < typingTxt.length) {
    $(".typing").append(typingTxt[typingIdx]);
    typingIdx++;
  } else {
    clearInterval(tyInt);
  }
}

document.addEventListener('DOMContentLoaded', function() {
  var sendButton = document.querySelector('.send-button');
  sendButton.addEventListener('click', checkResponse);
});

function handleKeyDown(event) {
  if (event.key === 'Enter') { // Enter 키를 눌렀을 때
      checkResponse();
  }
}

function checkResponse() {
  var response = document.querySelector('.chatting-textbox').value;
  if (response === '네') {
      window.location.href = "{% url 'aici:positive' %}";
  } else if (response === '아니요') {
      window.location.href = "{% url 'aici:negative' %}";
  }
}