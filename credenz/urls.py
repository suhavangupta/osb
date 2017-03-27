"""credenz URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^admin_pisb_django/', include(admin.site.urls)),
    url(r'^$', 'osb.views.home'),
    url(r'^login$','osb.views.log_in'),
    url(r'^admin_pisb$', 'osb.views.authenticate_func'),
    url(r'^authenticate$', 'osb.views.admin_func'),
    url(r'^manually_add$', 'osb.views.add_manually_func'),
    url(r'^app_add$', 'osb.views.get_data_app'),
    url(r'^slot_add$', 'osb.views.slot_add'),
    url(r'^email_send$', 'osb.views.email_send'),
    url(r'^slot_store$', 'osb.views.add_slot_func'),
    url(r'^user_store$', 'osb.views.add_data_manually'),
    url(r'^resendmail$', 'osb.views.resend_mail_password'),
    url(r'^confirmationmail$', 'osb.views.resend_confirmation_mail'),
    url(r'^show_slot$', 'osb.views.show_slot'),
    url(r'^show_user$', 'osb.views.show_user'),
    url(r'^confirm_slot$', 'osb.views.confirm_slot_book'),
    url(r'^log_out','osb.views.log_out'),
    url(r'^receipt_info','osb.views.receipt_name'),
    url(r'^call_info','osb.views.call_user'),
    url(r'^modify','osb.views.modify_data'),
]
