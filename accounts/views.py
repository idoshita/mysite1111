from django.views import View
from django.views.generic import View, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from accounts.models import CustomUser, SupportUser, Item
from accounts.forms import ProfileForm, SignupUserForm, SupportUserForm # 追加
from django.shortcuts import render, redirect
from allauth.account import views # 追加
from django.utils import timezone
from django.utils.timezone import localtime
from django.views.decorators.http import require_POST


#Strip API
import stripe
from django.conf import settings
from stripe.api_resources import tax_rate

stripe.api_key = settings.STRIPE_API_SECRET_KEY



class PaySuccessView(views.LoginView):
    template_name = 'accounts/success.html'


class PaySuccessfulView(TemplateView):
    def get(self, request, *args, **kwargs):
        id = self.kwargs.get("id")
        sp_data = SupportUser.objects.get(id=id)
        sp_data.is_confirmed = True  # 注文確定
        sp_data.save()
        return render(request, 'accounts/successful.html')


class PayCancelView(TemplateView):

    def get(self, request, *args, **kwargs):
        id = self.kwargs.get("id")
        sp_data = SupportUser.objects.get(id=id)
        return render(request, 'accounts/cancel.html', {
            "id":sp_data,})



tax_rate = stripe.TaxRate.create(
    display_name='消費税',
    description='消費税',
    country='JP',
    jurisdiction='JP',
    percentage=settings.TAX_RATE * 0,
    inclusive=True,  # 外税を指定（内税の場合はTrue）
)

def create_line_item(unit_amount, name, quantity):
    return {
        'price_data': {
            'currency': 'JPY',
            'unit_amount': unit_amount,
            'product_data': {'name': name, }
        },
        'quantity': quantity,
        'tax_rates': [tax_rate.id]
    }


class PayWithStripe(View):


    def post(self, request, *args, **kwargs):
        id = self.kwargs.get("id")

        sp_data = SupportUser.objects.get(id=id)

        sp_data.payment = "クレジット支払"
        sp_data.save()


        line_items = []
            
        price = sp_data.donation
        name = "賛助額"
        quantity = 1
        line_item = create_line_item(
            price, name, quantity)
        line_items.append(line_item)

        checkout_session = stripe.checkout.Session.create(
            customer_email=sp_data.email,
            payment_method_types=['card'],
            line_items=line_items,
            mode='payment',
#            success_url=f'{settings.MY_URL}accounts/success/sp_data.email/',
            success_url=f'{settings.MY_URL}accounts/successful/{id}/',
            cancel_url=f'{settings.MY_URL}accounts/cancel/{id}/',
        )
        return redirect(checkout_session.url)


#自作
class LoginView(views.LoginView):
    template_name = 'accounts/login.html'

