from django.urls import path
from . import views
urlpatterns = [
    #fetch wishlist
    path("/sendSesMail", views.sendSesMail.as_view(), name="sendSesMail"),
    path("/aws_ses", views.aws_ses.as_view(), name="aws_ses"),
    path("/track_image", views.track_image.as_view(), name="track_image"),
    path("/aws_sns", views.aws_sns.as_view(), name="aws_sns"),
    path('/ses/handle_delivery_notification', views.handle_delivery_notification.as_view(), name='handle_delivery_notification'),



]
