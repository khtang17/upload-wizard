var FormControls= {
    init:function() {
        $("#m_form_company").validate( {
            rules: {
                name: {
                    required: !0
                }
                , description: {
                    required: !0
                }
                , address: {
                    required: !0
                }
                , telephone_number: {
                    required: !0, phoneUS: !0
                }
            }
            , invalidHandler:function(e, r) {
                var i=$("#m_form_company_msg");
                i.removeClass("m--hide").show(), mApp.scrollTo(i, -200)
            }
            , submitHandler:function(e) {
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
                            window.location.reload();
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
            }
        }
        ),
        $("#m_form_2").validate( {
            rules: {
                email: {
                    required: !0, email: !0
                }
                , url: {
                    required: !0
                }
                , digits: {
                    required: !0, digits: !0
                }
                , creditcard: {
                    required: !0, creditcard: !0
                }
                , phone: {
                    required: !0, phoneUS: !0
                }
                , option: {
                    required: !0
                }
                , options: {
                    required: !0, minlength: 2, maxlength: 4
                }
                , memo: {
                    required: !0, minlength: 10, maxlength: 100
                }
                , checkbox: {
                    required: !0
                }
                , checkboxes: {
                    required: !0, minlength: 1, maxlength: 2
                }
                , radio: {
                    required: !0
                }
            }
            , invalidHandler:function(e, r) {
                mApp.scrollTo("#m_form_2"), swal( {
                    title: "", text: "There are some errors in your submission. Please correct them.", type: "error", confirmButtonClass: "btn btn-secondary m-btn m-btn--wide"
                }
                )
            }
            , submitHandler:function(e) {}
        }
        ),
        $("#m_form_3").validate( {
            rules: {
                billing_card_name: {
                    required: !0
                }
                , billing_card_number: {
                    required: !0, creditcard: !0
                }
                , billing_card_exp_month: {
                    required: !0
                }
                , billing_card_exp_year: {
                    required: !0
                }
                , billing_card_cvv: {
                    required: !0, minlength: 2, maxlength: 3
                }
                , billing_address_1: {
                    required: !0
                }
                , billing_address_2: {}
                , billing_city: {
                    required: !0
                }
                , billing_state: {
                    required: !0
                }
                , billing_zip: {
                    required: !0, number: !0
                }
                , billing_delivery: {
                    required: !0
                }
            }
            , invalidHandler:function(e, r) {
                mApp.scrollTo("#m_form_3"), swal( {
                    title: "", text: "There are some errors in your submission. Please correct them.", type: "error", confirmButtonClass: "btn btn-secondary m-btn m-btn--wide"
                }
                )
            }
            , submitHandler:function(e) {
                return swal( {
                    title: "", text: "Form validation passed. All good!", type: "success", confirmButtonClass: "btn btn-secondary m-btn m-btn--wide"
                }
                ), !1
            }
        }
        )
    }
}

;
jQuery(document).ready(function() {
    FormControls.init()
}

);