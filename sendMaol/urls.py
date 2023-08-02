from django.urls import path
from . import views
urlpatterns = [
    #fetch wishlist
    path("", views.sendMail.as_view(), name="sendMail"),
    path("/aws_ses", views.aws_ses.as_view(), name="aws_ses"),
    path("/track_image", views.track_image.as_view(), name="track_image"),

]
