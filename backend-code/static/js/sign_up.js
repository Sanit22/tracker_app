const password = document.getElementById("sign_up_password");
const con_password = document.getElementById("confirm_password");
const regex = /^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$/;
const password_warning = document.getElementById("password_warning");
const con_password_warning = document.getElementById("con_password_warning");
let validated = true;
const show_pass = document.getElementById("show_password");
const con_show_pass = document.getElementById("con_show_password");


password.addEventListener('input', function(){
    let curr_password = password.value;
    if(!curr_password.match(regex)){
        password_warning.style.display = 'block';
        validated = false;
    }
    else{
        password_warning.style.display = 'none';
        validated = true;
    }
});


con_password.addEventListener("input", function(){
    if(con_password.value != password.value){
        con_password_warning.style.display = 'block';
        validated = false;
    }
    else{
        con_password_warning.style.display = 'none';
        validated = true;
    }
});



show_pass.addEventListener('click', toggleShowHide.bind(null, password, show_pass));

con_show_pass.addEventListener('click', toggleShowHide.bind(null, con_password, con_show_pass));

function toggleShowHide(pass, text){
    console.log("INSIDE TOGGLLEE");
    if(pass.getAttribute('type') == "password"){
        pass.setAttribute('type', 'text');
        text.innerText = 'Hide'; 
    }
    else{
        pass.setAttribute('type', 'password');
        text.innerText = 'Show';   
    }
}
