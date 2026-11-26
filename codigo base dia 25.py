import time
import statistics


remedios = []
fornecedores = []
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
    ocorrencias["operacoes"] += 1
    ocorrencias["acessos"] += 1
    item = lista[i]
    ocorrencias["acessos"] += 1
    valor_item = item[campo]
    ocorrencias["comparacoes"] += 1

    if valor_item == valor:
       return i
  return -1    
   
  
def ordenar(lista, campo, maior=False):
  nova_lista = []
  
  for item in lista:
    ocorrencias["operacoes"] += 1
    ocorrencias["acessos"] += 1
    nova_lista.append(item.copy()) 
  
  for i in range(len(nova_lista) - 1):
    ocorrencias["operacoes"] += 1
    posicao = 1

    for j in range(i + 1, len(nova_lista)):
      ocorrencias["operacoes"] += 1
      ocorrencias["acessos"] += 1
      valor_j = nova_lista[j][campo]
      ocorrencias["acessos"] += 1
      valor_posicao = nova_lista[posicao][campo]

      if campo == "validade":
        valor_j = data_ordenacao(valor_j)
        valor_posicao = data_ordenacao(valor_posicao)

      ocorrencias["comparacoes"] += 1

      if maior and valor_j > valor_posicao:
        posicao = j

      elif not maior and valor_j < valor_posicao:
        posicao = j

    if posicao != i:
      ocorrencias["trocas"] += 1
      nova_lista[i], nova_lista[posicao] = (nova_lista[posicao], nova_lista[i])

  return nova_lista
        

      

def calcular_o_desempenho(funcao):
  zerar_as_ocorrencias()
  
  comeco = time.perf_counter()
  resultado = funcao()
  fim = time.perf_counter()

  return resultado, fim - comeco, ocorrencias.copy()




