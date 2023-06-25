function clickedButton()
{
    let email = document.getElementById("email").value;
   let password = document.getElementById("password").value;
   if (email == "ag1804@fayoum.edu.eg" && password == 123456) {
        
   window.location.href="courses.html";
}
}


function myFunction() {
    let x = document.getElementById("password");
    if (x.type === "password") {
      x.type = "text";
    } else {
      x.type = "password";
    }
  }