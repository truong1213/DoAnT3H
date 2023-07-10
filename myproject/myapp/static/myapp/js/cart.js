class product{
    constructor(name,price,imgUrl,){
        this.name = name;
        this.price = price;
        this.imgUrl = imgUrl;
    }
}
let productList = [];

const fetchProduct = () =>{
    axios({
        url: "http://127.0.0.1:8000/myapp/cartplus/",
        method: "GET",

    }).then((res)=>{
        console.log(res.data)
        productList = res.data
        renderProduct()
    }).catch((err)=>{
        console.log(err)
    });
}
const updateProduct = () =>{
    console.log('test')
    console.log(productList)
    data = {
        'data':productList
    }
    axios({
        url: "http://127.0.0.1:8000/myapp/AddQuantityProduct/",
        method: "POST",
        data: data,

    }).then((res)=>{
        
        console.log(res)
        console.log('test')
    }).catch((err)=>{
        console.log(err)
    });
}

const renderProduct = () =>{
    let htmlContent = "";
    for (let products of productList){
        if (products.quantity !== 0){
            htmlContent += ` <div class="cart_item">
            <div class="img">
              <img src="${products.product_img}" alt="">
            </div>
            <div class="cart_text">
              <div class="cart_text_left">
                <h3 class="cart_name">${products.product_title}</h3>
                <h4 class="cart_price">${products.product_price}₫</h4>
              </div>
              <div class="cart_text_right">
                <span  class="increase" onclick="increaseProduct(${products.id})">+</span> 
                <span class=" cart_number">${products.quantity}</span>
                <span class="decrease" onclick="decreaseProduct(${products.id})">-</span>
              </div>
              
            </div>
            <i class="fa fa-times del_item" onclick="removeProduct(${products.id})"></i>
          </div>`
        }
      
    }
    document.querySelector(".cart_content").innerHTML = htmlContent;
}
const increaseProduct = (id)=>{
    console.log(productList)
    for (let i = 0; i < productList.length; i++){
        if(productList[i].id === id){
            productList[i].quantity += 1;
            console.log(productList[i].quantity);
        }
    }
    renderProduct()

}
const decreaseProduct = (id)=>{
  
    for (let i = 0; i < productList.length; i++){
        console.log(productList[i].quantity);
        if(productList[i].id === id){
            productList[i].quantity -= 1;
            console.log(productList[i].quantity);
        }
    }
    renderProduct()


}
const removeProduct = (id)=>{
   
    for (let i = 0; i < productList.length; i++){
        console.log(productList[i].quantity);
        if(productList[i].id === id && productList[i].quantity > 0){
            productList[i].quantity = 0;
            console.log(productList[i].quantity);
        }
    }
    renderProduct()

}

btnCart.addEventListener('click',()=>{
    if (!cart.classList.contains('active')){
        updateProduct();
    }
    else{
        fetchProduct()
    }
})
