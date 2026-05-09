from django.urls import path
from . import views
from django.views.generic import TemplateView


app_name = "content"

urlpatterns = [
    # home
    path("", views.HomeView.as_view(), name="home"),
    # portfolio
    path('video/', views.VideoFilterListView.as_view(), name="video_list"),
    path('photo/', views.PhotoListView.as_view(), name="photo_list"),
    path('events/', views.EventFilterListView.as_view(), name="events_list"),
    path("events/<int:pk>/", views.EventDetailView.as_view(), name="event_detail"),
    # pages
    path("price/", views.PriceView.as_view(), name="price"),
    path("line_up/", views.LineUpListView.as_view(), name="line_up"),
    # contacts
    path("contacts/", views.Contacts.as_view(), name="contacts"),
    # documents
    path("policy/", views.TemplateView.as_view(
        template_name="content/documents/document_personal_data.html"
    ), name="policy"),
    path("cookie/", views.TemplateView.as_view(
            template_name="content/documents/document_cookie.html"
        ), name="cookie"),
    path("user_agree/", views.TemplateView.as_view(
                template_name="content/documents/document_user_agree.html"
            ), name="user_agree"),
    path("legal-information/", views.TemplateView.as_view(
                    template_name="content/documents/document_legal_information.html"
                ), name="legal-information")


]
