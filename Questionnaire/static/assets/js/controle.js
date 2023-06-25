  function addRow() {
    var table = document.querySelector("table");
    var tbody = table.querySelector("tbody");
    var lastRow = tbody.rows[tbody.rows.length - 1];
    var newRow = lastRow.cloneNode(true);
    var inputs = newRow.querySelectorAll("input");
    for (var i = 0; i < inputs.length - 1; i++) {
      inputs[i].value = "";
    }
    tbody.appendChild(newRow);
  }

  function addRows(rows) {
    var table = document.querySelector("table");
    var tbody = table.querySelector("tbody");
    // get faculty data from html

    for (var j = 0; j < rows.length; j++) {
      var row = rows[j];
      var lastRow = tbody.rows[tbody.rows.length - 1];
      var newRow = lastRow.cloneNode(true);
      var inputs = newRow.querySelectorAll("input");
      for (var i = 0; i < inputs.length - 1; i++) {
        inputs[i].value = row[i];
        
        
      }
      tbody.appendChild(newRow);
      if (tbody.rows.length === 2 && tbody.rows[0].querySelector("input").value === "") {
        tbody.removeChild(tbody.rows[0]);
      }
      
    }
    
  };


  function removeRow(button) {
    var row = button.parentNode.parentNode;
    row.parentNode.removeChild(row);
  }


  function editRow(button) {
    var row = button.parentNode.parentNode;
    var inputs = row.querySelectorAll("input[type='text'], input[type='number']");
    for (var i = 0; i < inputs.length; i++) {
      inputs[i].removeAttribute("readonly");
      inputs[i].classList.add("editable");
    }
    var buttons = row.querySelectorAll(".edit, .remove");
    for (var i = 0; i < buttons.length; i++) {
      buttons[i].style.display = "none";
    }
    button.style.display = "none";
    row.querySelector(".save").style.display = "inline-block";
    row.querySelector(".cancel").style.display = "inline-block";
  }



  function loadFile(file) {
    var reader = new FileReader();
    reader.onload = function(event) {
      var data = event.target.result;
      var workbook = XLSX.read(data, {type: 'binary'});
      var sheetName = workbook.SheetNames[0];
      var worksheet = workbook.Sheets[sheetName];
      var rows = XLSX.utils.sheet_to_json(worksheet, {header:1});
      addRows(rows);
    };
    reader.readAsBinaryString(file);
   

  }



  function modifyCheckboxValue(checkbox) {
    var row = checkbox.closest("tr");  // find the closest parent tr element
    var semesterNoInput = row.querySelector("[name='semester_no']");  // find the semester_no input in the same row
    if (checkbox.checked) {
        checkbox.value = semesterNoInput.value;  // modify the value if the checkbox is checked
        if (checkbox.name=="has_lab") {
          row.querySelector("[name='instructor_lab']").setAttribute("required", "required");
        }
        else{
          row.querySelector("[name='instructor_lab']").removeAttribute("required");
        }
        if (checkbox.name=="has_section") {
          row.querySelector("[name='instructor_sec']").setAttribute("required", "required");
        } 
        else{
          row.querySelector("[name='instructor_sec']").removeAttribute("required");
        }
      }
    
    else {
        checkbox.value = "";  // clear the value if the checkbox is unchecked
    
    }



  }