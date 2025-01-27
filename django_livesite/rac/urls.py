from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("404/", views.error_404, name="404"),
    path("test/", views.test, name="test"),
    path("home/", views.home, name="home"),
    path("karaoke/", views.karaoke, name="karaoke"),
    path("karaoke-start/", views.karaoke_started, name="karaoke-started"),
    path("rec/", views.rec, name="rec"),
    path("rec-res/", views.rec_res, name="rec-res"),
    path("rec-res-explain/", views.rec_res_explain, name="rec_res_explain"),
    path("table-res/", views.table_res, name="table-res"),
    path("graph.js", views.graph_js, name="rec-res"),
]
