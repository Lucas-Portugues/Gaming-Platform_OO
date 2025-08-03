class User:

    def __init__(self, name, email, password):
        
        self.name = name
        self.email = email
        self.password = password
        self.money = 0

    def read_money(self):
        
        print(f"This user has {self.money} remaining in the account.")

class Games:

    def __init__(self, name, version = 1.0):
        self.name = name
        self.version = version
        self.online = None
    
    def verification_version(self):
        print(f"This game is in version {self.version}!")
    
class Catalogo:
   
    def __init__(self):
        self.jogos_disponiveis = []
       

    def adicionar_jogo_catalogo(self, game):
      
        if (game not in self.jogos_disponiveis):
            self.jogos_disponiveis.append(game)
            print(f"'{game.nome}' foi adicionado ao catálogo geral.")

    def mostrar_catalogo(self):
       
        print("\n CATÁLOGO DE JOGOS DISPONÍVEIS ")
        if not self.jogos_disponiveis:
            print("Nenhum jogo disponivel no catálogo no momento.")
        else:
            for jogo in self.jogos_disponiveis:
                print(f"- {jogo}")
    
   
my_user = User('Lucas', 'Abc', 2015)
my_user.read_money()

my_game = Games('GOW', '2.0')
my_game.verification_version()

shop = Catalogo()

shop.adicionar_jogo_catalogo(my_game)

shop.mostrar_catalogo()





