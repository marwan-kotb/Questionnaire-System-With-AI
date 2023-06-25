$(document).on('click', '.table tbody tr td .btn-success', function() {
    var html = '';
    html += "<tr><td class='no'> </td>"
    html += "<td class='code'></td>"
    html += "<td class='name'></td>"
    html += "<td class='doc' ></td>"
    html += "<td><input type='button' class='btn btn-success' value='Add'></input> <input class='btn btn-danger' type='button' value='Remove'></input> <input class='btn edit' type='button' value='Edit'></input><input type='submit' class='btn save' value='Save'> </input> </td>"
    html += "</tr>"

    $(this).parent().parent().after(html)
})

$(document).on('click', '.table tbody tr td .btn-danger', function() {
    $(this).parent().parent().remove()
});


//edit Semester No
$(document).on('click', '.table tbody tr td .edit', function() {  
    $(this).parent().siblings('td.no').each(function() {  
      var content = $(this).html();  
      $(this).html('<input value="' + content + '" />');  
    });  
    $(this).siblings('.save').show();  
     
   
  });  

  //edit course code
$(document).on('click', '.table tbody tr td .edit', function() {  
    $(this).parent().siblings('td.code').each(function() {  
      var content = $(this).html();  
      $(this).html('<input value="' + content + '" />');  
    });  
    $(this).siblings('.save').show();  
     
   
  }); 

//edit course name
$(document).on('click', '.table tbody tr td .edit', function() {  
    $(this).parent().siblings('td.name').each(function() {  
      var content = $(this).html();  
      $(this).html('<input value="' + content + '" />');  
    });  
    $(this).siblings('.save').show();  
     
   
  }); 


  //edit course doc
$(document).on('click', '.table tbody tr td .edit', function() {  
    $(this).parent().siblings('td.doc').each(function() {  
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
                rows.eq(i).find('td.code').text(columns[1]);
                rows.eq(i).find('td.name').text(columns[2]);
                rows.eq(i).find('td.doc').text(columns[3]);
               
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