from django.urls import path
from . import views



urlpatterns = [
    path('', views.rank_top, name='rank_top'),
    path('rank/<shop>/<int:pk>', views.rank_shop, name='rank_shop'),
    path('about', views.about, name='about'),
    
    # path('rank/kaden/<int:pk>', views.rank_kaden, name='rank_kaden'),
    # path('rank/pet/<int:pk>', views.rank_pet, name='rank'),
]