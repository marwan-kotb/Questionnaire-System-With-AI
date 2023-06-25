// ****************************JS to page subject*****************************


navigationHeight=document.getElementById('header').offsetHeight;
document.documentElement.style.setProperty('--scroll-padding',navigationHeight-1+'px');

let courses = document.getElementById("Courses");
let course = document.querySelectorAll(".course");
let aboutProf=document.getElementById("section2");
let button=document.getElementById('btn')

Array.from(course).map((ele) => {
    ele.addEventListener("click", () => {
        let data =
            ` <section class="courseName">
          <div>
              <li onclick="openFeedback(this)" class="type" id="lec">Lecture ${" " + ele.textContent
            }</li>
            </div>
                  <div class="questionnaire" id="questionnair" class="Qform" id="servey">
                      <textarea placeholder="Tell Us Your Opinion about${" " + ele.textContent
            }" id="textLec"  required="" ></textarea>
                  </div>
          <div>
              <li onclick="openFeedback(this)" class="type" id="lab">Lab ${" " + ele.textContent
            }</li></div>
        <div class="questionnaire" id="questionnair" class="Qform" id="servey">
                    <textarea placeholder="Tell Us Your Opinion about${" " + ele.textContent
            }" id="textLec"  required=""></textarea>
         </div>
        <div><li onclick="openFeedback(this)" class="type" id="sec">Section${" " + ele.textContent
            }</li></div>
        <div class="questionnaire" id="questionnair" class="Qform" id="servey">
           <textarea placeholder="Tell Us Your Opinion about${" " + ele.textContent
            }" id="textLec"  required=""></textarea>
        </div>
      
    </section>`;
        courses.innerHTML = data;
        aboutProf.style.display="block";
   
    });
});
let btn = document.querySelector('.btn');
function openFeedback(clicked) {
    clicked.parentElement.nextElementSibling.children[0].classList.toggle(
        "show"
    );

    button.style.display = "block";

}
btn.addEventListener('click', (e) => {
    function checkFeedback(check) {
        if (check.value === "") {
            console.log("you must type your feedback")
        } else {
            window.location.href = "final.html";
        }
    }

})

// ********************** JS to questionaire page ****************************
// create array to store data
let saveData = localStorage.getItem("servey");
let serveyList = JSON.parse(saveData || "[]");
// select the inputs of the form
let textLec = document.getElementById("textLec");
// get last id
let lastserveyId = serveyList.length;
// create a function to push new servey into the array
let newServey = () => {
    serveyList.push({
        textLec: textLec.value,
    });
    textLec.value = "";
};
// handel save btn listener
let saveBtn = document.getElementById("submit");
// add new servey handler
let saveBtnHandler = () => {
    newServey();
    localStorage.setItem("servey", JSON.stringify(serveyList));
};
saveBtn.addEventListener("click", () => {
    if (textLec.value != "") {
        saveBtnHandler();
        window.location.href = "final.html";
    } else {
        if (textLec.value == "") {
            window.alert("You forget write your opinion !!!");
        }
    }
});
////////////////////////////////////////////////////////////////////////
