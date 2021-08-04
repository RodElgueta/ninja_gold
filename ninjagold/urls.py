from django.urls import path     
from . import views

urlpatterns = [ path('',views.login),
                path('ninja_gold',views.ninja_gold),
                path('process_money',views.procces_money,name="moneymach"),
                path('reset',views.reset),
                path('parameters',views.parameters),
                path('end',views.end)
]