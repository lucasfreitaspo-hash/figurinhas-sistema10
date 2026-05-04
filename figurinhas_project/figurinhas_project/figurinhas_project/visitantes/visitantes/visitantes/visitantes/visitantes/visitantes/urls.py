from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('registrar-entrada/', views.registrar_entrada, name='registrar_entrada'),
    path('registrar-venda/<int:entrada_id>/', views.registrar_venda, name='registrar_venda'),
    path('confirmar-venda/<int:venda_id>/', views.confirmar_venda, name='confirmar_venda'),
    path('api/calcular-preco/', views.calcular_preco, name='calcular_preco'),
    path('contatos/', views.contatos, name='contatos'),
    path('relatorio/', views.relatorio, name='relatorio'),
    path('registrar-saida/<int:entrada_id>/', views.registrar_saida, name='registrar_saida'),
]
