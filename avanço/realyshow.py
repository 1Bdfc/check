import json
import random



def carregar_perguntas():
    with open("./perguntas.json", "r", encoding="utf-8") as arq:
        arquivo = json.load(arq)



def selecionar_por_dificuldade(perguntas, nivel):
    perguntas_filtradas = []  # Cria uma lista vazia para guardar as perguntas filtradas
    for questao in perguntas:  # Percorre cada pergunta na lista de perguntas
        if (questao["dificuldade"] == nivel):  # Verifica se a dificuldade da pergunta é igual ao nível desejado
            perguntas_filtradas.append(questao)  # Adiciona a pergunta à lista de perguntas filtradas

def embaralhar_alternativas(alternativas, letra_correta):
    lista_inicial = []
    for opcao in alternativas:
        letra = opcao[0].lower() #Pega a primeira letra da opcao e a converte para minúscula.
        texto = opcao[3:].strip() #Pega a parte da string a partir do quarto caractere (índice 3) e remove espaços em branco extras do início e do final do texto.
        lista_inicial.append({"letra": letra, "texto": texto})

    texto_correto = "" #Essa variável armazenará o texto da alternativa correta.

    for opcao in lista_inicial:
        if (opcao["letra"] == letra_correta.lower()): #Verifica se a letra da alternativa atual é igual à alternativa correta.
            texto_correto = opcao["texto"] #Se a letra corresponder, armazena o texto dessa alternativa
            break

    random.shuffle(lista_inicial)

    letras_novas = ['a', 'b', 'c', 'd']
    alternativas_finais = []
    nova_letra_correta = ''

    for i in range(len(lista_inicial)):
        alt_texto = lista_inicial[i]["texto"] #Obtém o texto da alternativa na posição i.
        nova_letra = letras_novas[i] #Nova letra para essa alternativa da lista letras_novas.
        alternativas_finais.append(f"{nova_letra}) {alt_texto}")

        if (alt_texto == texto_correto): #Verificação do texto da alternativa atual
            nova_letra_correta = nova_letra

    return alternativas_finais, nova_letra_correta

def mostrar_pergunta(pergunta, numero):
    print(f"\nPergunta {numero}: {pergunta['texto']}") # f-string (formatação de string literal) 
    for op in pergunta['alternativas']: 
        print(op)

def usar_pulo(pulos_restantes):
    if (pulos_restantes > 0):
        pulos_restantes -= 1
        print("Você pulou está pergunta.")
        return True, pulos_restantes
    else:
        print("Você não tem mais pulos disponíveis.")
        return False, pulos_restantes

def usar_cartas(alternativas, correta, cartas_usadas):
    if cartas_usadas:
        print("Você já utilizou a ajuda das cartas.")
        return alternativas, cartas_usadas

    num_remover = random.randint(1, 4) # gera um número inteiro aleatório dentro de um intervalo que você escolher.

    # Criar uma lista das alternativas incorretas
    incorretas = []
    for opcoes in alternativas:
        letra = opcoes[0].lower()
        if (letra != correta.lower()):
            incorretas.append(opcoes)

    # Ajusta para não remover mais do que existe
    if (num_remover > len(incorretas)):
        num_remover = len(incorretas)

    # Embaralha as incorretas
    for i in range(len(incorretas) - 1, 0, -1):
        x = random.randint(0, i) #random.randint --- Gera um número inteiro aleatório dentro do intervalo.
        incorretas[i], incorretas[x] = incorretas[x], incorretas[i]

    # Pega as alternativas para remover
    removidas = []
    for i in range(num_remover):
        removidas.append(incorretas[i])

    # Criação da lista final sem as removidas
    restantes = []
    for opcoes in alternativas:
        if (opcoes not in removidas): # not in --- verifica se um valor NÃO está dentro de uma coleção
            restantes.append(opcoes) 

    print(f"A carta eliminou {num_remover} alternativa(s) incorreta(s).")

    return restantes, True

def verificar_resposta(resposta, correta):
    if (resposta.lower() == correta.lower()):
        return True
    else:
        return False

def controle_pontuacao(numero_pergunta):
    if (numero_pergunta <= 3):
        return 1000
    elif (numero_pergunta == 4):
        return 2000
    elif (numero_pergunta == 5):
        return 5000
    elif (numero_pergunta <= 9):
        return 10000
    elif (numero_pergunta <= 12):
        return 50000
    elif (numero_pergunta == 13):
        return 100000
    elif (numero_pergunta == 14):
        return 200000
    elif (numero_pergunta == 15):
        return 500000
    else:
        return 0



def iniciar_jogo():
    todas = carregar_perguntas() # Carrega todas as perguntas do arquivo
    perguntas_faceis = selecionar_por_dificuldade(todas, "facil", 5) # Separa as perguntas por nível de dificuldade
    perguntas_medias = selecionar_por_dificuldade(todas, "medio", 5)
    perguntas_dificeis = selecionar_por_dificuldade(todas, "dificil", 5)

    perguntas = perguntas_faceis + perguntas_medias + perguntas_dificeis 

    pontuacao = 0
    pulos_restantes = 3
    usou_cartas = False

    for i in range(len(perguntas)+1): # Laço das perguntas
        pergunta_atual = perguntas[i]

        # Embaralha as alternativas --- função criada anteriormente
        alternativas, correta = embaralhar_alternativas(pergunta_atual["alternativas"], pergunta_atual["correta"])
        print(f"\n Pergunta {i + 1} ")
        mostrar_pergunta({"texto": pergunta_atual["texto"], "alternativas": alternativas}, i + 1) #função criada anteriormente

        print("\nDeseja usar alguma ajuda?")
        print(f"1 - Cartas | 2 - Pular ({pulos_restantes} disponíveis) | Enter - Responder")
        escolha = input("Opção: ")

        if (escolha == "2"):
            pulou, pulos_restantes = usar_pulo(pulos_restantes)
            if (pulou == True):
                continue

        elif (escolha == "1"):
            if (usou_cartas == False):
                alternativas, usou_cartas = usar_cartas(alternativas, correta, usou_cartas)
                mostrar_pergunta({"texto": pergunta_atual["texto"], "alternativas": alternativas}, i + 1)
            else:
                print("Você já usou a ajuda das cartas.")

        resposta = input("Digite sua resposta (a/b/c/d): ")

        if verificar_resposta(resposta, correta): #Verifica se acertou pela função criada anteriormente 
            premio = controle_pontuacao(i + 1) 
            pontuacao += premio
            print(f"Certa resposta! Você acumulou R$ {pontuacao}.")
        else:
            if (i > 0):
             perda = controle_pontuacao(i) // 2
            else:
             perda = 0
             print("Resposta errada! Você perdeu o jogo.")
             print(f"Prêmio final: R$ {perda}.")
             return
            
    print(f"\nParabéns! Você venceu o Show do Milhão com o prêmio total de R$ {pontuacao}!")

if __name__ == "__main__": #Só executa o jogo se esse arquivo for o principal
    iniciar_jogo()