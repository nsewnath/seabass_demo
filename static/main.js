$(document).ready(function(){
  $(".form").hide();
  $(".form1").hide();

  $(".form-check-input2").click(function(){
    $(".form").show();
    $(".form1").hide();
  })

  $(".form-check-input3").click(function(){
    $(".form1").show();
    $(".form").hide();
  })

  $(".form-check-input1").click(function(){
    $(".form").hide();
    $(".form1").hide();
  })
}); 

