import time
import statistics

movimentacoes = []
pedidos_reposicao = []

ocorrencias = {
  "comparacoes": 0,
  "trocas": 0,
  "acessos": 0,
  "operacoes": 0
}

def zerar_as_ocorrencias():
  ocorrencias["comparacoes"] = 0
  ocorrencias["trocas"] = 0
  ocorrencias["acessos"] = 0
  ocorrencias["operacoes"] = 0

def tempo_da_ordenacao(lista, campo, maior=False):
  zerar_as_ocorrencias()

  comeco = time.perf_counter()
  resultado = ordenar_geral(lista, campo, maior)
  fim = time.perf_counter()

  tempototal = fim - comeco
  return resultado, tempototal, ocorrencias.copy()


def calcular_o_desempenho(funcao):
  zerar_as_ocorrencias()

  comeco = time.perf_counter()
  resultado = funcao()
  fim = time.perf_counter()

  tempototal = fim - comeco
  
  return resultado, tempototal, ocorrencias.copy()


def repetir_o_calculo(funcao, quantidade=5):
  tempos = []
  resultado = None
  contadores = None

  for repeticao in range(quantidade):
    resultado, tempo, contadores = calcular_o_desempenho(funcao)
    tempos.append(tempo)

  media = statistics.mean(tempos)
  desvio = statistics.stdev(tempos) if quantidade > 1 else 0
  
  return resultado, media, desvio, contadores

  
def obrigatorio(mensagem):
    while True:
        valor = input(mensagem).strip()
        if valor != "":
            return valor
        print("\nÉ obrigatorio informar esse campo ")
      
      
def numero(mensagem):
    while True:
        try:
            valor = int(input(mensagem))
            if valor >= 0:
                return valor
            print("\nPrecisa digitar um número positivo ")
        except ValueError:
            print("\nPrecisa digitar um número inteiro ")

          
def valor_monetario(mensagem):
    while True:
        try:
            valor = input(mensagem).replace("R$", "").replace(",", ".").strip()
            valor = float(valor)
            if valor >= 0:
                return valor
            print("\nPrecisa digitar um valor positivo ")
        except ValueError:
            print("Precisa digitar um valor válido, Exemplo: R$ 12,50")


def data_valida(mensagem):
    while True:
        valor = input(mensagem).strip()
        partes = valor.split("/")
        if (len(partes) == 3 and all(parte.isdigit() for parte in partes)
                and len(partes[0]) == 2 and len(partes[1]) == 2
                and len(partes[2]) == 4 and 1 <= int(partes[0]) <= 31
                and 1 <= int(partes[1]) <= 12):
            return valor
        print("a data precisa estar no formato 10/10/2027.")


def data_ordenacao(valor):
    partes = valor.split("/")
    return partes[2] + partes[1] + partes[0]


def buscar(lista, campo, valor):
    for i in range(len(lista)):
        if lista[i][campo] == valor:
            return i
    return -1

  
def valor_de_comparacao(item, campo):
  ocorrencias["acessos"] += 1
  valor = item[campo]
  if campo == "validade":
    valor = data_ordenacao(valor)
  return valor

def juntar_todos(esquerda, direita, campo, maior=False):
  resultado = []
  a = 0
  b = 0

  while a < len(esquerda) and b < len(direita):
    valor_da_esquerda = valor_de_comparacao(esquerda[a], campo)
    valor_da_direita = valor_de_comparacao(direita[b], campo)

    ocorrencias["comparacoes"] += 1

    if maior:
      if valor_da_esquerda >= valor_da_direita:
        resultado.append(esquerda[a])
        ocorrencias["trocas"] += 1
        a += 1
      else:
        resultado.append(direita[b])
        ocorrencias["trocas"] += 1
        b += 1

    else:
      if valor_da_esquerda <= valor_da_direita:
        resultado.append(esquerda[a])
        ocorrencias["trocas"] += 1
        a += 1
      else:
        resultado.append(direita[b])
        ocorrencias["trocas"] += 1 
        b += 1

  while a < len(esquerda):
    resultado.append(esquerda[a])
    ocorrencias["trocas"] += 1
    a += 1

  while b < len(direita):
    resultado.append(direita[b])
    ocorrencias["trocas"] += 1
    b += 1

  return resultado

