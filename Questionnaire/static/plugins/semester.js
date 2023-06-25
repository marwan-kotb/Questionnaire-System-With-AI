/* let semesterOneCourses=document.getElementsByClassName('coursesem1');
let semesterTwoCourses=document.getElementsByClassName('coursesem2');
let one=document.getElementById("one");
let two=document.getElementById("two");

let resultBtn=document.getElementsByClassName('btn')


let btnSemesterOne=document.querySelector('.btns1');
let btnSemesterTwo=document.querySelector('.btns2');

btnSemesterOne.addEventListener('click',()=>{
    one.style.display="block";
    for (const courseSem1 of semesterOneCourses){
        courseSem1.style.display="block";
    } 
   
})
btnSemesterTwo.addEventListener('click',()=>{
    two.style.display="block";
    for (const courseSem2 of semesterTwoCourses){
        courseSem2.style.display="block";
        
    }
    
    for (const courseSem1 of semesterOneCourses){
        courseSem1.style.display="none";
    }
    one.style.display="none";

    })
   
resultBtn.addEventListener('click',(e)=>{
    window.location.href='../result.html';
    e.preventDefault()
}) */