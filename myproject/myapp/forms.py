from django import forms
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm,UsernameField,SetPasswordForm,PasswordChangeForm,PasswordResetForm
from django.contrib.auth.models import User
from .models import Profile,Product
# from .models import Profile
class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'autofocus':"True",'class':'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Nhập lại mật khẩu',widget=forms.PasswordInput(attrs={'class':'form-control'}))
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Tên đăng nhập' 
        self.fields['password1'].label ='Mật khẩu'
        
    class Meta:
        model = User
        fields = ['username','email','password1','password2']
class CustomLoginForm(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(attrs={'autofocus':'True','class':'form-control','id':'userName'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'autocomplete':'current-password','class':'form-control','id':'userPass'}))
    
class MyResetPasswordForm(PasswordResetForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control'}))
class MySetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(label='Mật khẩu mới:',widget=forms.PasswordInput(attrs={'autocomplete':'current-password','class':'form-control'}))
    new_password2 = forms.CharField(label='Nhập lại:',widget=forms.PasswordInput(attrs={'autocomplete':'current-password','class':'form-control'}))
class MyProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['id','user','name','adress','mobile']
        widgets = {
            'name':forms.TextInput(attrs={'class':'form-control'}),
            'adress':forms.TextInput(attrs={'class':'form-control'}),
            'mobile':forms.TextInput(attrs={'class':'form-control'}),
        }
class MypasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(label='Mật khẩu cũ',widget=forms.PasswordInput(attrs={'autofocus':'True','autocomplete':'currrent-password','class':'form-control'}))
    new_password1 = forms.CharField(label='Nhập mật khẩu mới',widget=forms.PasswordInput(attrs={'autocomplete':'currrent-password','class':'form-control'}))
    new_password2 = forms.CharField(label='Nhập lại mật khẩu mới',widget=forms.PasswordInput(attrs={'autocomplete':'currrent-password','class':'form-control'}))
    
class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['title', 'selling_price', 'discounted_price', 'description', 'category', 'product_image']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'selling_price': forms.NumberInput(attrs={'class': 'form-control'}),
            'discounted_price': forms.NumberInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'product_image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'title': 'Tên sản phẩm',
            'selling_price': 'Giá gốc',
            'discounted_price': 'Giá đã giảm',
            'description': 'Mô tả sản phẩm',
            'category': 'Loại sản phẩm',
            'product_image': 'Ảnh sản phẩm',
        }