$("form[name=signUp_form]").submit(function(e){
    
    var $form=$(this);
    var $error=$form.find(".error");
    var data=$form.serialize();
    $.ajax({
        url:"/signUp",
        type:"POST",
        data:data,
        dataType:"json",
        success:function(resp){
            window.location.href="/home"
        },
        error: function(resp){
            $error.text(resp.responseJSON.error).removeClass("error--hidden");
        }
    })
    e.preventDefault();
});