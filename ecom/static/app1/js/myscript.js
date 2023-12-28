
$(document).ready(function(){
  $('.plus-cart').click(function(){
    var id=$(this).attr("pid").toString();
    var em= this.parentNode.children[2]
    console.log("pid : ",id)
   $.ajax({
    type:"GET",
    url:"/plus_cart",
    data:{
      prod_id:id
    },
    success:function(data){
      console.log("data =",data);
      em.innerText=data.quantity
      document.getElementById("amount").innerText=data.amount
      document.getElementById("totalamount").innerText=data.totalamount
   }
   })
  });
});


$(document).ready(function(){
  $('.minus-cart').click(function(){
    var id=$(this).attr("pid").toString();
    var em= this.parentNode.children[2]
    console.log("pid : ",id)
    $.ajax({
     type:"GET",
     url:"/minus_cart",
     data:{
      prod_id:id
     },
     success:function(data){
      console.log("data =",data);
      em.innerText=data.quantity
      document.getElementById("amount").innerText=data.amount
      document.getElementById("totalamount").innerText=data.totalamount
     }
    })
    });
});

$(document).ready(function(){
  $('.remove-cart').click(function(){
    var id=$(this).attr("pid").toString();
    var em=this
    console.log("pid : ",id)
    $.ajax({
     type:"GET",
     url:"/remove_cart",
     data:{
      prod_id:id
     },
     success:function(data){
      document.getElementById("amount").innerText=data.amount
      document.getElementById("totalamount").innerText=data.totalamount
      em.parentNode.parentNode.parentNode.parentNode.remove()
     }
    })
    });
});

$(document).ready(function(){
  $(document).on('click', '.minus-wishlist', function() {
    var id=$(this).attr("pid").toString();
   console.log("pid : ",id)
   $.ajax({
      type:"GET",
      url:"/minusWishlist",
      data:{
        prod_id:id
      },
      success:function(data){
       window.location.href=`http://127.0.0.1:8000/Product_Details/${id}`
     }
    }) 
 });
});

$(document).ready(function(){
  $(document).on('click', '.plus-wishlist', function() {
   var id=$(this).attr("pid").toString();
   console.log("pid : ",id)
   $.ajax({
      type:"GET",
      url:"/plusWishlist",
      data:{
        prod_id:id
      },
      success:function(data){
       window.location.href=`http://127.0.0.1:8000/Product_Details/${id}`
     }
    })
  });
});