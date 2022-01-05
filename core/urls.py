from django.urls import path
from rooms import views as rooms_views

app_name = "core"  # config urls.py의 namespace와 같아야함

urlpatterns = [path("", rooms_views.HomeView.as_view(), name="home")]  # view로 변환
