$(document).ready(function(){
    $(".form").hide();
    $(".form1").hide();

    $(".form-check2").click(function(){
      $(".form").show();
      $(".form1").hide();
    })

    $(".form-check3").click(function(){
      $(".form1").show();
      $(".form").hide();
    })

    $(".form-check1").click(function(){
      $(".form").hide();
      $(".form1").hide();
    })
}); 