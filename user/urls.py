from django.urls import path

from . import views
urlpatterns = [
    path("",views.user_login_page,name="user_login_page"),
    path("ajax/login/",views.login,name="login"),
    path("ajax/register/",views.register,name="register"),
    path("ajax/checkNewClient/",views.check_user,name="checkClient"),
    path("ajax/contracts/",views.contracts,name="contracts"),
    path("ajax/send_reset_request/",views.set_reset_pswd,name="pswd_reset_request"),
    path("reset_pswd/ajax/check_resend_password/",views.check_resend_password,name="check_reset_pswd"),
    path("reset_pswd/ajax/confirm_reset_pswd/",views.confirm_reset_pswd,name="confirm_reset_pswd"),
    path("reset_pswd/<slug:slug>",views.reset_pswd_page,name="reset_pswd"),
]