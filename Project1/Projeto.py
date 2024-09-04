'''
Autora: Maria Medvedeva 
Nº ist1106120
Resolução do primeiro projeto de Fundamentos de Programação
'''


def limpa_texto(cad_caracteres):
    ''' 
    limpa_texto: cad_caracteres -> cad_caracteres
    Esta função recebe uma cadeia de carateres qualquer e devolve a cadeia de carateres
    limpa que corresponde à remoção de carateres brancos conforme descrito.
    '''
    return " ".join(cad_caracteres.split())

def corta_texto(cad_caracteres,largura):
    '''
    corta_texto: cad_caracteres,num -> cad_carateres,cad_caracteres
    Esta função devolve duas subcadeias de carateres limpas: a primeira contendo 
    todas as palavras completas desde o início da cadeia original até um 
    comprimento máximo total igual à largura fornecida, e a segunda cadeia 
    contendo o resto do texto de entrada.

    Corrigido com a proposta do Professor da cadeira.
    '''

    if len(cad_caracteres) <= largura:
        return cad_caracteres, ''
    else:
        while cad_caracteres[largura] != ' ' and largura > 0:
            largura -= 1
        if largura == 0:
            raise ValueError("corta_texto: argumentos invalidos")
        return cad_caracteres[:largura], cad_caracteres[largura+1:]
     
def insere_espacos(cad_caracteres,larg_coluna):
    '''
    insere espacos: cad_carateres, num -> cad_carateres
    Esta função devolve uma cadeia de carateres de comprimento igual à 
    largura da coluna formada pela cadeia original com espaços entre palavras.

    Corrigido com a proposta do Professor da cadeira.
    '''
    if cad_caracteres.find(' ') == -1:
        if len(cad_caracteres) > larg_coluna:
            raise ValueError("insere_espacos: argumentos invalidos")
        return cad_caracteres + ' '* (larg_coluna - len(cad_caracteres))
    index = 0
    while len(cad_caracteres) != larg_coluna:
        index = cad_caracteres.find(' ', index)
        if index == -1:
            index = 0
        else:
            cad_caracteres = cad_caracteres[:index] + ' ' + cad_caracteres[index:] 
            while cad_caracteres[index] == ' ':
                index += 1
    return cad_caracteres

def justifica_texto(cad_caracteres, largura_coluna=80):
    '''
    justifica_texto: cad_carateres, num → tuplo
    Esta função devolve um tuplo de cadeias de carateres justificadas,
    isto é, de comprimento igual à largura da coluna com espaços 
    entre palavras conforme descrito.

    Corrigido com a proposta do Professor da cadeira.
    '''
    if type(cad_caracteres) is not str or len(cad_caracteres) == 0 or type(largura_coluna) != int or largura_coluna <= 0:
        raise ValueError('justifica_texto: argumentos invalidos')

    cad_caracteres = limpa_texto(cad_caracteres)

    for w in cad_caracteres.split(' '):
        if len(w) > largura_coluna:
            raise ValueError('justifica_texto: argumentos invalidos')

    # just_text = ''
    tuplo = ()
    while cad_caracteres:
        seg, cad_caracteres = corta_texto(cad_caracteres, largura_coluna)

        if cad_caracteres:
            tuplo += (insere_espacos(seg, largura_coluna),)
        else:
            tuplo += (seg + ' '*(largura_coluna - len(seg)),)
    return tuplo 

def calcula_quocientes(dicionario,num_dep):
    '''
    calcula_quociente: dicionario x num --> dicionario
    Devolve o dicionário com as mesmas chaves do dicionário 
    argumento (correspondente a partidos) contendo a lista 
    (de comprimento igual ao número de deputados) com os quocientes
    calculados com o método de Hondt ordenados em ordem decrescente.
    '''
    dicionario_copia = {}
    
    for partido, votos in dicionario.items():
        quocientes = []
        for i in range(1, num_dep + 1):
            quociente = votos / i
            quocientes.append(quociente)
        dicionario_copia[partido] = quocientes
    
    return dicionario_copia

