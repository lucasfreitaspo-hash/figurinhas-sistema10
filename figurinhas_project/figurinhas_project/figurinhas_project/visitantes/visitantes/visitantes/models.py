from django.db import models
from django.utils import timezone

class Produto(models.Model):
    nome = models.CharField(max_length=100)
    preco = models.DecimalField(max_digits=8, decimal_places=2)
    descricao = models.TextField(blank=True)
    ativo = models.BooleanField(default=True)
    
    class Meta:
        verbose_name_plural = "Produtos"
    
    def __str__(self):
        return f"{self.nome} - R$ {self.preco}"

class Visitante(models.Model):
    TIPO_CHOICES = [
        ('comprador', 'Comprador'),
        ('vendedor', 'Vendedor'),
        ('outro', 'Outro'),
    ]
    
    nome = models.CharField(max_length=150)
    telefone = models.CharField(max_length=20)
    email = models.EmailField(blank=True, null=True)
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)
    data_cadastro = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "Visitantes"
    
    def __str__(self):
        return f"{self.nome} - {self.tipo}"

class Entrada(models.Model):
    visitante = models.ForeignKey(Visitante, on_delete=models.CASCADE, related_name='entradas')
    data_entrada = models.DateTimeField(auto_now_add=True)
    data_saida = models.DateTimeField(blank=True, null=True)
    observacoes = models.TextField(blank=True)
    
    class Meta:
        verbose_name_plural = "Entradas"
    
    def __str__(self):
        return f"{self.visitante.nome} - {self.data_entrada}"
    
    def tempo_permanencia(self):
        if self.data_saida:
            return (self.data_saida - self.data_entrada).total_seconds() / 60
        return None

class Venda(models.Model):
    visitante = models.ForeignKey(Visitante, on_delete=models.CASCADE, related_name='vendas')
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField(default=1)
    preco_unitario = models.DecimalField(max_digits=8, decimal_places=2)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    data_venda = models.DateTimeField(auto_now_add=True)
    observacoes = models.TextField(blank=True)
    
    class Meta:
        verbose_name_plural = "Vendas"
    
    def __str__(self):
        return f"{self.visitante.nome} - {self.produto.nome} x{self.quantidade}"
    
    def save(self, *args, **kwargs):
        self.total = self.quantidade * self.preco_unitario
        super().save(*args, **kwargs)