def repetir_o_calculo(funcao, quantidade = 5):
  tempos = []
  resultado = None
  contadores = None

  for repeticao in range(quantidade):
    resultado, tempo, contadores = calcular_o_desempenho(funcao)
    tempos.append(tempo)
    

  media = statistics.mean(tempos)
  desvio = statistics.stdev(tempos)

  return resultado, media, desvio, contadores
  
  
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
            remedio = remedios[mudanca["posicao"]]
            remedio["quantidade"] = mudanca["quantidade_anterior"]
            print("\nO registro da ultima movimentação foi excluido")
          
        elif tipo == "adicionar_remedio":
            posicao = buscar(remedios, "codigo", mudanca["dados"]["codigo"])
            if posicao != -1:
                remedios.pop(posicao)
            print("\nO registro do ultimo cadastro de remedios foi excluido ")
          
        elif tipo == "remover_remedio":
            remedios.insert(mudanca["posicao"], mudanca["dados"])
            print("\nO registro do ultimo cadastro de remedios foi excluido ")
          
        elif tipo == "mudar_remedio":
            remedios[mudanca["posicao"]] = mudanca["anterior"]
            print("O registro da ultima alteração de remédio foi excluido ")
          
        elif tipo == "adicionar_fornecedor":
            posicao = buscar(fornecedores, "codigo", mudanca["dados"]["codigo"])
            if posicao != -1:
                fornecedores.pop(posicao)
            print("\nO registro do ultimo cadastro de fornecedores foi excluido ")
          
        elif tipo == "remover_fornecedor":
            fornecedores.insert(mudanca["posicao"], mudanca["dados"])
            print("\nO registro da ultima remoção de fornecedores foi excluida ")
          
        elif tipo == "mudar_fornecedor":
            fornecedores[mudanca["posicao"]] = mudanca["anterior"]
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
        if buscar(remedios, "codigo", codigo) != -1:
            print("\nJá temos um remédio cadastrado com esse código.")
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
        remedios.append(remedio)
        mudancas.registrar({"tipo": "adicionar_remedio", "dados": remedio.copy()})
        print("\nAdicionado à sessão de cadastros da ERP")

      
    def consultar_remedio(self):
        codigo = obrigatorio("\nCódigo do remedio -  ")
        posicao = buscar(remedios, "codigo", codigo)
        print(remedios[posicao] if posicao != -1 else "\nNão foi identificado nenhum remedio com esse código ")

      
    def mudar_remedio(self):
        codigo = obrigatorio("\nCódigo do remedio - ")
        posicao = buscar(remedios, "codigo", codigo)
        if posicao == -1:
            print("\nNão foi identificado nenhum remedio com esse código ")
            return
        anterior = remedios[posicao].copy()
        remedio = remedios[posicao]
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
        mudancas.registrar({"tipo": "mudar_remedio", "posicao": posicao, "anterior": anterior})
        print("\nModificações realizadas com sucesso! ")


      
    def remover_remedio(self):
        codigo = obrigatorio("\nCódigo do remedio - ")
        posicao = buscar(remedios, "codigo", codigo)
        if posicao == -1:
            print("\nNão foi identificado nenhum remedio com esse código ")
            return
        removido = remedios.pop(posicao)
        mudancas.registrar({"tipo": "remover_remedio", "posicao": posicao, "dados": removido})
        print("\nRemédio removido da sessão de cadastros ")

      
    def adicionar_fornecedor(self):
        codigo = obrigatorio("\nCódigo de identificação - ")
        if buscar(fornecedores, "codigo", codigo) != -1:
            print("\nJá temos um fornecedor identificado com esse código")
            return
        fornecedor = {"codigo": codigo, "nome": obrigatorio("Nome do fornecedor - "),
                      "telefone": obrigatorio("Telefone para contato (00-000000000) - ")}
        fornecedores.append(fornecedor)
        mudancas.registrar({"tipo": "adicionar_fornecedor", "dados": fornecedor.copy()})
        print("\nFornecedor adicionado a sessão de cadastros da ERP")

      
    def consultar_fornecedor(self):
        codigo = obrigatorio("\nCódigo fornecedor - ")
        posicao = buscar(fornecedores, "codigo", codigo)
        print(fornecedores[posicao] if posicao != -1 else "\nNão foi identificador nenhum fornecedor com esse código ")


      
    def mudar_fornecedor(self):
        codigo = obrigatorio("\nCódigo do fornecedor - ")
        posicao = buscar(fornecedores, "codigo", codigo)
        if posicao == -1:
            print("\nNão foi identificado nenhum fornecedor com esse código ")
            return
        anterior = fornecedores[posicao].copy()
        nome = input("Novo nome ( pressione Enter caso queira manter o mesmo nome) - ").strip()
        telefone = input("Novo telefone ( pressione Enter caso queira manter o numero atual  ) - ").strip()
        if nome != "": fornecedores[posicao]["nome"] = nome
        if telefone != "": fornecedores[posicao]["telefone"] = telefone
        mudancas.registrar({"tipo": "mudar_fornecedor", "posicao": posicao, "anterior": anterior})
        print("\nNovas mudanças feitas na sessão de fornecedores ")


      
    def remover_fornecedor(self):
        codigo = obrigatorio("\nCódigo do fornecedor - ")
        posicao = buscar(fornecedores, "codigo", codigo)
        if posicao == -1:
            print("\nNão foi identificado nenhum fornecedor com esse código ")
            return
        removido = fornecedores.pop(posicao)
        mudancas.registrar({"tipo": "remover_fornecedor", "posicao": posicao, "dados": removido})
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
        for remedio in ordenar(remedios, "validade"):
            print(remedio)
        

          
    def ordenar_valor(self):
        lista = []
        for remedio in remedios:
            copia = remedio.copy()
            copia["valor_estoque"] = copia["preco"] * copia["quantidade"]
            lista.append(copia)
        print("\nRemedios ordenados por valor no estoque - ")
        for remedio in ordenar(lista, "valor_estoque", True):
            print(remedio)

          
    def movimentar(self):
        codigo = obrigatorio("Código - ")
        posicao = buscar(remedios, "codigo", codigo)
        if posicao == -1:
            print("\nNão foi encontrado nenhum remedio com esse código ")
            return
        tipo = input("1 Entrada / 2 Saída: ")
        quantidade = numero("Quantidade - ")
        anterior = remedios[posicao]["quantidade"]
        if tipo == "1":
            remedios[posicao]["quantidade"] += quantidade
            nome = "entrada"
        elif tipo == "2" and quantidade <= anterior:
            remedios[posicao]["quantidade"] -= quantidade
            nome = "saida"
        else:
            print("\n Quantidade de movimentação invalida ou o estoque não possui o suficiente ")
            return
        mudanca = {"tipo": nome, "posicao": posicao,
                   "quantidade_anterior": anterior}
        mudancas.registrar(mudanca)
        print("\nA Movimentação foi registrada na ERP")

      
    def buscar_nome(self):
        nome = obrigatorio("Nome - ").lower()
        for remedio in remedios:
            if nome in remedio["nome"].lower(): print(remedio)

              
    def buscar_codigo(self):
        codigo = obrigatorio("Código - ")
        posicao = buscar(remedios, "codigo", codigo)
        print(remedios[posicao] if posicao != -1 else "\nNão foi encontrado nenhum remedio com esse código ")

      
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
        posicao = buscar(remedios, "codigo", codigo)
        if posicao == -1:
            print("\nNenhum remedio foi encontrado com esse código")
            return
          
        pedido = {"codigo": codigo, "nome": remedios[posicao]["nome"],
                  "validade": remedios[posicao]["validade"],
                  "criticidade": remedios[posicao]["criticidade"]}
      
        pedidos_reposicao.append(pedido)
        pedidos_reposicao[:] = ordenar(pedidos_reposicao, "validade")
        print("Pedido priorizado por validade. Criticidade:", pedido["criticidade"])


      
