let admin1 = document.getElementById("admin1"); //Admin button in First page
admin1.addEventListener('click', () => {
    window.location.href = "AdminLogin.html"; //login page
})

let admin2 = document.getElementById("admin2"); //Admin button in First page
admin2.addEventListener('click', () => {
    window.location.href = "AdminLogin.html"; //login page
})

let student=document.getElementById("student");
student.addEventListener('click',()=>{
    window.location.href="StudentLogin.html";
})