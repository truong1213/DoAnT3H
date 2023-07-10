from django.urls import path
from . import views
from django.contrib.auth import views as auth_view
from . forms import CustomLoginForm,MyResetPasswordForm,MySetPasswordForm
from rest_framework_simplejwt.views import TokenRefreshView
urlpatterns = [
    path('',views.home.as_view(),name ="home"), # Trang chủ
    path('san-pham/<str:val>',views.ProductDetail.as_view(),name="product_detail"), # Một sản phẩm
    path('danh-sach-san-pham/<str:val>/',views.PaginationViewProduct.as_view(),name='pagination_product'), #Danh sách sản phẩm theo loại
    path('profile/',views.ProfileView.as_view(),name = 'profile'),
    path('adress/',views.Adress.as_view(),name = 'adress'),
    

# ******************************************************************************************************
    path('dang-ki/',views.CustomRegister.as_view(),name='CustomRegisterView'), # Đăng kí
    path('dang-ki/<token>',views.VerifyRegisterComplete.as_view(),name='VerifyRegisterComplete'),
# *****************************************************************************************************
    path('dang-nhap/',views.MyLoginView.as_view(),name='login'), # Đăng nhập
    path('refresh-token/',TokenRefreshView.as_view(),name='refreshtoken'),
  
# ******************************************************** doi mat khau ****************************************************  
    path('doi-mat-khau/',views.MyPasswordChangeView.as_view(),name='changepassword'),
    path('doi-mat-khau/thanh-cong/',views.PasswordChangeDoneView.as_view(),name='passwordchangedone'),
    
# ****************************************************** quen mat khau ********************************************************* 
   path('reset-password/',views.MyResetPassword.as_view(),name='reset-password'),
   path('reset-password-confirm/<token>',views.MyresetPasswordConfirm.as_view(),name='myresetpasswordconfirm'),
#    ********************************************************* Giỏ hàng ***************************************************
    path('add-to-cart/<product_id>',views.add_cart,name='addcart'),
    path('show-cart/',views.ShowCart.as_view(),name = 'showcart'),
    path('delete-cart/<product_id>',views.DeleteProductCart.as_view(),name='DeleteProductCart'),
    path('cartplus/',views.CartPlus.as_view()),
# *********************************************** Thêm sản phẩm ***************************************************
    path('addproduct/',views.AddProductView.as_view(),name='addproduct'),
    # thêm số lượng sản phẩm
    path('AddQuantityProduct/',views.AddQuantityProduct.as_view(),name='AddQuantityProduct'),



    path('ProductList/',views.ProductList.as_view(),name="ProductList"),
]