def ordenar_geral(lista, campo, maior=False):
  lista_nova = []

  for item in lista:
    lista_nova.append(item.copy())

  if len(lista_nova) <= 1:
    return lista_nova

  meio = len(lista_nova) // 2

  esquerda = ordenar_geral(lista_nova[:meio], campo, maior)

  direita = ordenar_geral(lista_nova[meio:], campo, maior)

  return juntar_todos(esquerda, direita, campo, maior)



class NoAVL:
    def __init__(self, remedio):
        self.remedio = remedio
        self.esquerda = None
        self.direita = None
        self.altura = 1


class ArvoreAVL:
    def __init__(self):
        self.raiz = None

    def altura_no(self, no):
        if no is None:
            return 0
        return no.altura

    def balanceamento(self, no):
        if no is None:
            return 0
        return self.altura_no(no.esquerda) - self.altura_no(no.direita)

    def rotacao_para_esquerda(self, no):
        direita = no.direita
        meio = direita.esquerda

        direita.esquerda = no
        no.direita = meio

        no.altura = 1 + max(
            self.altura_no(no.esquerda), self.altura_no(no.direita)
        )

        direita.altura = 1 + max(
            self.altura_no(direita.esquerda), self.altura_no(direita.direita)
        )

        return direita

    def rotacao_para_direita(self, no):
        esquerda = no.esquerda
        meio = esquerda.direita

        esquerda.direita = no
        no.esquerda = meio

        no.altura = 1 + max(
            self.altura_no(no.esquerda), self.altura_no(no.direita)
        )

        esquerda.altura = 1 + max(
            self.altura_no(esquerda.esquerda), self.altura_no(esquerda.direita)
        )

        return esquerda

    def inserir(self, remedio):
        self.raiz = self.inserir_no(self.raiz, remedio)

    def inserir_no(self, no, remedio):
        if no is None:
            return NoAVL(remedio)

        if remedio["codigo"] < no.remedio["codigo"]:
            no.esquerda = self.inserir_no(no.esquerda, remedio)

        elif remedio["codigo"] > no.remedio["codigo"]:
            no.direita = self.inserir_no(no.direita, remedio)

        else:
            print("Já temos um remedio com esse codigo")
            return no

        no.altura = 1 + max(
            self.altura_no(no.esquerda), self.altura_no(no.direita)
        )

        balanceamento = self.balanceamento(no)
      
        if balanceamento > 1:
            if remedio["codigo"] < no.esquerda.remedio["codigo"]:
                return self.rotacao_para_direita(no)
            else:
                no.esquerda = self.rotacao_para_esquerda(no.esquerda)
                return self.rotacao_para_direita(no)

        if balanceamento < -1:
            if remedio["codigo"] > no.direita.remedio["codigo"]:
                return self.rotacao_para_esquerda(no)
            else:
                no.direita = self.rotacao_para_direita(no.direita)
                return self.rotacao_para_esquerda(no)

        return no

    def buscar(self, no, codigo):
        if no is None:
            return None

        ocorrencias["acessos"] += 1
        ocorrencias["comparacoes"] += 1
        ocorrencias["operacoes"] += 1
      
        if codigo == no.remedio["codigo"]:
            return no.remedio
          
        ocorrencias["comparacoes"] += 1
        ocorrencias["operacoes"] += 1


        if codigo < no.remedio["codigo"]:
            return self.buscar(no.esquerda, codigo)

        return self.buscar(no.direita, codigo)

    def listar(self):
      lista = []
      self.listar_no(self.raiz, lista)
      return lista

    def listar_no(self, no, lista):
      if no is not None:
        self.listar_no(no.esquerda, lista)
        lista.append(no.remedio)
        self.listar_no(no.direita, lista)

    def pre_ordem(self, no, lista):
      if no is not None:
        lista.append(no.remedio)
        self.pre_ordem(no.esquerda, lista)
        self.pre_ordem(no.direita, lista)

    def pos_ordem(self, no, lista):
      if no is not None:
        self.pos_ordem(no.esquerda, lista)
        self.pos_ordem(no.direita, lista)
        lista.append(no.remedio)
  
    def menor_no(self, no):
      atual = no

      while atual.esquerda is not None:
        atual = atual.esquerda

      return atual  

    def remover(self, codigo):
      self.raiz = self.remover_no(self.raiz, codigo)

    def remover_no(self, no, codigo):
      if no is None:
        return None

      if codigo < no.remedio["codigo"]:
        no.esquerda = self.remover_no(no.esquerda, codigo)


      elif codigo > no.remedio["codigo"]:
        no.direita = self.remover_no(no.direita, codigo)

      else:  
        if no.esquerda is None:
          return no.direita

        if no.direita is None:
          return no.esquerda


        menor = self.menor_no(no.direita)
        no.remedio = menor.remedio
        no.direita =self.remover_no(no.direita, menor.remedio["codigo"])

      no.altura = 1 + max(self.altura_no(no.esquerda), self.altura_no(no.direita))
      balanceamento = self.balanceamento(no)

      if balanceamento > 1:
        if self.balanceamento(no.esquerda) >= 0:
          return self.rotacao_para_direita(no)


        no.esquerda = self.rotacao_para_esquerda(no.esquerda)
        return self.rotacao_para_direita(no)

      if balanceamento < -1:
        if self.balanceamento(no.direita) <=0:
          return self.rotacao_para_esquerda(no)

        no.direita = self.rotacao_para_direita(no.direita)
        return self.rotacao_para_esquerda(no)

      return no

      
         
