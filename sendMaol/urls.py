from django.urls import path
from . import views
urlpatterns = [
    #fetch wishlist
    path("/sendSesMail", views.sendSesMail.as_view(), name="sendSesMail"),
    path("/sendBulkMail", views.sendBulkMail.as_view(), name="sendBulkMail"),
    # path("/updateStatus", views.updateStatus.as_view(), name="updateStatus"),
    path("/SNSEndpoint", views.SNSEndpoint.as_view(), name="SNSEndpoint"),



 


]
