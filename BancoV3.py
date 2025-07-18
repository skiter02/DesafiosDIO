class Historico:
    def __init__(self):
        self.transacoes = []

    def adicionar_transacao(self, transacao):
        self.transacoes.append(transacao)


class Transacao:
    def registrar(self, conta):
        raise NotImplementedError()


class Deposito(Transacao):
    def __init__(self, valor):
        self.valor = valor

    def registrar(self, conta):
        if conta.depositar(self.valor):
            conta.historico.adicionar_transacao(self)


class Saque(Transacao):
    def __init__(self, valor):
        self.valor = valor

    def registrar(self, conta):
        if conta.sacar(self.valor):
            conta.historico.adicionar_transacao(self)


class Conta:
    def __init__(self, cliente, numero, agencia="0001"):
        self.saldo = 0.0
        self.numero = numero
        self.agencia = agencia
        self.cliente = cliente
        self.historico = Historico()

    def sacar(self, valor):
        if valor > 0 and valor <= self.saldo:
            self.saldo -= valor
            return True
        print("Saque falhou: saldo insuficiente ou valor inválido.")
        return False

    def depositar(self, valor):
        if valor > 0:
            self.saldo += valor
            return True
        print("Depósito falhou: valor inválido.")
        return False

    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(cliente, numero)


class ContaCorrente(Conta):
    def __init__(self, cliente, numero, agencia="0001", limite=500.0, limite_saques=3):
        super().__init__(cliente, numero, agencia)
        self.limite = limite
        self.limite_saques = limite_saques
        self._saques_realizados = 0

    def sacar(self, valor):
        if self._saques_realizados >= self.limite_saques:
            print("Saque falhou: limite diário de saques atingido.")
            return False
        elif valor > self.limite:
            print("Saque falhou: valor excede o limite por saque.")
            return False
        elif super().sacar(valor):
            self._saques_realizados += 1
            return True
        return False


class PessoaFisica:
    def __init__(self, nome, cpf, data_nascimento, endereco):
        self.nome = nome
        self.cpf = cpf
        self.data_nascimento = data_nascimento
        self.endereco = endereco
        self.contas = []

    def adicionar_conta(self, conta):
        self.contas.append(conta)

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)


def exibir_extrato(conta):
    print("\n=========== EXTRATO ===========")
    print(f"Titular: {conta.cliente.nome}")
    print(f"Agência: {conta.agencia}  Conta: {conta.numero}")
    print("-------------------------------")
    if conta.historico.transacoes:
        for transacao in conta.historico.transacoes:
            tipo = transacao.__class__.__name__
            print(f"{tipo}: R$ {transacao.valor:.2f}")
    else:
        print("Não foram realizadas movimentações.")
    print(f"\nSaldo atual: R$ {conta.saldo:.2f}")
    print("===============================")