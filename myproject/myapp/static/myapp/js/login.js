let usersLogin = document.querySelector("#userLogin");
usersLogin.addEventListener("click",(event)=>{
    event.preventDefault(); 
    console.log(userName)
    userLogin();
})
const userLogin = ()=>{
    let userName = document.querySelector("#userName").value;
    let userPass = document.querySelector("#userPass").value;
    
    let user = {
        username: userName,
        password: userPass,
    }
    axios({
        url: "http://127.0.0.1:8000/myapp/dang-nhap/",
        method: "POST",
        data: user,
    
    }).then((res)=>{
    
        data_login = res.data
        console.log(data_login['access'])
        console.log(data_login['refresh'])
        localStorage.setItem('access',data_login['access'])
        localStorage.setItem('refresh',data_login['refresh'])
    }).catch((err)=>{
        console.log(err)
    });
  
}
