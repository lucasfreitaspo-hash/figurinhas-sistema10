from django.contrib import admin
from .models import Produto, Visitante, Entrada, Venda

@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'preco', 'ativo')
    search_fields = ('nome',)

@admin.register(Visitante)
class VisitanteAdmin(admin.ModelAdmin):
    list_display = ('nome', 'telefone', 'tipo', 'data_cadastro')
    search_fields = ('nome', 'telefone')
    list_filter = ('tipo', 'data_cadastro')

@admin.register(Entrada)
class EntradaAdmin(admin.ModelAdmin):
    list_display = ('visitante', 'data_entrada', 'data_saida')
    search_fields = ('visitante__nome',)
    list_filter = ('data_entrada',)

@admin.register(Venda)
class VendaAdmin(admin.ModelAdmin):
    list_display = ('visitante', 'produto', 'quantidade', 'total', 'data_venda')
    search_fields = ('visitante__nome',)
    list_filter = ('data_venda', 'produto')
