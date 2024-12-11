from modulo import Client, Investment  # Corrigido para importar o que é necessário

# Criando um cliente
cliente = Client(name="Alice")

# Criando uma conta e adicionando transações
conta = cliente.add_account(account_name="Conta Corrente")
conta.add_transaction(amount=500.0, category=1, description="Depósito")
conta.add_transaction(amount=-200.0, category=2, description="Compra")

# Exibindo saldo e transações
print(f"Saldo atual: R$ {conta.balance:.2f}")
for transacao in conta.transactions:
    print(transacao)

# Criando um investimento e calculando o patrimônio líquido
investimento = Investment(type="Fundo", amount=1000.0, rate_of_return=0.01, client=cliente)
cliente.add_investment(investimento)

print(f"Patrimônio líquido: R$ {cliente.get_net_worth():.2f}")
