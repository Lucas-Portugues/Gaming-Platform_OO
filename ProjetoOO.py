from abc import ABC, abstractmethod

class POOCoin:
    def __init__(self, valor):
        self.valor = round(valor, 2)
    def __str__(self): return f"P$ {self.valor:.2f}"
    def __add__(self, other): return POOCoin(self.valor + other.valor) if isinstance(other, POOCoin) else NotImplemented
    def __sub__(self, other): return POOCoin(self.valor - other.valor) if isinstance(other, POOCoin) else NotImplemented
    def __lt__(self, other): return self.valor < other.valor if isinstance(other, POOCoin) else NotImplemented

class Jogo:
   
    def __init__(self, nome, preco):
        self.nome = nome
        self.preco = preco
        self.loja = {}
        self.pontuacoes = {}

    def adicionar_pontuacao(self, nome_usuario, pontos):
        self.pontuacoes[nome_usuario] = self.pontuacoes.get(nome_usuario, 0) + pontos
        print(f"Pontuação de {nome_usuario} em {self.nome} atualizada para {self.pontuacoes[nome_usuario]} pontos.")

    def mostrar_ranking(self):
        print(f"\n {self.nome}")
        if not self.pontuacoes:
            print(" Ranking: Ninguém marcou pontos neste jogo ainda.")
            return
        ranking_ordenado = sorted(self.pontuacoes.items(), key=lambda item: item[1], reverse=True)
        print("  Ranking:")
        for i, (nome, pontos) in enumerate(ranking_ordenado, 1):
            print(f"    {i}. {nome} - {pontos} pontos")

class JogoOffline(Jogo):

    def __init__(self, nome, preco):
        super().__init__(nome, preco)

class JogoOnline(Jogo):
   
    def __init__(self, nome, preco):
        super().__init__(nome, preco)
        self.forum = []

    def postar_no_forum(self, nome_usuario, mensagem):
        self.forum.append(f"[{nome_usuario}]: {mensagem}")
        print("Mensagem postada no fórum!")

    def ver_forum(self):
        print(f"\n    Fórum de {self.nome}")
        if not self.forum: print("O fórum está vazio.")
        else:
            for post in self.forum: print(post)

class Usuario(ABC):

    def __init__(self, nome, email, senha, idade):
        self.nome = nome
        self.email = email
        self._senha = senha
        self.idade = idade
        self._saldo = POOCoin(0.0)
        self.inventario = {}
        self.jogos_adquiridos = {}
        self.preferencias = []
        self.tickets_suporte = []
        self.mensagens = []

    @property
    def saldo(self):
        return self._saldo
        
    def adicionar_saldo(self, valor_adicionar):
        if valor_adicionar.valor > 0:
            self._saldo += valor_adicionar
            print(f"Saldo adicionado!")
        else:
            print("O valor deve ser positivo.")

    def verificar_senha(self, senha):
        return self._senha == senha

    def atualizar_preferencias(self, novas_preferencias_str):
        self.preferencias = [p.strip() for p in novas_preferencias_str.split(',')]
        print(f"Preferências de {self.nome} atualizadas para: {self.preferencias}")

    @abstractmethod
    def obter_tipo_conta(self):
        pass
    
    def comprar_jogo(self, jogo):
        if jogo.nome in self.jogos_adquiridos:
            print("Você já possui o jogo '{jogo.nome}'.")
            return
        if self._saldo < jogo.preco:
            print("Saldo insuficiente para comprar '{jogo.nome}'.")
            return
        self._saldo -= jogo.preco
        self.jogos_adquiridos[jogo.nome] = jogo
        print(f"jogo '{jogo.nome} comprado com sucesso!'. Saldo atual: {self.saldo}")

    def comprar_item(self, jogo, nome_item):
        if jogo.nome not in self.jogos_adquiridos:
            print(f"Você precisa adquirir o jogo '{jogo.nome}' para comprar itens nele.")
            return
        if nome_item not in jogo.loja:
            print(f"Item '{nome_item}' não encontrado.")
            return
        preco = jogo.loja[nome_item]
        if self._saldo < preco:
            print(f"Saldo insuficiente.")
            return
        self._saldo -= preco
        if nome_item in self.inventario:
            self.inventario[nome_item] = self.inventario[nome_item] + 1
        else:
            self.inventario[nome_item] = 1
        print(f"'{nome_item}' comprado com sucesso! Novo saldo: {self.saldo}")