def atribui_mandatos(dicionario,deputados):
    '''
    atribui_mandatos: dicionario x deputados --> lista
    Devolve a lista ordenada de tamanho igual ao
    número de deputados contendo as cadeias de carateres dos 
    partidos que obtiveram cada mandato
    '''

    quocientes = calcula_quocientes(dicionario, deputados)
    mandatos = []
    
    # Para acompanhar quantos mandatos cada partido já recebeu
    mandatos_por_partido = {partido: 0 for partido in dicionario}
    
    for _ in range(deputados):
        # Encontrar o partido com o maior quociente atual
        max_quociente = -1
        partido_escolhido = None
        
        for partido, lista_quocientes in quocientes.items():
            if lista_quocientes:
                quociente_atual = lista_quocientes[0]
                if (quociente_atual > max_quociente) or (
                    quociente_atual == max_quociente and mandatos_por_partido[partido] < mandatos_por_partido[partido_escolhido]):
                    max_quociente = quociente_atual
                    partido_escolhido = partido
        
        # Atribuir o mandato ao partido escolhido
        mandatos.append(partido_escolhido)
        mandatos_por_partido[partido_escolhido] += 1
        
        # Remover o quociente usado do partido escolhido
        quocientes[partido_escolhido].pop(0)
    
    return mandatos

def obtem_partidos(dicionario):
    '''
    obtem_partidos:dicionario --> lista
    devolve a lista por ordem alfabética com o nome 
    de todos os partidos que participaram nas eleições
    '''
    dic_copy = dicionario.copy()
    lista = []
    for chave in dic_copy:
        for el in dic_copy[chave]:
            if el == "votos":
                for partido in dic_copy[chave][el]:
                   lista = lista +[partido,]
    
    def eli_repeticao(lista):
        # Usa um conjunto para remover duplicados
        lista_unica = list(set(lista))
        lista_unica.sort()
        
        return lista_unica

      
    return eli_repeticao(lista)

def obtem_resultado_eleicoes(dicionario):
    '''
    obtem_resultados_eleicoes: dicionario --> lista
    devolve uma lista ordenada com os resultados das eleições
    (nome partido, nº de deputados, nº de votos)
    '''
    if type(dicionario) != dict or dicionario == {}:
        raise ValueError("obtem_resultado_eleicoes: argumento invalido")
    for elementos in dicionario:
        if type(dicionario[elementos]) != dict or \
            type(elementos) != str or elementos == "" or \
            len(dicionario[elementos]) > 2:
            raise ValueError("obtem_resultado_eleicoes: argumento invalido")
        if not( 'votos' in dicionario[elementos] and  \
            'deputados' in dicionario[elementos] and \
            type(dicionario[elementos]['votos']) == dict and \
            type(dicionario[elementos]['deputados']) == int and \
            dicionario[elementos]['deputados'] >= 0 and \
            dicionario[elementos]['votos'] != {}):
            raise ValueError("obtem_resultado_eleicoes: argumento invalido")
    
        for el in dicionario[elementos]['votos']:
            if type(el) != str:
                raise ValueError("obtem_resultado_eleicoes: argumento invalido")
            valor = dicionario[elementos]['votos'][el]
            if not isinstance(valor, int):
                raise ValueError("obtem_resultado_eleicoes: argumento invalido")
            if valor < 0:
                raise ValueError("obtem_resultado_eleicoes: argumento invalido")
            
    dic_copia = dicionario.copy()
    lista = []  
    resultados_partidos = {}

    for partido in obtem_partidos(dicionario):
        resultados_partidos[partido] = [0, 0]  

    for circulo in dic_copia:
        mandatos = atribui_mandatos(dic_copia[circulo]['votos'], dic_copia[circulo]['deputados'])
        
        for partido in dic_copia[circulo]['votos']:
            votos = dic_copia[circulo]['votos'][partido]
            resultados_partidos[partido][1] += votos  # Acumular os votos totais
        
        for partido in mandatos:
            resultados_partidos[partido][0] += 1  # Acumular o nº de deputados

    for partido, resultado in resultados_partidos.items():
        lista.append((partido, resultado[0], resultado[1]))

    # Ordenar a lista primeiro por nº de deputados (decrescente) e depois por nº de votos (decrescente)
    lista.sort(key=lambda x: (-x[1], -x[2]))

    return lista



def produto_interno(vetor1,vetor2): 
    '''
    produto_interno: tuplo1 ,tuplo2 -> real
    Esta função recebe dois tuplos de números (inteiros ou reais) 
    representando dois vetores e retorna o resultado do produto 
    interno desses dois vetores.
    '''
    soma = 0
    for i in range(len((vetor1))):
        soma = soma + (vetor1[i] * vetor2[i])
    return float(soma)

