let btnCart = document.querySelector('#btn-cart');
let cart = document.querySelector('#cart');
let btnToggle = document.querySelector('.navbar-toggler')
window.addEventListener("load",function(){
    abc()
    bcd()
});
window.onscroll = ()=>{
    cart.classList.remove("active");
}

function abc(){
    let cardTitle = document.getElementsByClassName('cart_name');
    for(let i = 0; i < cardTitle.length; i ++ ){
        let text = cardTitle[i].innerHTML;
        let newtext = cutString(text,28);
        cardTitle[i].innerHTML = newtext;
    }
}
function bcd(){
    let cardTitle = document.getElementsByClassName('title-product');
    for(let i = 0; i < cardTitle.length; i ++ ){
        let text = cardTitle[i].innerHTML;
        let newtext = cutString(text,75);
        cardTitle[i].innerHTML = newtext;
    }
}
function cutString(str, num){
    if (str.length > num){
        return str.slice(0, num) + "...";
    }
    else{
        return str
    }
}
btnCart.addEventListener('click',()=>{
    cart.classList.toggle("active");
})
btnToggle.addEventListener('click',()=>{
    cart.classList.remove("active");
});
$('#slider1, #slider2, #slider3').owlCarousel({
    loop: true,
    margin: 20,
    responsiveClass: true,
    responsive: {
        0: {
            items: 2,
            nav: false,
            autoplay: true,
        },
        600: {
            items: 4,
            nav: true,
            autoplay: true,
        },
        1000: {
            items: 6,
            nav: true,
            loop: true,
            autoplay: true,
        }
    }
})

$('.plus-cart').click(function(){
    var id=$(this).attr("pid").toString();
    var eml=this.parentNode.children[2] 
    $.ajax({
        type:"GET",
        url:"/pluscart",
        data:{
            prod_id:id
        },
        success:function(data){
            eml.innerText=data.quantity 
            document.getElementById("amount").innerText=data.amount 
            document.getElementById("totalamount").innerText=data.totalamount
        }
    })
})

$('.minus-cart').click(function(){
    var id=$(this).attr("pid").toString();
    var eml=this.parentNode.children[2] 
    $.ajax({
        type:"GET",
        url:"/minuscart",
        data:{
            prod_id:id
        },
        success:function(data){
            eml.innerText=data.quantity 
            document.getElementById("amount").innerText=data.amount 
            document.getElementById("totalamount").innerText=data.totalamount
        }
    })
})


$('.remove-cart').click(function(){
    var id=$(this).attr("pid").toString();
    var eml=this
    $.ajax({
        type:"GET",
        url:"/removecart",
        data:{
            prod_id:id
        },
        success:function(data){
            document.getElementById("amount").innerText=data.amount 
            document.getElementById("totalamount").innerText=data.totalamount
            eml.parentNode.parentNode.parentNode.parentNode.remove() 
        }
    })
})


$('.plus-wishlist').click(function(){
    var id=$(this).attr("pid").toString();
    $.ajax({
        type:"GET",
        url:"/pluswishlist",
        data:{
            prod_id:id
        },
        success:function(data){
            //alert(data.message)
            window.location.href = `http://localhost:8000/product-detail/${id}`
        }
    })
})


$('.minus-wishlist').click(function(){
    var id=$(this).attr("pid").toString();
    $.ajax({
        type:"GET",
        url:"/minuswishlist",
        data:{
            prod_id:id
        },
        success:function(data){
            window.location.href = `http://localhost:8000/product-detail/${id}`
        }
    })
})