class LogoutView(views.LogoutView):
    template_name = 'accounts/logout.html'

    def post(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            self.logout()
        return redirect('/')
    
class SignupView(views.SignupView):
    template_name = 'accounts/signup.html'
    form_class = SignupUserForm


class SupportView(views.FormView):
    def get(self, request, *args, **kwargs):
        form = SupportUserForm(request.POST or None)
        return render(request, 'accounts/support.html', {
            'form': form,
        })

    def post(self, request, *args, **kwargs):
        form = SupportUserForm(request.POST or None)
        if form.is_valid():
            member = SupportUser()
            member.first_name = form.cleaned_data['first_name']
            member.last_name = form.cleaned_data['last_name']
            member.first_kana = form.cleaned_data['first_kana']
            member.last_kana = form.cleaned_data['last_kana']
            member.post_code = form.cleaned_data['post_code']
            member.state = form.cleaned_data['state']
            member.city = form.cleaned_data['city']
            member.city_block = form.cleaned_data['city_block']
            member.apartments = form.cleaned_data['apartments']
            if member.apartments == "":
                member.apartments = "入力無し"
            member.email = form.cleaned_data['email']
            member.phone = form.cleaned_data['phone']
            if member.phone == "":
                member.phone = "入力無し"
            member.donation = form.cleaned_data['donation']
            return redirect('account_support_content', member.first_name, 
                            member.last_name, 
                            member.first_kana,
                            member.last_kana,
                            member.post_code,
                            member.state,
                            member.city,
                            member.city_block,
                            member.apartments,
                            member.email,
                            member.phone,
                            member.donation
                            )


class SupportContentView(View):
    def get(self, request, *args, **kwargs):
        first_name = self.kwargs.get("first_name")
        last_name = self.kwargs.get("last_name")
        first_kana = self.kwargs.get("first_kana")
        last_kana = self.kwargs.get("last_kana")
        post_code = self.kwargs.get("post_code")
        state = self.kwargs.get("state")
        city = self.kwargs.get("city")
        city_block = self.kwargs.get("city_block")
        apartments = self.kwargs.get("apartments")
        email = self.kwargs.get("email")
        phone = self.kwargs.get("phone")
        donation = self.kwargs.get("donation")
        return render(request, 'accounts/support_content.html', {
            "last_name":last_name,
            "first_name":first_name,
            "first_kana":first_kana,
            "last_kana":last_kana,
            "post_code":post_code,
            "state":state,
            "city":city,
            "city_block":city_block,
            "apartments":apartments,
            "email":email,
            "phone":phone,
            "donation":donation,
        })

    def post(self, request, *args, **kwargs):

        first_name = self.kwargs.get("first_name")
        last_name = self.kwargs.get("last_name")
        first_kana = self.kwargs.get("first_kana")
        last_kana = self.kwargs.get("last_kana")
        post_code = self.kwargs.get("post_code")
        state = self.kwargs.get("state")
        city = self.kwargs.get("city")
        city_block = self.kwargs.get("city_block")
        apartments = self.kwargs.get("apartments")
        email = self.kwargs.get("email")
        phone = self.kwargs.get("phone")
        donation = self.kwargs.get("donation")

        if phone == "入力無し":
            phone = "00000000000"

        created = localtime(timezone.now())

        member = SupportUser()
        member.first_name = first_name
        member.last_name = last_name
        member.first_kana = first_kana
        member.last_kana = last_kana
        member.post_code = post_code
        member.state = state
        member.city = city
        member.city_block = city_block
        member.apartments = apartments
        member.email = email
        member.phone = phone
        member.donation = donation
        member.created = created
        member.save()
        id = member.id
        return redirect('cart', id)



class CartListView(View):
    def get(self, request, *args, **kwargs):
        id = self.kwargs.get("id")
        sp_data = SupportUser.objects.get(id=id)

        return render(request, 'accounts/cart.html', {
            "id":sp_data,
        })

    def post(self, request, *args, **kwargs):
        id = self.kwargs.get("id")
        sp_data = SupportUser.objects.get(id=id)

        return render(request, 'accounts/cart.html', {
            "id":sp_data,
        })




class BankView(View):
    def get(self, request, *args, **kwargs):
        id = self.kwargs.get("id")
        sp_data = SupportUser.objects.get(id=id)

        sp_data.payment = "銀行支払"

        sp_data.save()


        return render(request, 'accounts/bank.html', {
            "id":sp_data,
        })

    def post(self, request, *args, **kwargs):
        id = self.kwargs.get("id")
        sp_data = SupportUser.objects.get(id=id)

        sp_data.payment = "銀行支払"
        sp_data.save()

        return render(request, 'accounts/bank.html', {
            "id":sp_data,
        })



#class ProfileView(LoginRequiredMixin, View):
class ProfileView(View):
    def get(self, request, *args, **kwargs):
        user_data = SupportUser.objects.all()

        return render(request, 'accounts/profile.html', {
            'user_data': user_data,
        })

class ProfileEditView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        user_data = CustomUser.objects.get(id=request.user.id)
        form = ProfileForm(
            request.POST or None,
            initial={
                'first_name': user_data.first_name,
                'last_name': user_data.last_name,
                'department': user_data.department
            }
        )

        return render(request, 'accounts/profile_edit.html', {
            'form': form
        })

    def post(self, request, *args, **kwargs):
        form = ProfileForm(request.POST or None)
        if form.is_valid():
            user_data = CustomUser.objects.get(id=request.user.id)
            user_data.first_name = form.cleaned_data['first_name']
            user_data.last_name = form.cleaned_data['last_name']
            user_data.department = form.cleaned_data['department']
            user_data.save()
            return redirect('profile')

        return render(request, 'accounts/profile.html', {
            'form': form
        })
    

@require_POST#ボタンが押された時のみ動作する。
def Shipping(request,id):
    sp_data = SupportUser.objects.get(id=id)
    shipping = localtime(timezone.now())
    sp_data.shipping = shipping  # 注文確定
    sp_data.save()
    return redirect('profile')

@require_POST#ボタンが押された時のみ動作する。
def Payment(request,id):
    sp_data = SupportUser.objects.get(id=id)
    sp_data.is_confirmed = True  # 支払済
    sp_data.save()
    return redirect('profile')
