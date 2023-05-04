const trackerCreate = document.getElementById("create-tracker-button");
trackerCreate.onclick = function(){
    location.href = "/create_tracker";
}

const flashDiv = document.getElementById("flash-message");

setTimeout(() => {
    flashDiv.style.display = "none";
  }, "3000")