class Mudancas:
    def registrar(self, mudanca):
        movimentacoes.append(mudanca)
    def desfazer(self):
        if len(movimentacoes) == 0:
            print("\nNo momento não há nenhuma necessidade de mudança\n")
            return
          
        mudanca = movimentacoes.pop()
        tipo = mudanca["tipo"]
        
      
        if tipo == "entrada" or tipo == "saida":
            remedio = arvore_remedios.buscar(arvore_remedios.raiz, mudanca["codigo"])
            if remedio is not None:
              remedio["quantidade"] = mudanca["quantidade_anterior"]
            print("\nO registro da ultima movimentação foi excluido")
          
        elif tipo == "adicionar_remedio":
            codigo = mudanca["dados"]["codigo"]
            
            arvore_remedios.remover(codigo)
            print("\nO registro do ultimo cadastro de remedios foi excluido ")
          
        elif tipo == "remover_remedio":
            arvore_remedios.inserir(mudanca["dados"])
            print("\nO registro do ultimo cadastro de remedios foi excluido ")
          
        elif tipo == "mudar_remedio":
            remedio = arvore_remedios.buscar(arvore_remedios.raiz, mudanca["codigo"])
            if remedio is not None:
              anterior = mudanca["anterior"]
              remedio["codigo"] = anterior["codigo"]
              remedio["nome"] = anterior["nome"]
              remedio["fabricacao"] = anterior["fabricacao"]
              remedio["validade"] = anterior["validade"]
              remedio["preco"] = anterior["preco"]
              remedio["quantidade"] = anterior["quantidade"]
              remedio["criticidade"] =  anterior["criticidade"]

              
             
            print("O registro da ultima alteração de remédio foi excluido ")
          
        elif tipo == "adicionar_fornecedor":
            codigo = mudanca["dados"]["codigo"]
            arvore_fornecedores.remover(codigo)
            
            print("\nO registro do ultimo cadastro de fornecedores foi excluido ")
          
        elif tipo == "remover_fornecedor":
            arvore_fornecedores.inserir(mudanca["dados"])
            print("\nO registro da ultima remoção de fornecedores foi excluida ")
          
        elif tipo == "mudar_fornecedor":
            fornecedor = arvore_fornecedores.buscar(arvore_fornecedores.raiz, mudanca["codigo"])

            if fornecedor is not None:
              fornecedor["codigo"] = mudanca["anterior"]["codigo"]
              fornecedor["nome"] = mudanca["anterior"]["nome"]
              fornecedor["telefone"] = mudanca["anterior"]["telefone"]
            
            print("\nO registro da ultima alteração de fornecedores foi excluida ")


  
