$(document).on('click', '.table tbody tr td .btn-success', function() {
    var html = '';
    html += "<tr><td class='no'></td>"
    html += "<td class='name'></td>"
    html += "<td class='password'></td>"
    html += "<td class='mail' ></td>"
    html += "<td class='level' ></td>"
    html += "<td><button type='button' class='btn btn-success'>Add</button> <button class='btn btn-danger' type='button'>Remove</button> <button class='btn edit' type='button'>Edit</button><button class='btn save'> Save </button> </td>"
    html += "</tr>"

    $(this).parent().parent().after(html)
})

$(document).on('click', '.table tbody tr td .btn-danger', function() {
    $(this).parent().parent().remove()
});


//edit Student No
$(document).on('click', '.table tbody tr td .edit', function() {  
    $(this).parent().siblings('td.no').each(function() {  
      var content = $(this).html();  
      $(this).html('<input value="' + content + '" />');  
    });  
    $(this).siblings('.save').show();  
     
   
  });  

  //edit Student Name
$(document).on('click', '.table tbody tr td .edit', function() {  
    $(this).parent().siblings('td.name').each(function() {  
      var content = $(this).html();  
      $(this).html('<input value="' + content + '" />');  
    });  
    $(this).siblings('.save').show();  
     
   
  }); 

//edit Student Phone
$(document).on('click', '.table tbody tr td .edit', function() {  
    $(this).parent().siblings('td.password').each(function() {  
      var content = $(this).html();  
      $(this).html('<input value="' + content + '" />');  
    });  
    $(this).siblings('.save').show();  
     
   
  }); 


 

  //edit Student Courses
$(document).on('click', '.table tbody tr td .edit', function() {  
    $(this).parent().siblings('td.mail').each(function() {  
      var content = $(this).html();  
      $(this).html('<input value="' + content + '" />');  
    });  
    $(this).siblings('.save').show();  
     
   
  }); 





  //edit Student E-mail
  $(document).on('click', '.table tbody tr td .edit', function() {  
    $(this).parent().siblings('td.level').each(function() {  
      var content = $(this).html();  
      $(this).html('<input value="' + content + '" />');  
    });  
    $(this).siblings('.save').show();  
     
   
  });

  $(document).on('click', '.table tbody tr td .save', function() {  
    $('input').each(function() {  
      var content = $(this).val();  
      $(this).html(content);  
      $(this).contents().unwrap();  
    });  
    $(this).siblings('.edit').show();  
    $(this).siblings('.delete').show();  
   
  });  



var ExcelToJSON = function() {

this.parseExcel = function(file) {
    var reader = new FileReader();

    reader.onload = function(e) {
        var data = e.target.result;
        var workbook = XLSX.read(data, {
            type: 'binary'
        });
        workbook.SheetNames.forEach(function(sheetName) {
            // Here is your object
            var XL_row_object = XLSX.utils.sheet_to_row_object_array(workbook.Sheets[sheetName]);
            var json_object = JSON.stringify(XL_row_object);
            productList = JSON.parse(json_object);

            var rows = $('.table tbody tr', );
            console.log(productList)
            for (i = 0; i < productList.length; i++) {

                var columns = Object.values(productList[i])
                rows.eq(i).find('td.no').text(columns[0]);
                rows.eq(i).find('td.name').text(columns[1]);
                rows.eq(i).find('td.password').text(columns[2]);
                rows.eq(i).find('td.mail').text(columns[3]);
                rows.eq(i).find('td.level').text(columns[4]);
            }

        })
    };
    reader.onerror = function(ex) {
        console.log(ex);
    };

    reader.readAsBinaryString(file);



};
};

function handleFileSelect(evt) {

var files = evt.target.files; // FileList object
var xl2json = new ExcelToJSON();
xl2json.parseExcel(files[0]);
}

document.getElementById('upload').addEventListener('change', handleFileSelect, false);



/* $(document).ready(function() {
  $('form').on('submit', function(event) {
    event.preventDefault();
    var formData = $(this).serialize();
    $.ajax({
      type: 'POST',
      url: $(this).attr('action'),
      data: formData,
      beforeSend: function(xhr, settings) {
        xhr.setRequestHeader("X-CSRFToken", $('input[name="csrfmiddlewaretoken"]').val());
      },
      success: function(response) {
        // handle response from server
      },
      error: function(xhr, textStatus, errorThrown) {
        console.log("Error:", errorThrown);
      }
    });
  });
}); */