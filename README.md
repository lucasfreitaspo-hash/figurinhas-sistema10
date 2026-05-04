# 🎴 Mister Wiz - Sistema de Figurinhas da Copa do Mundo

Sistema de gerenciamento de vendas e contatos para loja de figurinhas Panini da Copa do Mundo.

## 🌟 Características

- ✅ Registro de entrada e saída de visitantes
- ✅ Sistema de vendas com cálculo automático de preços
- ✅ Base de dados de contatos
- ✅ Relatórios de vendas
- ✅ Interface responsiva com design Mister Wiz
- ✅ Funciona em múltiplas máquinas da rede

## 🛍️ Produtos

- **Capa Mole (Brochura)**: R$ 24,90
- **Capa Dura**: R$ 74,90
- **Pacote de Figurinhas (7 unidades)**: R$ 7,00

## 🚀 Como Rodar

### Pré-requisitos
- Python 3.8+
- pip

### Instalação

```bash
git clone https://github.com/lucasfreitaspo-hash/figurinhas-sistema.git
cd figurinhas-sistema
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver 0.0.0.0:8000