class Cadastros:
  
    def remedios(self):
        while True:
            print("\n                            ==============================")
            print("                                       Remedios           ")
            print("                            ==============================")
            print("\n 1 / Adicionar")
            print(" 2 / Consultar")
            print(" 3 / Mudar ")
            print(" 4 / Remover ")
            print(" 0 / Voltar pro menu principal da ERP")
          
            opcao = input("\nSua ecolha --> ")
            if opcao == "1":
              self.adicionar_remedio()
            elif opcao == "2":
              self.consultar_remedio()
            elif opcao == "3":
              self.mudar_remedio()
            elif opcao == "4":
              self.remover_remedio()
            elif opcao == "0":
              break
            else: print("\nOpção inválida ")
              
    def fornecedores(self):
      
        while True:
            print("\n                            ==============================")
            print("                                    Fornecedores         ")
            print("                            ==============================")
            print("\n 1 / Adicionar")
            print(" 2 / Consultar")
            print(" 3 / Mudar")
            print(" 4 / Remover")
            print(" 0 / Voltar pro menu principal ERP")
          
            opcao = input("\nSua scolha --> ")
          
            if opcao == "1": self.adicionar_fornecedor()
            elif opcao == "2": self.consultar_fornecedor()
            elif opcao == "3": self.mudar_fornecedor()
            elif opcao == "4": self.remover_fornecedor()
            elif opcao == "0": break
            else: print("\nOpção inválida ")
              
    def adicionar_remedio(self):
        codigo = obrigatorio("\nDigite o código do remédio -  ")
        if arvore_remedios.buscar(arvore_remedios.raiz, codigo) is not None:
          print("\nJá temos um remédio cadastrado com esse código")
          return
            
        fabricacao = data_valida("Fabricação (dd/mm/aaaa) - ")
        validade = data_valida("Validade final (dd/mm/aaaa) - ")
        if data_ordenacao(validade) < data_ordenacao(fabricacao):
            print("\nA data de validade final  não pode ser anterior à fabricação.")
            return

        remedio = {"codigo": codigo,
                   "nome": obrigatorio("Nome do remédio -  "),
                   "fabricacao": fabricacao,
                   "validade": validade,
                   "preco": valor_monetario("Valor do remédio (R$) - "),
                   "quantidade": numero("Quantidade -  "),
                   "criticidade": numero("Criticidade do remédio (1 a 3) - ")}
        arvore_remedios.inserir(remedio)
        mudancas.registrar({"tipo": "adicionar_remedio", "dados": remedio.copy()})
        print("\nAdicionado à sessão de cadastros da ERP")

      
    def consultar_remedio(self):
        codigo = obrigatorio("\nCódigo do remedio -  ")
        remedio = arvore_remedios.buscar(arvore_remedios.raiz, codigo)

        if remedio is not None:
          print(remedio)
        else:
          print( "\nNão foi identificado nenhum remedio com esse código ")

      
    def mudar_remedio(self):
        codigo = obrigatorio("\nCódigo do remedio - ")
        remedio = arvore_remedios.buscar(arvore_remedios.raiz, codigo)

        if remedio is None:
          print("\nNão foi identificado nenhum remedio com esse código ")
          return
          
        anterior = remedio.copy()
      
        nome = input("\nNovo nome (pressione Enter caso nao queira modificar o nome) -  ").strip()
        if nome != "": remedio["nome"] = nome
        validade = input("\nNovo prazo de validade (dd/mm/aaaa; Enter para manter) - ").strip()
        if validade != "":
            partes = validade.split("/")
            if (len(partes) == 3 and all(parte.isdigit() for parte in partes)
                    and len(partes[0]) == 2 and len(partes[1]) == 2
                    and len(partes[2]) == 4):
                remedio["validade"] = validade
            else:
                print("\nEssa data não é valida, a data de validade não foi alterada ")
        preco = input("\nNovo preço (R$ 12,50; Enter para manter) - ").strip()
        if preco != "":
            try:
                preco = float(preco.replace("R$", "").replace(",", "."))
                if preco >= 0:
                    remedio["preco"] = preco
                else:
                    print("\n Preço inválido, o preço não foi alterado ")
            except ValueError:
                print("Preço inválido, o preço não foi alterado ")
        mudancas.registrar({"tipo": "mudar_remedio", "codigo": codigo, "anterior": anterior})
        print("\nModificações realizadas com sucesso! ")


      
    def remover_remedio(self):
        codigo = obrigatorio("\nCódigo do remedio - ")
        remedio = arvore_remedios.buscar(arvore_remedios.raiz, codigo)

        if remedio is None:
          print("\nNão foi identificado nenhum remedio com esse código ")
          return

        removido = remedio.copy()
        arvore_remedios.remover(codigo)

        mudancas.registrar({
          "tipo": "remover_remedio",
          "codigo": codigo,
          "dados": removido
          
        })

        print("\nRemédio removido da sessão de cadastros ")

      
    def adicionar_fornecedor(self):
        codigo = obrigatorio("\nCódigo de identificação - ")
        if arvore_fornecedores.buscar(arvore_fornecedores.raiz, codigo) is not None:
          print("\n Já temos um fornecedor com esse codigo")
          return
          
        fornecedor = {"codigo": codigo, "nome": obrigatorio("Nome do fornecedor - "),
                      "telefone": obrigatorio("Telefone para contato (00-000000000) - ")}
        arvore_fornecedores.inserir(fornecedor)
        mudancas.registrar({"tipo": "adicionar_fornecedor", "dados": fornecedor.copy()})
        print("\nFornecedor adicionado a sessão de cadastros da ERP")

      
    def consultar_fornecedor(self):
        codigo = obrigatorio("\nCódigo fornecedor - ")
        fornecedor = arvore_fornecedores.buscar(arvore_fornecedores.raiz, codigo)
        if fornecedor is not None:
          print(fornecedor)

        else:
           print("\nNão foi identificador nenhum fornecedor com esse código ")
          
      
      
    def mudar_fornecedor(self):
        codigo = obrigatorio("\nCódigo do fornecedor - ")
        fornecedor = arvore_fornecedores.buscar(arvore_fornecedores.raiz, codigo)
        if fornecedor is None:
          print("\nNão foi identificado nenhum fornecedor com esse codigo")
          return
        
        anterior = fornecedor.copy()
        nome = input("Novo nome ( pressione Enter caso queira manter o mesmo nome) - ").strip()
        telefone = input("Novo telefone ( pressione Enter caso queira manter o numero atual  ) - ").strip()
        if nome != "": fornecedor["nome"] = nome
        if telefone != "": fornecedor["telefone"] = telefone
        mudancas.registrar({"tipo": "mudar_fornecedor", "codigo": codigo, "anterior": anterior})
        print("\nNovas mudanças feitas na sessão de fornecedores ")


      
    def remover_fornecedor(self):
        codigo = obrigatorio("\nCódigo do fornecedor - ")
        fornecedor = arvore_fornecedores.buscar(arvore_fornecedores.raiz, codigo)
        if fornecedor is None:
          print("\nNão foi identificado nenhum fornecedor com esse codigo")
          return
          
        removido = fornecedor.copy()
        arvore_fornecedores.remover(codigo)
        
        mudancas.registrar({"tipo": "remover_fornecedor", "codigo": codigo, "dados": removido})
        print("\nFornecedor removido da sessão de cadastros ")


      
