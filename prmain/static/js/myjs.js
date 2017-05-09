
var sourse = $('#entry-template').html()
var template = Handlebars.compile(sourse);

$('#analytics').html("<div class='text-center'><img alt='loading' src='../static/ajax-loader.gif'/></div>");
$('#myModal').on('show.bs.modal', function (e) {
      
      $('#analytics').html("<div class='text-center'><img alt='loading' src='../static/ajax-loader.gif'/></div>");
      $.getJSON(Flask.url_for("analytics")).done(function(data, textStatus, jqXHR) {

                  $('#analytics').html(template(data));
               
        })
        .fail(function(jqXHR, textStatus, errorThrown) {
    
            // log error to browser's console
            console.log(errorThrown.toString());
            $('#analytics').html("<div class='text-center'><p>Can't load data</p></div>");
    
        });;
      //return false;
  
})
