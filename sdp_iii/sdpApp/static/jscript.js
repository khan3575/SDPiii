var password = document.getElementById("password");
var confirm_password = document.getElementById("confirmation-password");

function validatePassword(){
    if(password.value != confirm_password.value)
    {
        confirm_password.setCustomValidty("Password Doesn't Match");
    }
    else{
        confirm_password.setCustomValidty('');
    }
    password.onchange = validatePassword;
    confirm_password.onkeyup= validatePassword;
}
