from django.conf.urls import url
from . import views

urlpatterns = [
    url('^image_codes/(?P<uuid>[\w-]+)/$',views.ImageCodeView.as_view()),
]