'use strict';

var $window = $(window);

function run()
{
	var fName = arguments[0],
		aArgs = Array.prototype.slice.call(arguments, 1);
	try {
		fName.apply(window, aArgs);
	} catch(err) {
		 
	}
};
 
/* chart
================================================== */
function _chart ()
{
	$('.b-results').appear(function() {
		setTimeout(function() {
			$('.chart').easyPieChart({
				easing: 'easeOutElastic',
				delay: 3000,
				barColor: '#369670',
				trackColor: '#fff',
				scaleColor: false,
				lineWidth: 21,
				trackWidth: 21,
				size: 250,
				lineCap: 'round',
				onStep: function(from, to, percent) {
					this.el.children[0].innerHTML = Math.round(percent);
				}
			});
		}, 150);
	});
};
 

$(document).ready(function() {
  
	run(_chart);
  
    
});

/***************************Filtering*********************************/
function myapp() {
    const buttons = document.querySelectorAll(".button");
    const chart = document.querySelectorAll(".feedback");
  
    function filter(feedback, items) {
      items.forEach((item) => {
        const isItemFiltered = !item.classList.contains(feedback);
        const isShowAll = feedback.toLowerCase() === "all";
        if (isItemFiltered && !isShowAll) {
          item.classList.add("hide");
        } else {
          item.classList.remove("hide");
        }
      });
    }
  
    buttons.forEach((button) => {
      button.addEventListener("click", () => {
		//chart.style="margin:auto";
	

        const currentFeedback = button.dataset.filter;
        console.log(currentFeedback);
        filter(currentFeedback, chart);
		

      });
    });
  }
  
  myapp();