class Estoque:
    def menu(self):
        while True:
            print("\n======================")
            print("      ESTOQUE ")
            print("======================")
            print(" 1 / Busca por prazo de validade")
            print(" 2 / Busca por valor ")
            print(" 3 / Busca por nome")
            print(" 4 / Busca pelo código")
            print(" 5 / Movimentar Lote")
            print(" 0 / Voltar ao menu principal da ERP ")
          
            opcao = input("\nSua escolha --> ")
          
            if opcao == "1":
              self.ordenar_validade()
            elif opcao == "2":
              self.ordenar_valor()
            elif opcao == "3":
              self.buscar_nome()
            elif opcao == "4":
              self.buscar_codigo()
            elif opcao == "5":
              self.movimentar()
            elif opcao == "0":
              break
            else: 
              print("\nOpção inválida ")

              
    def ordenar_validade(self):
        print("\nRemedios chegando no prazo da validade - ")

        lista = arvore_remedios.listar()
        for remedio in ordenar_geral(lista, "validade"):
          print(remedio)
        
        

          
    def ordenar_valor(self):
        lista = []
        for remedio in arvore_remedios.listar():
            copia = remedio.copy()
            copia["valor_estoque"] = copia["preco"] * copia["quantidade"]
            lista.append(copia)
        print("\nRemedios ordenados por valor no estoque - ")
        for remedio in ordenar_geral(lista, "valor_estoque", True):
            print(remedio)

          
    def movimentar(self):
        codigo = obrigatorio("Código - ")
        remedio = arvore_remedios.buscar(arvore_remedios.raiz, codigo)

        if remedio is None:
          print("\nNão foi encontrado nenhum remedio com esse código ")
          return
          
        
        tipo = input("1 Entrada / 2 Saída: ")
        quantidade = numero("Quantidade - ")
        anterior = remedio["quantidade"]
      
        if tipo == "1":
            remedio["quantidade"] += quantidade
            nome = "entrada"
        elif tipo == "2" and quantidade <= anterior:
            remedio["quantidade"] -= quantidade
            nome = "saida"
        else:
            print("\n Quantidade de movimentação invalida ou o estoque não possui o suficiente ")
            return
        mudanca = {"tipo": nome, "codigo": codigo,
                   "quantidade_anterior": anterior}
        mudancas.registrar(mudanca)
        print("\nA Movimentação foi registrada na ERP")

      
    def buscar_nome(self):
        nome = obrigatorio("Nome - ").lower()
        for remedio in arvore_remedios.listar():
          if nome in remedio["nome"].lower():
            print(remedio)
            

              
    def buscar_codigo(self):
        codigo = obrigatorio("Código - ")
        remedio = arvore_remedios.buscar(arvore_remedios.raiz, codigo)

        if remedio is not None:
          print(remedio)

        else:
          print("\nNão foi encontrado nenhum remedio com esse código ")
        
       

      
