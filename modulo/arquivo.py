from datetime import datetime, timedelta
from typing import List


class Transaction:
    """
    Representa uma transação financeira.

    Atributos:
    amount (float): O valor da transação.
    date (datetime): A data da transação.
    category (int): A categoria da transação.
    description (str): A descrição da transação.
    """

    def __init__(self, amount: float, category: int, description: str = "") -> None:
        """
        Inicializa uma nova transação.

        Parameters:
        amount (float): O valor da transação.
        category (int): A categoria da transação.
        description (str): A descrição da transação.
        """
        self.amount = amount
        self.date = datetime.now()
        self.category = category
        self.description = description

    def __str__(self) -> str:
        """
        Retorna uma representação em string da transação.

        Returns:
        str: Descrição da transação com o valor e a categoria.
        """
        return f"Transação: {self.description} R$ {self.amount:.2f} ({self.category})"
    
    def update(self, **attributes) -> None:
        """
        Atualiza os atributos da transação.

        Parameters:
        attributes (dict): Dicionário de atributos a serem atualizados.
        """
        for key, value in attributes.items():
            if hasattr(self, key):
                setattr(self, key, value)


class Account:
    """
    Representa uma conta bancária.

    Atributos:
    name (str): O nome da conta.
    balance (float): O saldo atual da conta.
    transactions (List[Transaction]): Lista de transações realizadas na conta.
    """

    def __init__(self, name: str) -> None:
        """
        Inicializa uma nova conta bancária.

        Parameters:
        name (str): O nome da conta.
        """
        self.name: str = name
        self.balance: float = 0.0
        self.transactions: List[Transaction] = []

    def add_transaction(self, amount: float, category: int, description: str = "") -> Transaction:
        """
        Adiciona uma transação à conta.

        Parameters:
        amount (float): O valor da transação.
        category (int): A categoria da transação.
        description (str): A descrição da transação.

        Returns:
        Transaction: A transação criada e adicionada à conta.
        """
        transaction = Transaction(amount, category, description)
        self.transactions.append(transaction)
        self.balance += amount
        return transaction

    def get_transactions(self, start_date: datetime = None, end_date: datetime = None, category: int = None) -> List[Transaction]:
        """
        Obtém as transações dentro de um intervalo de datas e/ou categoria.

        Parameters:
        start_date (datetime): Data inicial para o filtro de transações.
        end_date (datetime): Data final para o filtro de transações.
        category (int): Categoria das transações a serem filtradas.

        Returns:
        List[Transaction]: Lista de transações filtradas.
        """
        result = self.transactions
        if start_date:
            result = [t for t in result if t.date >= start_date]
        if end_date:
            result = [t for t in result if t.date <= end_date]
        if category:
            result = [t for t in result if t.category == category]
        return result


class Investment:
    """
    Representa um investimento realizado por um cliente.

    Atributos:
    type (str): O tipo de investimento.
    initial_amount (float): O valor inicial investido.
    date_purchased (datetime): A data de aquisição do investimento.
    rate_of_return (float): A taxa de retorno do investimento por mês.
    client (Client): O cliente que fez o investimento.
    """

    def __init__(self, type: str, amount: float, rate_of_return: float, client: 'Client'):
        """
        Inicializa um investimento.

        Parameters:
        type (str): O tipo de investimento (ex. Ações, Títulos, etc).
        amount (float): O valor inicial investido.
        rate_of_return (float): A taxa de retorno do investimento por mês.
        client (Client): O cliente que fez o investimento.
        """
        self.type: str = type
        self.initial_amount: float = amount
        self.date_purchased: datetime = datetime.now()
        self.rate_of_return: float = rate_of_return
        self.client: 'Client' = client

    def calculate_value(self) -> float:
        """
        Calcula o valor atual do investimento considerando a taxa de retorno.

        Returns:
        float: O valor atual do investimento.
        """
        months = (datetime.now().year - self.date_purchased.year) * 12 + (datetime.now().month - self.date_purchased.month)
        return self.initial_amount * ((1 + self.rate_of_return) ** months)

    def sell(self, account: Account) -> None:
        """
        Vende o investimento e adiciona o valor à conta do cliente.

        Parameters:
        account (Account): A conta do cliente onde o valor será adicionado.
        """
        current_value = self.calculate_value()
        account.add_transaction(current_value, 0, f"Venda de {self.type}")


class Client:
    """
    Representa um cliente que pode ter várias contas e investimentos.

    Atributos:
    name (str): O nome do cliente.
    accounts (List[Account]): Lista de contas bancárias do cliente.
    investments (List[Investment]): Lista de investimentos do cliente.
    """

    def __init__(self, name: str) -> None:
        """
        Inicializa um cliente.

        Parameters:
        name (str): O nome do cliente.
        """
        self.name: str = name
        self.accounts: List[Account] = []
        self.investments: List[Investment] = []

    def add_account(self, account_name: str) -> Account:
        """
        Adiciona uma conta bancária ao cliente.

        Parameters:
        account_name (str): O nome da nova conta.

        Returns:
        Account: A conta criada e adicionada ao cliente.
        """
        account = Account(account_name)
        self.accounts.append(account)
        return account

    def add_investment(self, investment: Investment) -> None:
        """
        Adiciona um investimento ao cliente.

        Parameters:
        investment (Investment): O investimento a ser adicionado.
        """
        self.investments.append(investment)

    def get_net_worth(self) -> float:
        """
        Calcula o patrimônio líquido do cliente, somando o saldo das contas e o valor dos investimentos.

        Returns:
        float: O patrimônio líquido do cliente.
        """
        account_balance = sum(account.balance for account in self.accounts)
        investment_value = sum(investment.calculate_value() for investment in self.investments)
        return account_balance + investment_value


# Testes
if __name__ == "__main__":
    # Criando um cliente
    client = Client("Alice")

    # Adicionando uma conta
    account = client.add_account("Conta Corrente")
    account.add_transaction(1000, 1, "Salário")
    account.add_transaction(-200, 2, "Compra no mercado")
    print(f"Saldo na conta: R$ {account.balance:.2f}")

    # Listando transações
    print("Transações na conta:")
    for transaction in account.get_transactions():
        print(transaction)

    # Criando um investimento
    investment = Investment("Ações", 5000, 0.02, client)
    client.add_investment(investment)

    # Calculando o patrimônio líquido
    net_worth = client.get_net_worth()
    print(f"Patrimônio líquido: R$ {net_worth:.2f}")

    # Vendendo investimento
    investment.sell(account)
    print(f"Saldo após venda do investimento: R$ {account.balance:.2f}")