class UsuarioInfantil(Usuario):
 
    def __init__(self, nome, email, senha, idade, responsavel_email):
        super().__init__(nome, email, senha, idade)
        self.responsavel_email = responsavel_email
        self.status_aprovacao = 'pendente'
        self.permissoes = {'pode_comprar_itens': False, 'pode_comprar_jogos': False}

    def obter_tipo_conta(self):
        return "Infantil"

    def comprar_jogo(self, jogo):
       
        if self.status_aprovacao != 'aprovado':
            print("Sua conta precisa ser aprovada por um responsável.")
            return
        if not self.permissoes['pode_comprar_jogos']:
            print("Você não tem permissão para comprar jogos.")
            return
        super().comprar_jogo(jogo)

    def comprar_item(self, jogo, nome_item):
       
        if self.status_aprovacao != 'aprovado':
            print("Sua conta precisa ser aprovada por um responsável.")
            return
        if not self.permissoes['pode_comprar_itens']:
            print("Você não tem permissão para comprar itens.")
            return
        super().comprar_item(jogo, nome_item)

class UsuarioAdulto(Usuario):

    def obter_tipo_conta(self):
        return "Adulto"
    def definir_permissoes(self, dependente):
        print(f"\nConfigurando permissões para '{dependente.nome}':")
        perm_itens = input("Permitir que este usuário compre ITENS nos jogos? (s/n): ").lower()
        dependente.permissoes['pode_comprar_itens'] = (perm_itens == 's')
        perm_jogos = input("Permitir que este usuário compre JOGOS da loja? (s/n): ").lower()
        dependente.permissoes['pode_comprar_jogos'] = (perm_jogos == 's')
        print("Permissões salvas.")

class Admin(Usuario):
 
    def __init__(self, nome, email, senha):
        super().__init__(nome, email, senha, 23)
    def obter_tipo_conta(self):
        return "Admin"