class Prioridade:
    def pedidos(self):
        while True:
            print("\n======================")
            print("     PRIORIDADE  ")
            print("======================")
            print("\n 1 / Adicionar pedido")
            print(" 2 / Exibir Fila")
            print(" 3 / Atender ")
            print(" 0 / Voltar ao menu principal da ERP")
          
        
            opcao = input("\nSua escolha --> ")
            if opcao == "1":
              self.adicionar()
            elif opcao == "2":
                for pedido in pedidos_reposicao: print(pedido)
            elif opcao == "3":
                if len(pedidos_reposicao) == 0:
                  print("Fila vazia.")
                else: 
                  print("Atendido:", pedidos_reposicao.pop(0))
            elif opcao == "0":
              break
              
              
    def adicionar(self):
        codigo = obrigatorio("\nCódigo do remédio - ")
        remedio = arvore_remedios.buscar(arvore_remedios.raiz, codigo)

        if remedio is None:
          print("\nNenhum remedio foi encontrado com esse código")
          return
          
        pedido = {"codigo": codigo, "nome": remedio["nome"],
                  "validade": remedio["validade"],
                  "criticidade": remedio["criticidade"]}
      
        pedidos_reposicao.append(pedido)
        pedidos_reposicao[:] = ordenar_geral(pedidos_reposicao, "validade")
        print("Pedido priorizado por validade. Criticidade:", pedido["criticidade"])


      