class Relatorios:
    def menu(self):
        while True:
            print("\n======================")
            print("   RELATÓRIOS   ")
            print("======================")
            print("\n 1 / Histórico dos lotes")
            print(" 2 / Remover o ultimo lançamento")
            print(" 3 / Calcular o nosso desempenho")
            print(" 0 / Voltar ao menu principal da ERP")
       
            opcao = input("\nSua escolha --> ")

          
            if opcao == "1":
                for mudanca in movimentacoes: print(mudanca)
                  
            elif opcao == "2":
                mudancas.desfazer()

            elif opcao == "3":
               self.calcular_o_desempenho()
              
              
            elif opcao == "0": 
              break

    def calcular_o_desempenho(self):
      if not remedios:
        print("\nNão foi realizado nenhum cadastrado, então não é possivel calcular o desempenho.")
        return

      codigo = obrigatorio("Digite o código do remédio para que a busca seja feita: ")

      
      print("\n--------------------------------------------")
      print("          Cálculo do nosso desempenho        ")
      print("--------------------------------------------")  
      posicao, media, desvio, contadores = repetir_o_calculo(lambda: buscar(remedios, "codigo", codigo))
      if posicao != -1:
        print("\nResultado da busca:", remedios[posicao])
        print("\nPosição da busca:", posicao)
        
      print(f"tempo médio : {media * 1000:.4f} ms" )
      print(f"desvio padrão : {desvio * 1000:.4f} ms ")
      print("total de comparações : ", contadores["comparacoes"])
      print("total de trocas : ", contadores["trocas"])
      print("total de acessos : ", contadores["acessos"])
      print("total de perações : ", contadores["operacoes"]) 


             
cadastros = Cadastros()
estoque = Estoque()
prioridade = Prioridade()
relatorios = Relatorios()
mudancas = Mudancas()

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