class Plataforma:
  
    def __init__(self):
        self.usuarios = {}
        self.jogos = {}
        #Admin padrão da plataforma
        self.usuarios["admin"] = Admin("lucas", "POO@ic.ufal.br", "admin123")
    
    def encontrar_usuario(self, nome_ou_email):
        for user in self.usuarios.values():
            if user.nome == nome_ou_email or user.email == nome_ou_email:
                return user
        return None

    def executar(self):
     
        while True:
            print("\n    MENU PRINCIPAL\n")
            print("1 - Login")
            print("2 - Criar nova conta")
            print("3 - Sair")
            escolha = input("\nEscolha uma opção: ")

            if escolha == "1": self.login()
            elif escolha == "2": self.criar_usuario()
            elif escolha == "3":
                print("Obrigado por jogar! Saindo...")
                break
            else: print("Opção inválida!")

    def criar_usuario(self):
        nome = input("Digite o nome do novo usuário: ")
        if self.encontrar_usuario(nome):
            print("Nome de usuário já existe!")
            return
        email = input("Digite seu e-mail: ")
        if self.encontrar_usuario(email):
            print("E-mail já cadastrado!")
            return
        try:
            idade = int(input("Digite sua idade: "))
        except ValueError:
            print("Idade inválida.")
            return
        senha = input("Digite sua senha: ")

        if idade < 18:
            email_resp = input("Por ser menor de idade, digite o e-mail de um responsável já cadastrado: ")
            responsavel = self.encontrar_usuario(email_resp)
            if isinstance(responsavel, UsuarioAdulto):
                novo_usuario = UsuarioInfantil(nome, email, senha, idade, email_resp)
                self.usuarios[nome] = novo_usuario
                responsavel.mensagens.append(f"Sistema: O usuário '{nome}' ({idade} anos) solicitou aprovação como seu dependente.")
                print("\nConta criada! Peça ao seu responsável para checar as mensagens e aprovar seu cadastro.")
            else:
                print("\nE-mail do responsável não encontrado ou não é uma conta de adulto. Cadastro cancelado.")
        else:
            novo_usuario = UsuarioAdulto(nome, email, senha, idade)
            self.usuarios[nome] = novo_usuario
            print("\nConta criada com sucesso!\n")
    
    def login(self):
        nome_usuario = input("Digite seu nome de usuário ou e-mail: ")
        senha = input("Digite sua senha: ")
        usuario = self.encontrar_usuario(nome_usuario)

        if usuario and usuario.verificar_senha(senha):
            print(f"\nLogin bem-sucedido! Bem-vindo, {usuario.nome}!\n")
            if isinstance(usuario, Admin): self.menu_admin(usuario)
            else: self.menu_usuario(usuario)
        else:
            print("\nUsuário ou senha inválidos.\n")
    
    def menu_admin(self, admin):
        while True:
            print("\n1 - Gerenciar Jogos")
            print("2 - Adicionar Pontuação a um Jogador")
            print("3 - Listar Usuários")
            print("4 - Deslogar\n")

            escolha = input("> ")

            if escolha == '1': self.gerenciar_jogos_admin()
            elif escolha == '2':
                nome_usr = input("Adicionar pontos para qual usuário? ")
                usuario = self.encontrar_usuario(nome_usr)
                if not usuario:
                    print("Usuário não encontrado.")
                    continue
                nome_jogo = input(f"Em qual jogo adicionar pontos para {nome_usr}? ")
                jogo = self.jogos.get(nome_jogo)
                if not jogo:
                    print("Jogo não encontrado.")
                    continue
                if nome_jogo not in usuario.jogos_adquiridos:
                    print(f"Erro: O usuário '{usuario.nome}' não possui o jogo '{nome_jogo}'.")
                    continue
                try:
                    pontos = int(input("Quantos pontos? "))
                    jogo.adicionar_pontuacao(usuario.nome, pontos)
                except ValueError: print("Valor de pontos inválido.")
            elif escolha == '3':
                for u in self.usuarios.values(): print(f"- {u.nome} ({u.obter_tipo_conta()})")
            elif escolha == '4': break
    
    def gerenciar_jogos_admin(self):
        while True:
            print("\n    Gerenciamento de Jogos\n")
            print("1 - Adicionar jogo")
            print("2 - Adicionar item a um jogo")
            print("3 - Voltar")
            escolha = input("> ")
            if escolha == '1':
                nome_jogo = input("Nome do jogo: ")
                if nome_jogo in self.jogos:
                    print("Jogo já existe.")
                    continue
                try:
                    preco = float(input("Preço do jogo em POOCoins: "))
                    preco_jogo = POOCoin(preco)
                except ValueError:
                    print("Preço inválido.")
                    continue
                tipo = input("\nJogo é (1) Online ou (2) Offline? ")
                if tipo == '1': self.jogos[nome_jogo] = JogoOnline(nome_jogo, preco_jogo)
                elif tipo == '2': self.jogos[nome_jogo] = JogoOffline(nome_jogo, preco_jogo)
                else: 
                    print("Tipo inválido. Jogo não criado.")
                    continue
                print("\nJogo adicionado!")
            elif escolha == '2':
                nome_jogo = input("Adicionar item em qual jogo? ")
                if nome_jogo not in self.jogos:
                    print("Jogo não encontrado.")
                    continue
                item = input("Nome do item: ")
                try:
                    preco = float(input("Preço em POOCoins: "))
                    self.jogos[nome_jogo].loja[item] = POOCoin(preco)
                    print("Item adicionado à loja!")
                except ValueError: print("Preço inválido.")
            elif escolha == '3': break
    
    def menu_usuario(self, usuario):
        if isinstance(usuario, UsuarioInfantil) and usuario.status_aprovacao == 'pendente':
            print("\nSua conta está pendente de aprovação. Peça para seu responsável liberá-la.")
            return

        while True:
            
            print(f"\n    Menu: {usuario.nome} | Saldo: {usuario.saldo}\n")
            if isinstance(usuario, UsuarioAdulto):
                print("0 - Gerenciar Dependentes")
            print("1 - Loja de Jogos")
            print("2 - Comprar Item")
            print("3 - Adicionar Saldo")
            print("4 - Ver Catálogo de Jogos e Rankings")
            print("5 - Gerenciar Preferências")
            print("6 - Acessar Fórum (Jogos Online)")
            print("7 - Suporte ao Usuário")
            print("8 - Ver Minhas Mensagens")
            print("9 - Deslogar")
            escolha = input("> ")

            if escolha == '1':
            
                
                print("\n    Loja de Jogos Disponíveis")

                jogos_a_venda = {}
            
                for nome, jogo in self.jogos.items():
                    if nome not in usuario.jogos_adquiridos:
                        jogos_a_venda[nome] = jogo

                if not jogos_a_venda:
                    print("Você já possui todos os jogos da plataforma!")
                else:
                  
                    for nome, jogo in jogos_a_venda.items():
                        print(f"- {nome} | Preço: {jogo.preco}")
                    
                    jogo_a_comprar = input("Digite o nome do jogo que deseja comprar (ou enter para voltar): ")

                    if jogo_a_comprar in jogos_a_venda:
                       
                        usuario.comprar_jogo(jogos_a_venda[jogo_a_comprar])
                    elif jogo_a_comprar:

                        print("Jogo não encontrado na loja.")
        
            elif escolha == '2':
                print("\n    Sua Biblioteca de Jogos")
                if not usuario.jogos_adquiridos:
                    print("Você ainda não possui jogos.")
                else:
                    for nome_jogo in usuario.jogos_adquiridos.keys(): print(f"- {nome_jogo}")
                    nome_jogo = input("Comprar item de qual jogo? ")
                    if nome_jogo in usuario.jogos_adquiridos:
                        item = input("Qual item? ")
                        usuario.comprar_item(self.jogos[nome_jogo], item)
                    else: print("Você não possui este jogo.")
            elif escolha == '3':
                try:
                    valor = float(input("Digite o valor em POOCoins para adicionar: "))
                    usuario.adicionar_saldo(POOCoin(valor))
                except ValueError: print("Valor inválido.")
            elif escolha == '4':
                for jogo in self.jogos.values(): jogo.mostrar_ranking()
            elif escolha == '5':
                prefs = input("Digite suas preferências, separadas por vírgula (ex: RPG, Aventura): ")
                usuario.atualizar_preferencias(prefs)
            elif escolha == '6':
                nome_jogo = input("Acessar fórum de qual jogo? ")
                jogo = self.jogos.get(nome_jogo)
                if isinstance(jogo, JogoOnline):
                    if jogo.nome in usuario.jogos_adquiridos:
                        jogo.ver_forum()
                        postar = input("Deseja postar uma mensagem? (s/n) ")
                        if postar.lower() == 's':
                            msg = input("Sua mensagem: ")
                            jogo.postar_no_forum(usuario.nome, msg)
                    else: print("Você precisa possuir este jogo para acessar o fórum.")
                else: print("Este jogo não é online ou não existe.")
            elif escolha == '7': self.menu_suporte(usuario)
            elif escolha == '8':
                print("\n    Caixa de Entrada\n")
                if not usuario.mensagens:
                    print("Nenhuma mensagem.")
                for msg in usuario.mensagens: print(f"- {msg}")
            elif escolha == '0' and isinstance(usuario, UsuarioAdulto): self.menu_dependentes(usuario)
            elif escolha == '9': break

    def menu_suporte(self, usuario):
        print("\n    Central de Suporte")
        print("1 - Abrir um ticket de suporte")
        print("2 - Ver meus tickets")
        escolha = input("> ")
        if escolha == '1':
            problema = input("Descreva seu problema: ")
            usuario.tickets_suporte.append({'problema': problema, 'status': 'Aberto'})
            print("Ticket aberto com sucesso!")
        elif escolha == '2':
            if not usuario.tickets_suporte:
                print("Você não tem tickets abertos.")
            for i, ticket in enumerate(usuario.tickets_suporte, 1):
                print(f"{i}. Problema: {ticket['problema']} | Status: {ticket['status']}")

    def menu_dependentes(self, usuario_adulto):
        print("\n    Gerenciamento de Dependentes ")
        pendentes = [u for u in self.usuarios.values() if isinstance(u, UsuarioInfantil) and u.responsavel_email == usuario_adulto.email and u.status_aprovacao == 'pendente']
        if pendentes:
            print("Contas pendentes de aprovação:")
            for i, dep in enumerate(pendentes, 1):
                print(f"{i} - {dep.nome} (Idade: {dep.idade})")
            try:
                escolha = int(input("Digite o número da conta para aprovar (ou 0 para cancelar): "))
                if 0 < escolha <= len(pendentes):
                    dependente_aprovado = pendentes[escolha-1]
                    dependente_aprovado.status_aprovacao = 'aprovado'
                    print(f"Conta de {dependente_aprovado.nome} aprovada!")
                    usuario_adulto.definir_permissoes(dependente_aprovado)
            except ValueError:
                print("Entrada inválida.")
        else:
            print("Nenhuma conta pendente de aprovação.")

