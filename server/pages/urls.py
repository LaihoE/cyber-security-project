from django.urls import path

from .views import homePageView, insertMessageView

urlpatterns = [
    path('', homePageView, name='home'),
    path('insertMessage/', insertMessageView, name='insertMessageView'),
]
