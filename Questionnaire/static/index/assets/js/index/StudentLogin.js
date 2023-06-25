
let button=document.getElementById("btnL");
button.addEventListener('click',()=>{
    let email = document.getElementById("email").value;
    let password = document.getElementById("password").value;
     if (email === "ag1804@fayoum.edu.eg" && password === "123456") {
          
      window.location.href="subject.html";
  }else {
           alert("Invalid information");
              return;
  }
})
   



// ///////////////////////////////// Password /////////////////////////
let password = document.getElementById("password");
let showP = document.getElementById("show");
let hideP = document.getElementById("hide");
hideP.addEventListener('click', () => {
    showP.style.display = "block";
    hideP.style.display = "none";
    password.type = "text";
});
showP.addEventListener('click', () => {
    showP.style.display = "none";
    hideP.style.display = "block";
    password.type = "password";
})
