from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("search", views.search, name = "search"),
    path("<int:pagenumber>/next", views.next, name = "next"),
    path("<int:pagenumber>/nextin", views.nextindex, name = "nextindex"),
    path("<int:pagenumber>/nextstall", views.nextstall, name = "nextstall"),
    path("stalltype", views.stalltype, name = "stalltype"),
    path("<str:name>", views.info, name = "info")
]