# =================================================================================
plataforma_gaming = Plataforma()

print("    Configurando dados")
print("\n...")

jogo1 = JogoOnline("Aventuras_em_POO", POOCoin(100.0))
jogo2 = JogoOffline("Semestre_Rush", POOCoin(50.0))
plataforma_gaming.jogos[jogo1.nome] = jogo1
plataforma_gaming.jogos[jogo2.nome] = jogo2

jogo1.loja['Ponto_Extra'] = POOCoin(10.0)
jogo1.postar_no_forum("lucas", "Não sei programar em Python! :(")

luu = UsuarioAdulto("luu", "luu@ic.com", "luu123", 30)
rafael = UsuarioInfantil("rafael", "rafael@email.com", "rafael123", 12, "luu@ic.com")
maria = UsuarioInfantil("maria", "maria@email.com", "maria123", 10, "luu@ic.com")
plataforma_gaming.usuarios.update({luu.nome: luu, rafael.nome: rafael, maria.nome: maria})

luu.adicionar_saldo(POOCoin(250))
rafael.adicionar_saldo(POOCoin(75))

rafael.status_aprovacao = 'aprovado'
rafael.permissoes['pode_comprar_itens'] = True
rafael.permissoes['pode_comprar_jogos'] = False

luu.mensagens.append(f"Sistema: A usuária '{maria.nome}' ({maria.idade} anos) solicitou aprovação como sua dependente.")
    
jogo1.adicionar_pontuacao(luu.nome, 2100)
jogo1.adicionar_pontuacao(rafael.nome, 1250)

luu.comprar_jogo(jogo1)

rafael.comprar_jogo(jogo1)
    
print("\n    Configuração inicial concluída!")
    
plataforma_gaming.executar()