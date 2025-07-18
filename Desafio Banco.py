def menu_principal():
    return """
[d] Depositar
[s] Sacar
[e] Extrato
[n] Novo usuário
[c] Criar conta
[l] Listar contas
[q] Sair
=> """


# LISTAS
usuarios = []
contas = []


# FUNÇÕES AUXILIARES
def filtrar_usuario(cpf):
    return next((usuario for usuario in usuarios if usuario["cpf"] == cpf), None)


def criar_usuario():
    cpf = input("Informe o CPF (somente números): ")
    if filtrar_usuario(cpf):
        print("Já existe um usuário com esse CPF.")
        return

    nome = input("Informe o nome completo: ")
    nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/UF): ")

    usuarios.append({
        "nome": nome,
        "data_nascimento": nascimento,
        "cpf": cpf,
        "endereco": endereco
    })

    print("Usuário criado com sucesso!")


def criar_conta(agencia, numero_conta):
    cpf = input("Informe o CPF do usuário: ")
    usuario = filtrar_usuario(cpf)

    if usuario:
        contas.append({
            "agencia": agencia,
            "numero_conta": numero_conta,
            "usuario": usuario,
            "saldo": 0,
            "extrato": "",
            "saques_realizados": 0
        })
        print(f"Conta criada com sucesso! Número: {numero_conta}")
    else:
        print("Usuário não encontrado. Cadastre primeiro o usuário.")


def listar_contas():
    for conta in contas:
        print(f"\nAgência: {conta['agencia']}")
        print(f"Conta: {conta['numero_conta']}")
        print(f"Titular: {conta['usuario']['nome']}")


def depositar(conta, valor, /):  # apenas posicional
    if valor > 0:
        conta["saldo"] += valor
        conta["extrato"] += f"Depósito: R$ {valor:.2f}\n"
        print("Depósito realizado com sucesso!")
    else:
        print("Operação falhou! O valor é inválido.")


def sacar(*, conta, valor, limite, limite_saques):  # apenas por nome
    if valor <= 0:
        print("Operação falhou! Valor inválido.")
    elif valor > conta["saldo"]:
        print("Saldo insuficiente.")
    elif valor > limite:
        print("Valor excede o limite por saque.")
    elif conta["saques_realizados"] >= limite_saques:
        print("Limite de saques diários excedido.")
    else:
        conta["saldo"] -= valor
        conta["extrato"] += f"Saque: R$ {valor:.2f}\n"
        conta["saques_realizados"] += 1
        print("Saque realizado com sucesso!")


def exibir_extrato(conta):
    print("\n=========== EXTRATO ===========")
    print(f"Titular: {conta['usuario']['nome']}")
    print(f"Agência: {conta['agencia']}  Conta: {conta['numero_conta']}")
    print("-------------------------------")
    print(conta["extrato"] if conta["extrato"] else "Não foram realizadas movimentações.")
    print(f"\nSaldo atual: R$ {conta['saldo']:.2f}")
    print("===============================")

# EXECUÇÃO PRINCIPAL
AGENCIA = "0001"
contador_contas = 1
LIMITE_SAQUES = 3
LIMITE_VALOR_SAQUE = 500

while True:
    opcao = input(menu_principal())

    if opcao == "d":
        numero = int(input("Informe o número da conta: "))
        conta = next((c for c in contas if c["numero_conta"] == numero), None)
        if conta:
            valor = float(input("Informe o valor do depósito: "))
            depositar(conta, valor)
        else:
            print("Conta não encontrada.")

    elif opcao == "s":
        numero = int(input("Informe o número da conta: "))
        conta = next((c for c in contas if c["numero_conta"] == numero), None)
        if conta:
            valor = float(input("Informe o valor do saque: "))
            sacar(
                conta=conta,
                valor=valor,
                limite=LIMITE_VALOR_SAQUE,
                limite_saques=LIMITE_SAQUES
            )
        else:
            print("Conta não encontrada.")

    elif opcao == "e":
        numero = int(input("Informe o número da conta: "))
        conta = next((c for c in contas if c["numero_conta"] == numero), None)
        if conta:
            exibir_extrato(conta)
        else:
            print("Conta não encontrada.")

    elif opcao == "n":
        criar_usuario()

    elif opcao == "c":
        criar_conta(AGENCIA, contador_contas)
        contador_contas += 1

    elif opcao == "l":
        listar_contas()

    elif opcao == "q":
        break

    else:
        print("Operação inválida. Escolha novamente.")