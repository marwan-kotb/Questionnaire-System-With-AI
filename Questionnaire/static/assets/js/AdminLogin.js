function clickedButton()
{
    var email = document.getElementById("email").value;
   var password = document.getElementById("password").value;
   if (email === "AM1234@fayoum.edu.eg" && password === "123456") {
        
   window.location.href="options.html";
}
}


function myFunction() {
    var x = document.getElementById("password");
    if (x.type === "password") {
      x.type = "text";
    } else {
      x.type = "password";
    }
  }