class Relatorios:
    def menu(self):
        while True:
            print("\n======================")
            print("   RELATÓRIOS   ")
            print("======================")
            print("\n 1 / Histórico de lotes")
            print(" 2 / Remover ultimo lançamento")
            print(" 3 / Em ordem")
            print(" 4 / pré ordem")
            print(" 5 / pós ordem")
            print(" 6 / calculo do desempenho")
            print(" 0 / Voltar ao menu principal da ERP")
       
            opcao = input("\nSua escolha --> ")
            if opcao == "1":
                for mudanca in movimentacoes: print(mudanca)
            elif opcao == "2":
                mudancas.desfazer()
            elif opcao == "3":
              lista = []
              arvore_remedios.listar_no(arvore_remedios.raiz, lista)

              for remedio in lista:
                print(remedio)

            elif opcao == "4":
              lista = []
              arvore_remedios.pre_ordem(arvore_remedios.raiz, lista)

              for remedio in lista:
                print(remedio)

            elif opcao == "5":
              lista = []
              arvore_remedios.pos_ordem(arvore_remedios.raiz, lista)

              for remedio in lista:
                print(remedio)

            elif opcao == "6":
              self.medir_desempenho_do_sistema()
              
            elif opcao == "0": 
              break

    def medir_desempenho_do_sistema(self):
      if arvore_remedios.raiz is None:
        print("\nNão foi realizado nenhum cadastrado, então não é possivel calcular o desempenho.")
        return
      
      
        
      codigo = obrigatorio("Código do remédio para medir a busca - ")
      
      resultado, media, desvio, contadores = repetir_o_calculo(lambda: arvore_remedios.buscar(arvore_remedios.raiz, codigo))
      
      print("\n--------------------------------------------")
      print("          Cálculo do nosso desempenho        ")
      print("--------------------------------------------")  
    
      print("\nresultado da busca:", resultado)
      print(f"tempo médio: {media * 1000:.4f} ms ")
      print(f"desvio padrão: {desvio * 1000:.4f} ms")
      print("Comparações:", contadores["comparacoes"])
      print("Trocas:", contadores["trocas"])
      print("Acessos:", contadores["acessos"])
      print("Operações:", contadores["operacoes"])   
   

    


cadastros = Cadastros()
estoque = Estoque()
prioridade = Prioridade()
relatorios = Relatorios()
mudancas = Mudancas()
arvore_remedios = ArvoreAVL()
arvore_fornecedores = ArvoreAVL()


def menu_erp_farmacia():
    while True:
        print("                            ==============================")
        print("                              ERP - FARMACIA PAGUE MAIS           ")
        print("                            ==============================")
        print("\n------------------------------------------------------------------------------------")
        print("\n 1 / Cadastros")
        print(" 2 / Estoque ")
        print(" 3 / Prioridade ")
        print(" 4 / Relatorios")
        print(" 5 / Mudanças ")
        print(" 0 / Sair ")
        print("\n------------------------------------------------------------------------------------")

      
        opcao = input("\nSua escolha -->   ")
        if opcao == "1":
            print("\n======================")
            print(" (1)  Remédios ")
            print("======================")
            print("\n======================")
            print(" (2) Fornecedores")
            print("======================") 
          
            escolha = input("\nSua escolha --> ")
            if escolha == "1": cadastros.remedios()
            elif escolha == "2": cadastros.fornecedores()
        elif opcao == "2":
          estoque.menu()
        elif opcao == "3":
          prioridade.pedidos()
        elif opcao == "4":
          relatorios.menu()
        elif opcao == "5":
          mudancas.desfazer()
        elif opcao == "0":
          print("\nSaindo da ERP..........")
          break
        else:
          print("\nOpção invalida!")
          
menu_erp_farmacia()