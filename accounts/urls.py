from django.urls import path
from accounts import views

urlpatterns = [
    path('login/', views.LoginView.as_view(), name='account_login'),
    path('logout/', views.LogoutView.as_view(), name='account_logout'),
    path('signup/', views.SignupView.as_view(), name='account_signup'),
    path('support/', views.SupportView.as_view(), name='account_support'),
    path('support/content/<str:first_name>/<str:last_name>/<str:first_kana>/<str:last_kana>/<str:post_code>/<str:state>/<str:city>/<str:city_block>/<str:apartments>/<str:email>/<str:phone>/<int:donation>/', views.SupportContentView.as_view(), name='account_support_content'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('profile/edit/', views.ProfileEditView.as_view(), name='profile_edit'),


    # Stripe Pay
    path('checkout/<str:id>/', views.PayWithStripe.as_view(), name='checkout'),
    path('success/', views.PaySuccessView.as_view()),
    path('successful/<str:id>/', views.PaySuccessfulView.as_view()),
    path('cancel/<str:id>/', views.PayCancelView.as_view()),

    path('cart/<str:id>/', views.CartListView.as_view(), name='cart'),  # カートページ
    path('bank/<str:id>/', views.BankView.as_view(), name='bank'),

    #発送、未発送の設定
    path("shipping/<str:id>/",views.Shipping,name="shipping"),

    #未決済の設定
    path("payment/<str:id>/",views.Payment,name="payment"),


]