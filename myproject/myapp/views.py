# from typing import Any, Dict
import json
from django.http import HttpResponse,JsonResponse
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib.auth.views import PasswordChangeView,PasswordChangeDoneView
from .forms import MypasswordChangeForm,ProductForm
from django.template.loader import render_to_string
from .models import Product, Profile
from django.views import View   
from .forms import CustomUserCreationForm,MyProfileForm,MyResetPasswordForm,MySetPasswordForm
from .serializers import ProductSerializer
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import permission_classes
from django.core.mail import send_mail
from django.conf import settings
from .models import TokenReset,TokenRegister,Cart
from .serializers import TokenResetSerializer,TokenRegisterSerializer,CartSerializer
from rest_framework.decorators import permission_classes
from rest_framework_simplejwt.views import TokenObtainPairView
from .forms import CustomLoginForm
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated,AllowAny
from django.contrib.auth.decorators import login_required
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
# Create your views here.
# product_list = Product.objects.all()
# ***************************************************** TRANG CHỦ ****************************************************
class Authenticate():
    def authenticate(self,request):
        authentication = JWTAuthentication()
        try:
            user,_ = authentication.authenticate(request)
            return user
        except:
            return None
    def is_login(self,request):
        user = self.authenticate(request)
        if user and user.is_authenticated:
            return 1
        else:
            return None
    def is_manager(self,request):
        user = self.authenticate(request)
        if user and user.is_staff:
            return 1
        else:
            return None
class home(View):
    my_auth = Authenticate()
    def get(self, request):
        is_login = self.my_auth.is_login(request)
        phone_list = Product.objects.filter(category=2).order_by('id')[:3]
        laptop_list = Product.objects.filter(category=1).order_by('id')[:3]
        tablet_list = Product.objects.filter(category=4).order_by('id')[:3]
        phukien_list = Product.objects.filter(category=3).order_by('id')[:3]
        print(is_login)
        return render(request,'myapp/home.html',locals())

# class product_detail(View):
#     my_auth = Authenticate()
#     def get(self,request,val):
#         is_login = self.my_auth.is_login(request)
#         product = Product.objects.filter(id=val).first()
#         serializer_product = ProductSerializer(product)
#         return render(request,'myapp/product_detail.html',{"product":serializer_product.data,"is_login":is_login})
class ProductDetail(APIView):
    permission_classes = [AllowAny]
    def get(self,request,val):
        product = Product.objects.filter(id=val).first()
        serializer_product = ProductSerializer(product)
        return JsonResponse(data=serializer_product.data,safe=False)
# ********************************************** ĐĂNG KÍ *****************************************************
class CustomRegister(View):
    my_auth = Authenticate()
    
    def get(self, request):
        is_login = self.my_auth.is_login(request)
        form = CustomUserCreationForm()
        return render(request,'myapp/customregister.html',locals())
    def post(self, request):
        is_login = self.my_auth.is_login(request)
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            
            token = TokenRegister.objects.create(user=user)
            serializer = TokenRegisterSerializer(token)
            html = render_to_string('myapp/mailregister.html',{'token':serializer.data['token']})
            send_mail(
                subject='',
                html_message=html,
                message=html,
                fail_silently=False,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[user.email],
            )
            return HttpResponse(f'Đăng kí thành công. Chúng tôi đã gửi mail xác nhận cho bạn {user.email}')
        else:
            return HttpResponse(f'đăng kí thất bại {form.error_messages}')
class VerifyRegisterComplete(View):
    my_auth = Authenticate()
    
    def get(self, request,token):
        is_login = self.my_auth.is_login(request)
        token = TokenRegister.objects.filter(token=token).first()
        # print(token)
        if token:
            user_name = token.user
            user = User.objects.filter(username=user_name).first()
            user.is_active = True
            user.save()
            token.delete()
            return HttpResponse(f'Xác nhận thành công {user.username} ')
        else:
            return HttpResponse('đường link sai ')
