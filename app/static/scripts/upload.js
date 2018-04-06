
function noPreview() {
  $('#image-preview-div').css("display", "none");
  $('#preview-img').attr('src', 'noimage');
  $('#submit').attr('disabled', '');
}

function preview() {
  $('#image-preview-div').css("display", "block");
  $('#preview-img').css('max-height', '250px');
}

function selectImage(e) {
  $('#file').css("color", "green");
  $('#image-preview-div').css("display", "block");
  $('#preview-img').attr('src', e.target.result);
  $('#preview-img').css('max-height', '250px');
}

$(document).ready(function () {
   $(function() {
       var maxsize = 5 * 1024 * 1024; // 5 MB

       $('#max-size').html((maxsize/(1024 * 1024)).toFixed(2));

       var img_src = $('#preview-img').attr('src');
       var ext = img_src.substr(img_src.lastIndexOf('.') + 1);
       if(ext.length > 0)
           preview();

       $('form').on('submit', function(event) {
            event.preventDefault();

            $('#progressBar').attr('aria-valuenow', 0).css('width', '0%').text('0%');
            $('.progress').show();
            $('.alert-danger').hide();
            $('.alert-success').hide();

            var form_data = new FormData($('form')[0]);
            $.ajax({
                xhr: function(){
                    var xhr = new window.XMLHttpRequest();
                    xhr.upload.addEventListener('progress', function(e){
                       if(e.lengthComputable){
                           console.log('Bytes Loaded: ' + e.loaded);
                           console.log('Total size: ' + e.total);
                           console.log('Percentage uploaded: ' + (e.loaded / e.total));

                           var percent = Math.round((e.loaded / e.total) * 100);

                           $('#progressBar').attr('aria-valuenow', percent).css('width', percent + '%').text(percent + '%');
                       }
                    });
                    return xhr;
                },
                type: 'POST',
                url: '/company',
                data: form_data,
                contentType: false,
                processData: false,
                success: function(data) {
                    if(data[1] == 200) {
                        $('.alert-success .text').text(data[0].message);
                        $('.alert-success').show();
                    }else{
                        $('.progress').hide();
                        $('.alert-danger .text').text(data[0].message);
                        $('.alert-danger').show();
                    }
                    console.log(data);
                },error: function(jqXHR, status, err){
                     console.log(status);
                    $('.alert-danger .text').text(err.toLowerCase()+'!');
                    $('.alert-danger').show();
                }
            });
        });


       $('#file').change(function() {

            $('#message').empty();

            var file = this.files[0];
            var match = ["image/jpeg", "image/png", "image/jpg"];

            if ( !( (file.type == match[0]) || (file.type == match[1]) || (file.type == match[2]) ) )
            {
              noPreview();

              $('#message').html('<div class="alert alert-warning" role="alert">Unvalid image format. Allowed formats: JPG, JPEG, PNG.</div>');

              return false;
            }

            if ( file.size > maxsize )
            {
              noPreview();

              $('#message').html('<div class=\"alert alert-danger\" role=\"alert\">The size of image you are attempting to upload is ' + (file.size/1024).toFixed(2) + ' KB, maximum size allowed is ' + (maxsize/1024).toFixed(2) + ' KB</div>');

              return false;
            }

            $('#submit').removeAttr("disabled");

            var reader = new FileReader();
            reader.onload = selectImage;
            reader.readAsDataURL(this.files[0]);

          });
    });
});