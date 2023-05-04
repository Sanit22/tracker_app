const datetime = document.getElementById("datetime");
const form = document.getElementById("log_form");
const timestamp = document.getElementById("timestamp");
console.log("INSIDE LOG FORM")
form.onsubmit = function(e){
    timestamp.value = datetime.value;
}


