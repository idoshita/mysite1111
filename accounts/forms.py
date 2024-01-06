from django import forms
from allauth.account.forms import SignupForm # 追加

class SignupUserForm(SignupForm):
    first_name = forms.CharField(max_length=30, label='姓')
    last_name = forms.CharField(max_length=30, label='名')

    def save(self, request):
        user = super(SignupUserForm, self).save(request)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()
        return user
    
class SupportUserForm(forms.Form):
    first_name = forms.CharField(max_length=30, label='姓')
    last_name = forms.CharField(max_length=30, label='名')
    first_kana = forms.CharField(max_length=30, label='姓カナ')
    last_kana = forms.CharField(max_length=30, label='名カナ')
    post_code = forms.RegexField(label='郵便番号(ハイフンなし)',
        regex=r'^[0-9]+$',
        max_length=7,
        widget=forms.TextInput(attrs={'onKeyUp' : "AjaxZip3.zip2addr(this,'','state','city')"}),
    )
    state = forms.CharField(label='都道府県',max_length=6)
    city = forms.CharField(label='市区町村',max_length=10)
    city_block = forms.CharField(max_length=30, label='丁目、番号')
    apartments = forms.CharField(max_length=30, label='マンション名、部屋番号', required=False)
    email = forms.EmailField(max_length=30, label='メールアドレス')
    phone = forms.RegexField(
        regex=r'^[0-9]+$',
        max_length=11, label='電話番号',
        required=False)
    donation = forms.RegexField(
        regex=r'^[0-9]+$',
        max_length=10, label='賛助額/100000')



class ProfileForm(forms.Form):
    first_name = forms.CharField(max_length=30, label='姓')
    last_name = forms.CharField(max_length=30, label='名')
    department = forms.CharField(max_length=30, label='所属', required=False)