def verifica_convergencia(matriz,constantes,variavel_x,precisao):
    '''
    verifica_convergencia:
    matriz x  constantes x variavel_x x precisao --> booleano
    Deve retornar  True caso o valor absoluto do
    erro de todas as equações seja inferior à precisão,
    |fi(x) - ci| < ϵ, e False caso contrário
    '''
    num_equacoes = len(matriz)
    
    for i in range(num_equacoes):
        soma = 0
        # Calcula a soma para a i-ésima equação
        for j in range(len(matriz[i])):
            soma += matriz[i][j] * variavel_x[j]
        
        # Verifica o erro absoluto
        erro = abs(soma - constantes[i])
        
        if erro >= precisao:
            return False
    
    return True

def retira_zeros_diagonal(matriz,c):
    '''
    retira_zeros_diagonal: matriz x c --> tuplo x tuplo
    devolve uma nova matriz com as mesmas linhas que a de
    entrada, mas com estas reordenadas de forma a não 
    existirem valores 0 na diagonal. O segundo parâmetro 
    de saída é também o vetor de entrada com a mesma reordenação de
    linhas que a aplicada à matriz.
    '''
    lista_1 = list(matriz)
    lista_2 = list(c)
    for diagonal in range(len(lista_1)):
        if lista_1[diagonal][diagonal] == 0:
            for coluna in range(len(lista_1)):
                if lista_1[diagonal][coluna] != 0 and lista_1[coluna][diagonal]:
                    lista_1[diagonal],lista_1[coluna] = \
                    lista_1[coluna],lista_1[diagonal]

                    lista_2[diagonal],lista_2[coluna] = \
                    lista_2[coluna],lista_2[diagonal]
                    break
    

    return tuple(lista_1),tuple(lista_2)

def eh_diagonal_dominante(matriz):
    '''
    eh_diagonal_dominante:tuplo --> booleano
    Retorna True caso seja uma matriz diagonalmente dominante,
    e False caso contrário.
    '''
    for i in range(len(matriz)):
        sum_off_diagonal = 0
        for j in range(len(matriz[i])):
            if j != i:
                sum_off_diagonal += abs(matriz[i][j])
        if abs(matriz[i][i]) < sum_off_diagonal:
            return False
    return True
    
def resolve_sistema(matriz,constantes,precisao):
    '''
    resolve_sistema: matriz x constantes x precisao --> tuplo
    Devolve um tuplo que é a solução do sistema de equações 
    de entrada aplicando o método de Jacobi.

    Parte final, parcialmente corrigida com a proposta do Professor da cadeira.
    '''
    if not (isinstance(matriz, tuple) and len(matriz) >= 1 and \
        all((isinstance(t, tuple) and len(t) == len(matriz)) for t in matriz) and \
        all(isinstance(x, (int,float)) for t in matriz for x in t)):
        raise ValueError("resolve_sistema: argumentos invalidos")
    
    if not (isinstance(constantes, tuple) and len(constantes) >= 1 and \
        all(isinstance(x, (int,float)) for x in constantes) and \
        len(constantes) <= len(matriz)):
        raise ValueError("resolve_sistema: argumentos invalidos")
    
    if not (type(precisao) == float and precisao > 0):
        raise ValueError("resolve_sistema: argumentos invalidos")
    
    for linhas in range(len(matriz)):
        if not type(matriz[linhas]) == tuple:
            raise ValueError("resolve_sistema: argumentos invalidos")
        for valor in range(len(matriz[linhas])):
            if not (type(matriz[linhas][valor]) == int or \
                type(matriz[linhas][valor]) == float):
                raise ValueError("resolve_sistema: argumentos invalidos")
    
    
    matriz,constantes = retira_zeros_diagonal(matriz,constantes)
    variavel_x = (0,) * len(constantes)

    if not eh_diagonal_dominante(matriz):
            raise ValueError("resolve_sistema: matriz nao diagonal dominante")
    
    while not verifica_convergencia(matriz,constantes, variavel_x,precisao):
        variavel_x_nova = ()
        for linha in range(len(constantes)):
            variavel_x_nova += (variavel_x[linha] + (constantes[linha] - \
            produto_interno(matriz[linha], variavel_x))/ matriz[linha][linha],)
        variavel_x = variavel_x_nova[:]
    
    return variavel_x