# ************************************************ ĐĂNG NHẬP *******************************************
class MyLoginView(TokenObtainPairView):
    my_auth = Authenticate()
    
    def get(self, request):
        is_login = self.my_auth.is_login(request)
        if is_login is not None:
            return redirect('home')
        else:
            form = CustomLoginForm
            return render(request,'myapp/login.html',locals())
# ********************************************** PHÂN TRANG SẢN PHẨM (product_detail) ***************************************
class MyPagination(PageNumberPagination):
    page_size = 6
    page_query_param = 'page'

class PaginationViewProduct(APIView):
    pagination_class = MyPagination
    authentication_classes = [SessionAuthentication]
    my_auth = Authenticate()
    def get(self, request,val):
        is_login = self.my_auth.is_login(request)
        if val == "Dien-thoai":
            queryset = Product.objects.filter(category=2).all()
        elif val == "Laptop":
            queryset = Product.objects.filter(category=1).all()
        elif val == "Tablet":
            queryset = Product.objects.filter(category=4).all()
        elif val == "Phu-kien":
            queryset = Product.objects.filter(category=3).all()
        paginator = self.pagination_class()
        paginated_queryset = paginator.paginate_queryset(queryset, request)
        serializer = ProductSerializer(paginated_queryset, many=True)
        # page_list = paginator.get_page_number(), # danh sách các trang 
        if request.GET.get('page'):            
            current_page = int(request.GET.get('page')) # trang hiện tại 
        else:
            current_page = 1
       
        product_count = queryset.count() #Tổng số sản phẩm
        
        total_pages = (product_count//(paginator.page_size))+1 #tổng số trang 
        page_list = [] #danh sách trang 
        for i in range(1, total_pages+1, 1):
            page_list.append(i)
        page_list_sub = [] #danh sách trang hiện ra
        first_three_dots = None
        last_three_dots = None
        # thuật toán phân trang
        if (current_page+2)<total_pages:
            last_three_dots =1
        if (current_page-2)>1:
            first_three_dots = 1
        if total_pages< 5:
            for page in page_list:
                page_list_sub.append(page)
        else:
            if current_page<4:
                for page in page_list:
                    if page<=5:
                        page_list_sub.append(page)
            else:   
                if (current_page+2)>total_pages:
                    for page in page_list:
                        if page>(total_pages-4):
                            page_list_sub.append(page)                      
                else:
                    if (current_page+2)<total_pages:
                        for page in page_list:
                            if page>=(current_page-2)and page<=(current_page+2):
                                page_list_sub.append(page)
        

        context = {
            'product_list': serializer.data,
            'previous_page_url': paginator.get_previous_link(),
            'page_list': page_list_sub, # danh sách các trang 
            'current_page': paginator.page.number, # trang hiện tại 
            'next_page_url': paginator.get_next_link(),
            'total_pages':total_pages, #Tổng số trang
            'category':val,
            'first_three_dots':first_three_dots,
            'last_three_dots':last_three_dots,
            'is_login':is_login
        }
        
        return render(request, 'myapp/product.html', context)
#***************************************************** PROFILES ********************************************************
class ProfileView(View):
    active_profile = 1
    active_adress = None
    my_auth = Authenticate()
    def get(self, request, *args, **kwargs):
        is_login = self.my_auth.is_login(request)
        if is_login is not None:    
            active_profile = 1
            active_adress = None
            form = MyProfileForm()
            if request.user.is_authenticated:
                user = request.user
            return render(request,'myapp/profile.html',locals())
            pass
        else:
            return redirect('login')
    def post(self, request, *args, **kwargs):
        is_login = self.my_auth.is_login(request)
        active_profile = 1
        active_adress = None
        form = MyProfileForm(request.POST)
        if form.is_valid():
            user = request.user
            name = form.cleaned_data['name']
            adress = form.cleaned_data['adress']
            mobile = form.cleaned_data['mobile']
            check = Profile.objects.filter(user=user).first()
            if check:
                check.name = name
                check.adress = adress
                check.mobile = mobile
                check.save()
            else:
                reg = Profile(user=user,name=name,adress=adress,mobile=mobile)
                reg.save()
        return render(request,'myapp/profile.html',locals())
class Adress(View):
    my_auth = Authenticate()
    def get(self, request):
        is_login = self.my_auth.is_login(request)

        if is_login is not None:
            user = self.my_auth.authenticate(request)
            active_adress = 1
            active_profile = None
            
            if user:  
                check = Profile.objects.filter(user=user).first()
                if check:
                    name = check.name
                    adress = check.adress
                    mobile = check.mobile
                    info ={'name':name,'adress':adress,'mobile':mobile}
            else:
                messages_info = 'Chưa nhập thông tin'
                return render(request,'myapp/adress.html',locals())
            return render(request,'myapp/adress.html',locals())
        else:
            return redirect('login')
        
# ***************************************************** Quên mật khẩu *********************************************************
class MyResetPassword(View):
    my_auth = Authenticate()
    def get(self, request, *args, **kwargs):
        is_login = self.my_auth.is_login(request)
        form = MyResetPasswordForm
        return render(request,'myapp/resetpassword.html',locals())
    def post(self, request, *args, **kwargs):
        is_login = self.my_auth.is_login(request)
        if request.method == 'POST':
            email = request.POST.get('email')
            user = User.objects.filter(email=email).first()
            if user:
                TokenReset.objects.create(user = user)
                token = TokenReset.objects.filter(user=user).first()
                serializer = TokenResetSerializer(token)

                html = render_to_string('myapp/sendmailresetpassword.html',{"token":serializer.data['token']})
             
                send_mail(
                    subject="mail reset password",
                    message=html,
                    html_message=html,
                    from_email='sharingan.cmth@outlook.com',
                    recipient_list = [email],
                    fail_silently=False,
                )
                return HttpResponse('check your mail')
            else:
                return HttpResponse('failed')
        else:
            form = MyResetPasswordForm
            return render(request,'myapp/resetpassword.html',locals())
class MyresetPasswordConfirm(View):
    my_auth = Authenticate()
    def get(self, request,token):
        is_login = self.my_auth.is_login(request)
        test_token = TokenReset.objects.filter(token=token).first()
        user = User.objects.filter(username=test_token.user).first()
        if test_token:
            form = MySetPasswordForm(user=user)
            return render(request,'myapp/resetpasswordconfirm.html',locals())
        else:
            return redirect('reset-password')
    def post(self, request,token):
        is_login = self.my_auth.is_login(request)
        test_token = TokenReset.objects.filter(token=token).first()
        if test_token:
            username = test_token.user
            password = request.POST.get('new_password1')
            user = User.objects.filter(username=username).first()
            if user:
                user.password = password
                user.save()
                test_token.delete()
                return HttpResponse('đổi mật khẩu thành công')
        return HttpResponse('Đổi mật khẩu thất bại ')

# *************************************************** ĐỔI MẬT KHẨU *************************************************************
class MyPasswordChangeView(PasswordChangeView):
    template_name = 'myapp/changepassword.html'
    form_class=MypasswordChangeForm
    success_url = 'thanh-cong/'
    my_auth = Authenticate()
    def get_context_data(self, **kwargs):
        is_login = self.my_auth.is_login(self.request)
        context = super().get_context_data(**kwargs)
        context['is_login'] = is_login
        return context
class MyPasswordChangeDoneView(PasswordChangeDoneView):
    template_name = 'myapp/passwordchangedone.html'
    my_auth = Authenticate()
    def get_context_data(self, **kwargs):
        is_login = self.my_auth.is_login(self.request)
        context = super().get_context_data(**kwargs)
        context['is_login'] = is_login
        return context
    
# ********************************************************** CART *******************************************************

def add_cart(request,product_id):
    my_auth = Authenticate()
    is_login = my_auth.is_login(request)
    user = my_auth.authenticate(request)
    if user and user.is_authenticated:
        username = user
        user = User.objects.get(username=username)
        user_id = user.id
        product = Product.objects.get(id=product_id)
        cart = Cart.objects.filter(user=user_id,product=product).first()
        if cart:
            cart.quantity +=1
            cart.save()
        else:   
            Cart.objects.create(user=user,product=product)
        
        return redirect('showcart')
    else:
        return redirect('login')     
class ShowCart(View):
    my_auth = Authenticate()
    def get(self, request):
        is_login = self.my_auth.is_login(request)
        user = self.my_auth.authenticate(request)
        if user and user.is_authenticated:
            cart = Cart.objects.filter(user=user).all()
            serializer = CartSerializer(cart,many=True)
            data = serializer.data
          
            # return JsonResponse(data=data,safe=False) 
            return render(request,'myapp/show-cart.html',locals())
           
        else:
            return redirect('login')        
#  xóa sản phẩm trong giỏ hàng 
class DeleteProductCart(View):
    my_auth = Authenticate()
    def get(self,request,product_id):
        user = self.my_auth.authenticate(request)
        cart = Cart.objects.filter(user=user,product=product_id).first()
        cart.delete()
        return redirect('showcart')

# ******************************************************** THÊM SẢN PHẨM ******************************************
class AddProductView(View):
    form = ProductForm
    my_auth = Authenticate()
    def get(self, request, *args, **kwargs):
        # is_manager = self.my_auth.is_manager(request)
        # if is_manager is not None:            
            return render(request,'myapp/addproduct.html',{"form":self.form})
        # else:
        #     return redirect('home')
    def post(self, request):
        # is_manager = self.my_auth.is_manager(request)
        # if is_manager is not None: 
            if request.method == 'POST':
                form = ProductForm(request.POST)
                if form.is_valid():
                    form.save()
                    return JsonResponse({'message': 'Thêm sản phẩm thành công!'})
                else:
                    errors = form.errors.as_json()
                    return JsonResponse({'errors': errors}, status=400)
            else:
                form = ProductForm()

                return render(request, 'myapp/addproduct.html', {'form': form})
        # else:
        #     return redirect('home')

# ******************************test giỏ hàng ****************************
class CartPlus(View):
    my_auth = Authenticate()
    def get(self, request, *args, **kwargs):
        is_login = self.my_auth.is_login(request)
        
        if is_login is not None:
                user = self.my_auth.authenticate(request)
                cart = Cart.objects.filter(user=user).all()
                serializer = CartSerializer(cart,many=True)
                data = serializer.data
               
                return JsonResponse(data,safe=False)
            
        else:
            is_login = None
            return JsonResponse(data=is_login,safe=False)
# ********************************************** THÊM SỐ LƯỢNG SẢN PHẨM **********************************
class AddQuantityProduct(View):
    my_auth = Authenticate()
    def post(self, request):
        is_login = self.my_auth.is_login(request)
        if is_login is not None:
            data = request.body
            data = json.loads(data)
            data = data['data']
            for item in data:
                for item in data:
                    user = item['user']
                    product_id = item['product']
                    quantity = item['quantity']    
                    cart = Cart.objects.filter(user=user,product=product_id).first()
                    if quantity == 0:
                        cart.delete()
                    else:
                        cart.quantity = quantity
                        cart.save()
            return JsonResponse(data={"message":"done"},safe=False)
        else:
            return redirect('home')
class ProductList(APIView):
    def get(self, request, *args, **kwargs):
        product_list = Product.objects.all()
        serializer = ProductSerializer(product_list,many=True)
        return JsonResponse(data=serializer.data,safe=False)

                
                