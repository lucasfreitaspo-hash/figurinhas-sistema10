from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.http import JsonResponse
from django.db.models import Sum, Count, Q
from .models import Visitante, Entrada, Venda, Produto
from datetime import datetime, timedelta

def index(request):
    hoje = timezone.now().date()
    
    total_visitantes = Visitante.objects.count()
    entradas_hoje = Entrada.objects.filter(
        data_entrada__date=hoje
    ).count()
    compradores = Visitante.objects.filter(tipo='comprador').count()
    vendedores = Visitante.objects.filter(tipo='vendedor').count()
    
    vendas_hoje = Venda.objects.filter(data_venda__date=hoje)
    total_vendas_hoje = vendas_hoje.aggregate(Sum('total'))['total__sum'] or 0
    quantidade_vendas_hoje = vendas_hoje.count()
    
    produtos_vendidos = Produto.objects.filter(
        venda__data_venda__date=hoje
    ).annotate(total_qty=Sum('venda__quantidade')).order_by('-total_qty')[:5]
    
    return render(request, 'index.html', {
        'total_visitantes': total_visitantes,
        'entradas_hoje': entradas_hoje,
        'compradores': compradores,
        'vendedores': vendedores,
        'total_vendas_hoje': f"{total_vendas_hoje:.2f}",
        'quantidade_vendas_hoje': quantidade_vendas_hoje,
        'produtos_vendidos': produtos_vendidos,
    })

def registrar_entrada(request):
    if request.method == 'POST':
        nome = request.POST.get('nome', '').strip()
        telefone = request.POST.get('telefone', '').strip()
        email = request.POST.get('email', '').strip()
        tipo = request.POST.get('tipo', 'outro')
        
        if not nome or not telefone:
            return render(request, 'registrar_entrada.html', 
                        {'erro': 'Nome e telefone são obrigatórios'})
        
        visitante, created = Visitante.objects.get_or_create(
            telefone=telefone,
            defaults={'nome': nome, 'email': email, 'tipo': tipo}
        )
        
        if not created:
            visitante.nome = nome
            visitante.tipo = tipo
            if email:
                visitante.email = email
            visitante.save()
        
        entrada = Entrada.objects.create(visitante=visitante)
        
        return redirect('registrar_venda', entrada_id=entrada.id)
    
    return render(request, 'registrar_entrada.html')

def registrar_venda(request, entrada_id):
    entrada = get_object_or_404(Entrada, id=entrada_id)
    produtos = Produto.objects.filter(ativo=True)
    
    if request.method == 'POST':
        produto_id = request.POST.get('produto_id')
        quantidade = request.POST.get('quantidade')
        observacoes = request.POST.get('observacoes', '')
        
        try:
            produto = Produto.objects.get(id=produto_id)
            quantidade = int(quantidade)
            
            if quantidade <= 0:
                return render(request, 'registrar_venda.html', {
                    'entrada': entrada,
                    'produtos': produtos,
                    'erro': 'Quantidade deve ser maior que zero'
                })
            
            venda = Venda.objects.create(
                visitante=entrada.visitante,
                produto=produto,
                quantidade=quantidade,
                preco_unitario=produto.preco,
                observacoes=observacoes
            )
            
            return redirect('confirmar_venda', venda_id=venda.id)
        
        except (Produto.DoesNotExist, ValueError):
            return render(request, 'registrar_venda.html', {
                'entrada': entrada,
                'produtos': produtos,
                'erro': 'Dados inválidos'
            })
    
    return render(request, 'registrar_venda.html', {
        'entrada': entrada,
        'produtos': produtos,
    })

def confirmar_venda(request, venda_id):
    venda = get_object_or_404(Venda, id=venda_id)
    entrada = venda.visitante.entradas.latest('data_entrada')
    
    if request.method == 'POST':
        acao = request.POST.get('acao')
        
        if acao == 'nova_venda':
            return redirect('registrar_venda', entrada_id=entrada.id)
        elif acao == 'registrar_saida':
            entrada.data_saida = timezone.now()
            entrada.save()
            return redirect('index')
    
    return render(request, 'confirmar_venda.html', {
        'venda': venda,
        'entrada': entrada,
    })

def calcular_preco(request):
    produto_id = request.GET.get('produto_id')
    quantidade = request.GET.get('quantidade', 1)
    
    try:
        produto = Produto.objects.get(id=produto_id)
        quantidade = int(quantidade)
        total = float(produto.preco) * quantidade
        
        return JsonResponse({
            'sucesso': True,
            'preco_unitario': float(produto.preco),
            'total': total,
            'total_formatado': f"R$ {total:.2f}"
        })
    except (Produto.DoesNotExist, ValueError):
        return JsonResponse({'sucesso': False, 'erro': 'Produto não encontrado'})

def contatos(request):
    filtro = request.GET.get('filtro', 'todos')
    busca = request.GET.get('busca', '')
    
    visitantes = Visitante.objects.all()
    
    if filtro != 'todos':
        visitantes = visitantes.filter(tipo=filtro)
    
    if busca:
        visitantes = visitantes.filter(
            Q(nome__icontains=busca) | Q(telefone__icontains=busca)
        )
    
    visitantes = visitantes.annotate(
        total_visitas=Count('entradas'),
        total_gasto=Sum('vendas__total')
    ).order_by('-data_cadastro')
    
    return render(request, 'contatos.html', {
        'visitantes': visitantes,
        'filtro': filtro,
        'busca': busca,
    })

def relatorio(request):
    data_inicio = request.GET.get('data_inicio')
    data_fim = request.GET.get('data_fim')
    
    vendas = Venda.objects.all()
    
    if data_inicio:
        try:
            data_inicio = datetime.strptime(data_inicio, '%Y-%m-%d').date()
            vendas = vendas.filter(data_venda__date__gte=data_inicio)
        except ValueError:
            pass
    
    if data_fim:
        try:
            data_fim = datetime.strptime(data_fim, '%Y-%m-%d').date()
            vendas = vendas.filter(data_venda__date__lte=data_fim)
        except ValueError:
            pass
    
    vendas = vendas.order_by('-data_venda')
    
    total_vendas = vendas.aggregate(Sum('total'))['total__sum'] or 0
    total_itens = vendas.aggregate(Sum('quantidade'))['quantidade__sum'] or 0
    
    produtos_ranking = Produto.objects.filter(
        venda__in=vendas
    ).annotate(
        total_vendido=Sum('venda__quantidade'),
        valor_total=Sum('venda__total')
    ).order_by('-total_vendido')
    
    return render(request, 'relatorio.html', {
        'vendas': vendas,
        'total_vendas': f"{total_vendas:.2f}",
        'total_itens': total_itens,
        'produtos_ranking': produtos_ranking,
        'data_inicio': data_inicio,
        'data_fim': data_fim,
    })

def registrar_saida(request, entrada_id):
    entrada = get_object_or_404(Entrada, id=entrada_id)
    entrada.data_saida = timezone.now()
    entrada.save()
    return redirect('index')
