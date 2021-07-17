from django.urls import path

from . import views
app_name = "savethehawkers"
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
    path("<str:name>/info", views.info, name = "info"),
    path("<str:name>/editing", views.edity, name="editing"),
    path("<str:name>/report", views.report, name="report"),
    path("creations", views.creations, name="creations"),
    path("<str:name>/comment", views.comment, name="comment"),
    path("<str:name>/profile", views.userprofile, name="users"),
    path("community", views.community, name="community"),
    path("bookmark/<str:name>", views.bookmark, name="bookmark"),

    path("name", views.name, name="name"),
]
