#TAD_GERADOR
#Construtores
def cria_gerador(b,s):
    '''
    cria_gerador: int x int --> lista
    Esta função recebe o número de bits e a seed e devolve a o gerador
    correspondente.
    '''
    if not (type(b) == int and type(s) == int and\
        (b == 32 or b == 64) and s > 0 and \
        s <= ((2** b)-1)):
        #estado inferior ao tamanho que esse estado permite representar
        raise ValueError("cria_gerador: argumentos invalidos")
    
    return [b,s]
       
def cria_copia_gerador(g):
    '''
    cria_gerador_copia: lista --> lista
    Devolve uma cópia nova do gerador.
    '''
    return g[:]

#Seletores

def obtem_estado(g):
    '''
    obtem_estado: lista --> int
    Devolve o estado atual do gerador sem o alterar.
    '''
    if eh_gerador(cria_copia_gerador(g)):
        return g[1]

#Modificadores

def define_estado(g,s):
    '''
    define_estado: lista x int --> int 
    Devolve o novo valor do estado do gerador g.
    '''
    g[1] = s
    return g[1]

def atualiza_estado(g):
    '''
    atualiza_estado: lista --> int
    Devolve o estado atualizado do gerador g.
    '''
    if g[0] == 32:
        g[1] ^= (g[1] << 13) & 0xFFFFFFFF
        g[1] ^= (g[1] >> 17) & 0xFFFFFFFF
        g[1] ^= (g[1] << 5) & 0xFFFFFFFF
    else:
        g[1] ^= (g[1] << 13) &  0xFFFFFFFFFFFFFFFF
        g[1] ^= (g[1] >> 7) &  0xFFFFFFFFFFFFFFFF
        g[1] ^= (g[1] << 17) &  0xFFFFFFFFFFFFFFFF
    define_estado(g,g[1])
    return g[1]

#Reconhecedor

def eh_gerador(arg):
    '''
    eh_gerador: universal --> bool
    Devolve True caso o seu argumento seja um TAD gerador e
    False caso contrário.
    '''
    return type(arg) == list and len(arg) == 2 and \
        type(arg[0]) == int and type(arg[1]) == int and \
        (arg[0] == 32 or arg[0] == 64) and arg[1] > 0 and \
        arg[1] <= (2**arg[0]) 
        #estado inferior ao tamanho que esse estado permite representar

#Teste

def geradores_iguais(g1,g2):
    '''
    geradores_iguais: lista x lista --> bool
    Devolve True apenas se os argumentos são geradores e são
    iguais.
    '''
    return eh_gerador(g1) and eh_gerador(g2) and \
        g1[0] == g2[0] and g1[1] == g2[1]

#Transformador
def gerador_para_str(g):
    '''
    gerador_para_str: lista --> str
    Devolve a cadeia de carateres que representa o seu argumento.
    '''
    string_g = "xorshift" + str(g[0]) + "(s=" + str(g[1]) + ")"
    return string_g

#Funções de alto nível

def mod(num1, num2): #Função auxiliar
        return num1 % num2

def gera_numero_aleatorio(g,n):
    '''
    gera_numero_aleatorio: lista x int --> int
    Devolve um número aleatório no intervalo [1, n]
    obtido a partir do novo estado do gerador como 1 + mod(s,n)
    '''
    #s = atualiza_estado(g)
    numero_aleatorio = 1 + mod(atualiza_estado(g),n)
    if 1 <= numero_aleatorio <= n:
        return numero_aleatorio

def gera_carater_aleatorio(g,c):
    '''
    gera_caracter_aleatorio: lista x str --> str
    Devolve um caráter aleatório no intervalo entre 
    'A' e o caráter maiúsculo dado.
    '''
    s = atualiza_estado(g)
    letra_maiuscula = c.capitalize()
    caracteres = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    car = list(caracteres)
    l = len(car[: ord(letra_maiuscula) - ord('A')+1])
                #slicing até ao carater pretendido
    return chr(ord('A') + mod(s,l))

#TAD_COORDENADA
#Construtor

def cria_coordenada(col,lin):
    '''
    cria_coordenada: str x int --> tuplo
    Recebe os valores correspondentes à coluna e
    linha e devolve a coordenada correspondente.
    '''
    if not (type(col) == str and type(lin) == int and\
        col >= 'A' and col <= 'Z' and 1 <= lin <= 99 and \
        len(col) == 1):
        raise ValueError("cria_coordenada: argumentos invalidos")
    
    return (col,lin)

#Seletores

def obtem_coluna(c):
    '''
    obtem_coluna: tuplo --> str
    Devolve a coluna da coordenada.
    '''
    if eh_coordenada(c):
        return c[0]

def obtem_linha(c):
    '''
    obtem_linha: tuplo --> int
    Devolve a linha da coordenada.
    '''
    if eh_coordenada(c):
        return c[1]

#Reconhecedor

def eh_coordenada(arg):
    '''
    eh_coordenada: universal --> bool
    Devolve True caso o seu argumento seja um TAD coordenada 
    e False caso contrário.
    '''
    return type(arg) == tuple and len(arg) == 2 and \
        type(arg[0]) == str and type(arg[1]) == int and \
        'A' <= arg[0] <= 'Z' and 1 <= arg[1] <= 99 and \
        len(arg[0]) == 1

#Teste

def coordenadas_iguais(c1,c2):
    '''
    coordenadas_iguais: tuplo x tuplo --> bool
    Devolve True apenas se os argumentos são coordenadas e
    são iguais.
    '''
    return eh_coordenada(c1) and eh_coordenada(c2) and \
        c1[0] == c2[0] and c1[1] == c2[1]

#Transformador

def coordenada_para_str(c):
    '''
    coordenada_para_str: tuplo --> str
    Devolve a cadeia de carateres que representa o seu
    argumento.
    '''
    return '{:s}{:02d}'.format(c[0], c[1])


def str_para_coordenada(s):
    '''
    str_para_coordenada: str --> tuplo
    Devolve a coordenada reapresentada pelo seu argumento.
    '''
    s1 = list(s)
    if len(s1) == 3 and type(s1[0]) == str and \
        type(s1[1]) == int and type(s1[2]) == int and s1[1] == '0':
        return (s1[0], s1[2])
    else:
        return (s1[0], int(s1[1] + s1[2]))

#Funções de alto nível

def obtem_coordenadas_vizinhas(c):
    '''
    obtem_coordenadas_vizinhas: tuplo --> tuplo
    Devolve um tuplo com as coordenadas vizinhas à coordenada, começando 
    pela coordenada na diagonal acima-esquerda e seguindo 
    no sentido horário.
    '''
    #viz_1 = 3 coordenadas vizinhas da linha cima
    #viz_2 = 2 coordenadas vizinhas: à direita da coordenada pedida,
        # e a coordenada abaixo desta.
    #viz_3 = 3 coordenadas vizinhas: as duas restantes da linha abaixo e 
    #a coordenada à esqueda da indicada
    if obtem_coluna(c) == 'A' and obtem_linha(c) != 1 and obtem_linha(c) != 99:
        viz_1 = (cria_coordenada(obtem_coluna(c),obtem_linha(c) -1),\
        cria_coordenada(chr(ord(obtem_coluna(c)) + 1),obtem_linha(c) -1))
         
        viz_2 = (cria_coordenada(chr(ord(obtem_coluna(c)) + 1),obtem_linha(c)),\
        cria_coordenada(chr(ord(obtem_coluna(c)) + 1),obtem_linha(c) + 1))
        
        viz_3 = [(cria_coordenada(obtem_coluna(c),obtem_linha(c) +1))]
        return viz_1 + viz_2 + tuple(viz_3)

    elif obtem_coluna(c) == 'Z'and obtem_linha(c) != 1 and obtem_linha(c) != 99:
        viz_1 = (cria_coordenada(chr(ord(obtem_coluna(c)) - 1),obtem_linha(c) -1),\
        cria_coordenada(obtem_coluna(c),obtem_linha(c) -1))

        viz_3 = (cria_coordenada(obtem_coluna(c),obtem_linha(c) +1),\
        cria_coordenada(chr(ord(obtem_coluna(c)) - 1),obtem_linha(c) +1),\
        cria_coordenada(chr(ord(obtem_coluna(c)) - 1),obtem_linha(c)))
        
        return viz_1 + viz_3

    elif obtem_linha(c) == 1 and obtem_coluna(c) != 'A' and obtem_coluna(c) != 'Z':
        viz_2 = (cria_coordenada(chr(ord(obtem_coluna(c)) + 1),obtem_linha(c)),\
        cria_coordenada(chr(ord(obtem_coluna(c)) + 1),obtem_linha(c) + 1))

        viz_3 = (cria_coordenada(obtem_coluna(c),obtem_linha(c) +1),\
        cria_coordenada(chr(ord(obtem_coluna(c)) - 1),obtem_linha(c) +1),\
        cria_coordenada(chr(ord(obtem_coluna(c)) - 1),obtem_linha(c)))
        return viz_2 + viz_3

    elif obtem_linha(c) == 99 and obtem_coluna(c) != 'A' and obtem_coluna(c) != 'Z':
        viz_1 = (cria_coordenada(chr(ord(obtem_coluna(c)) - 1),obtem_linha(c) -1),\
        cria_coordenada(obtem_coluna(c),obtem_linha(c) -1),\
        cria_coordenada(chr(ord(obtem_coluna(c)) + 1),obtem_linha(c) -1))

        viz_2 = [(cria_coordenada(chr(ord(obtem_coluna(c)) + 1),obtem_linha(c)))]

        viz_3 = [((cria_coordenada(chr(ord(obtem_coluna(c)) - 1),obtem_linha(c))))]
        return viz_1 + tuple(viz_2) + tuple(viz_3)
        
    elif obtem_coluna(c) == 'A' and obtem_linha(c) == 1:
        viz_2 = (cria_coordenada(chr(ord(obtem_coluna(c)) + 1),obtem_linha(c)),\
        cria_coordenada(chr(ord(obtem_coluna(c)) + 1),obtem_linha(c) + 1))

        viz_3 = [(cria_coordenada(obtem_coluna(c),obtem_linha(c) +1))]
        
        return viz_2 + tuple(viz_3)

    elif obtem_coluna(c) == 'A' and obtem_linha(c) == 99:
        viz_1 = (cria_coordenada(obtem_coluna(c),obtem_linha(c) -1),\
        cria_coordenada(chr(ord(obtem_coluna(c)) + 1),obtem_linha(c) -1))

        viz_2 = [(cria_coordenada(chr(ord(obtem_coluna(c)) + 1),obtem_linha(c)))]            
        return viz_1 + tuple(viz_2)
        
    elif obtem_coluna(c) == 'Z' and obtem_linha(c) == 1:
        viz_3 = (cria_coordenada(obtem_coluna(c),obtem_linha(c) +1),\
        cria_coordenada(chr(ord(obtem_coluna(c)) - 1),obtem_linha(c) +1),\
        cria_coordenada(chr(ord(obtem_coluna(c)) - 1),obtem_linha(c)))
        return viz_3
        
    elif obtem_coluna(c) == 'Z' and obtem_linha(c) == 99:
        viz_1 = (cria_coordenada(chr(ord(obtem_coluna(c)) - 1),obtem_linha(c) -1),\
        cria_coordenada(obtem_coluna(c),obtem_linha(c) -1))

        viz_3 = [(cria_coordenada(chr(ord(obtem_coluna(c)) - 1),obtem_linha(c)))]
        return viz_1 + tuple(viz_3)

    else:
        viz_1 = (cria_coordenada(chr(ord(obtem_coluna(c)) - 1),obtem_linha(c) -1),\
        cria_coordenada(obtem_coluna(c),obtem_linha(c) -1),\
        cria_coordenada(chr(ord(obtem_coluna(c)) + 1),obtem_linha(c) -1))

        viz_2 = (cria_coordenada(chr(ord(obtem_coluna(c)) + 1),obtem_linha(c)),\
        cria_coordenada(chr(ord(obtem_coluna(c)) + 1),obtem_linha(c) + 1))

        viz_3 = (cria_coordenada(obtem_coluna(c),obtem_linha(c) +1),\
        cria_coordenada(chr(ord(obtem_coluna(c)) - 1),obtem_linha(c) +1),\
        cria_coordenada(chr(ord(obtem_coluna(c)) - 1),obtem_linha(c)))
        return viz_1 + viz_2 + viz_3

def obtem_coordenada_aleatoria(c,g):
    '''
    obtem_coordenada_aleatorio: tuplo x lista --> tuplo
    Devolve uma coordenada gerada aleatoriamente.
    '''
    col = gera_carater_aleatorio(g,obtem_coluna(c))
    lin = gera_numero_aleatorio(g,obtem_linha(c))
    return (col,lin)

#TAD_PARCELA
#Construtores

def cria_parcela():
    '''
    cria_parcela: {} --> lista
    Devolve uma parcela tapada sem mina escondida.
    '''
    p = {'estado': '#', 'tem_minas': False}
    return p

def cria_copia_parcela(p):
    '''
    cria_copia_parcela: lista --> lista
    Devolve uma nova cópia da parcela.
    '''
    # Corrigido com a proposta do Professor da cadeira
    return {'estado': p['estado'], 'tem_minas': p['tem_minas']}


#Modificadores

def limpa_parcela(p):
    '''
    limpa_parcela: lista --> lista
    Modifica o estado da parcela para limpa e devolve a própria parcela.
    '''
    if eh_parcela(p):
        p['estado'] = '?'
        return p

def marca_parcela(p):
    '''
    marca_parcela: lista --> lista
    Modifica o estado da parcela para marcada com uma bandeira e 
    devolve a própria parcela.
    '''
    if eh_parcela(p):
        p['estado'] = '@'
        return p

def desmarca_parcela(p):
    '''
    desmarca_parcela: lista --> lista
    Modifica o estado da parcela para tapada e devolve a própria parcela.
    '''
    
    if eh_parcela(p):
        p['estado'] = '#'
        return p

def esconde_mina(p):
    '''
    esconde_mina: lista --> lista
    Modifica parcela escondendo uma mina e devolve a própria parcela.
    '''

    if eh_parcela(p):
        p['tem_minas'] = True
        return p

#Reconhecedores

def eh_parcela(arg):
    '''
    eh_parcela: universal --> bool
    Devolve True caso o seu argumento seja um TAD parcela e
    False caso contrário.
    '''
    # Corrigido com a proposta do Professor da cadeira.
    return type(arg) == dict and len(arg) == 2  and\
         'estado' in arg and 'tem_minas' in arg and type(arg['tem_minas']) == bool and \
        len(arg['estado']) == 1 and arg['estado'] in '#?@'

def eh_parcela_tapada(p):
    '''
    eh_parcela_tapada: lista --> bool
    Devolve True caso a parcela se encontre tapada e False
    caso contrário.
    '''
    return eh_parcela(p) and p['estado'] == '#'

def eh_parcela_marcada(p):
    '''
    eh_parcela_marcada: lista --> bool
    Devolve True caso a parcela se encontre marcada
    com uma bandeira e False caso contrário.
    '''
    return eh_parcela(p) and p['estado'] == '@'

def eh_parcela_limpa(p):
    '''
    eh_parcela_limpa: lista --> bool
    Devolve True caso a parcela se encontre limpa e False
    caso contrário.
    '''
    return eh_parcela(p) and p['estado'] == '?'

def eh_parcela_minada(p):
    '''
    eh_parcela_minada: lista --> bool
    Devolve True caso a parcela esconda uma mina e
    False caso contrário.
    '''
    return eh_parcela(p) and p['tem_minas'] 

#Teste

def parcelas_iguais(p1,p2):
    '''
    parcelas_iguais: lista x lista --> bool
    Devolve True apenas se os argumentos serem parcelas e serem iguais.
    '''
    # Corrigido com a proposta do Professor da cadeira.
    return eh_parcela(p1) and eh_parcela(p2) and p1 == p2

#Transformador

def parcela_para_str(p):
    '''
    parcela_para_str: lista --> str
    Devolve a cadeia de caracteres que representa a parcela
    em função do seu estado: parcelas tapadas ('#'), parcelas marcadas ('@'),
    parcelas limpas sem mina ('?') e parcelas limpas com mina ('X').
    '''
    if eh_parcela_limpa(p) and p['tem_minas']:
        return 'X'
    else:
        return p['estado']

#Função de alto nível

def alterna_bandeira(p):
    '''
    alterna_bandeira: lista --> bool
    Desmarca a parcela se estiver marcada e marca se estiver tapada, 
    devolvendo True. Em qualquer outro caso, não modifica a 
    parcela e devolve False.
    '''
    if eh_parcela_marcada(p):
        desmarca_parcela(p)
        return True
    elif eh_parcela_tapada(p):
        marca_parcela(p)
        return True
    else:
        return False

#TAD_CAMPO
#Construtores

def cria_campo(c,l):
    '''
    cria_campo: str x int --> lista
    Devolve o campo do tamanho pretendido formado por parcelas tapadas sem minas.
    '''
    if not (type(c) == str and type(l) == int and \
        'A' <= c <= 'Z' and len(c) == 1 and \
        1 <= l <= 99):
        raise ValueError("cria_campo: argumentos invalidos")
    campo = []
    col = []
    for linhas in range(l):
        for colunas in range(ord(c) - ord('A') + 1):
            col = col + [cria_parcela()]
        campo = campo + [col]
        col = []
    return campo

def cria_copia_campo(m):
    '''
    cria_copia_campo: lista --> lista
    Devolve uma nova cópia do campo.
    '''
    camp = []
    linha = []
    for l in range(len(m)):
        for elemento in range(len(m[l])):
            parc = m[l][elemento].copy()
            linha = linha + [parc]
        camp = camp + [linha]
        linha = []
    return camp

#Seletores

def obtem_ultima_coluna(m):
    '''
    obtem_ultima_coluna: lista --> str
    Devolve a cadeia de caracteres que corresponde à
    última coluna do campo de minas.
    '''
    return chr(len(m[0]) + ord('A') - 1)

def obtem_ultima_linha(m):
    '''
    obtem_ultima_linha: lista --> int
    Devolve o valor inteiro que corresponde à última linha
    do campo de minas.
    '''
    return len(m)

def obtem_parcela(m,c):
    ''' 
    obtem_parcela: lista x tuplo --> lista
    Devolve a parcela do campo que se encontra na coordenada introduzida.
    '''
    if eh_coordenada_do_campo(m, c): 
        coluna = ord(c[0]) - ord('A')  
        linha = c[1] - 1  # A coordenada usa 1-based index, convertendo para 0-based
        
        if 0 <= linha < len(m) and 0 <= coluna < len(m[0]):
            return m[linha][coluna]  


def obtem_coordenadas(m,s):
    '''
    obtem_coordenadas: lista x str --> tuplo
    Devolve o tuplo formado pelas coordenadas ordenadas em ordem ascendente de 
    esquerda à direita e de cima a baixo das parcelas dependendo do valor de s.
    '''
    res = ()
    for linha in range(len(m)):
        for coluna in range(len(m[linha])):
            c = cria_coordenada(chr(ord('A') + coluna),linha + 1)
            if s == 'limpas' and eh_parcela_limpa(obtem_parcela(m,c)):
                res = res + (c,)
            if s == 'marcadas' and eh_parcela_marcada(obtem_parcela(m,c)):
                res = res + (c,)
            if s == 'tapadas' and eh_parcela_tapada(obtem_parcela(m,c)):
                res = res + (c,)
            if s == 'minadas' and eh_parcela_minada(obtem_parcela(m,c)):
                res = res + (c,)
    return res

def obtem_numero_minas_vizinhas(m,c):
    '''
    obtem_numero_minas_vizinhas: lista x tuplo --> int
    Devolve o número de parcelas vizinhas da parcela na coordenada indicada 
    que escondem uma mina.
    '''
    if eh_coordenada_do_campo(m,c):
        n_minas = 0
        conjunto_coord = obtem_coordenadas_vizinhas(c)
        for coor in range(len(conjunto_coord)):
            if eh_parcela_minada(obtem_parcela(m,conjunto_coord[coor])):
                n_minas += 1
        return n_minas

#Reconhecedores

def eh_campo(arg):
    '''
    eh_campo: universal --> booleano
    Devolve True caso o seu argumento seja um TAD campo e False caso contrário.
    '''
    return type(arg) == list and type(len(arg))== int and 1 <= len(arg) <= 99 and\
        type(arg[1]) == list and eh_parcela(arg[0][0]) and \
        type(chr(len(arg[0]) + ord('A') - 1)) == str and \
        ord('A') <= len(arg[0]) + ord('A') - 1 <= ord('Z')

def eh_coordenada_do_campo(m,c):
    '''
    eh_coordenada_do_campo: lista x tuplo --> bool
    Devolve True se a coordenada introduzida é uma coordenada válida
    dentro do campo m.
    '''
    return eh_coordenada(c) and 1 <= obtem_linha(c) <= len(m) and \
    'A' <= obtem_coluna(c) <= obtem_ultima_coluna(m)

#Teste

def campos_iguais(m1,m2):
    '''
    campos_iguais: lista x lista --> bool
    Devolve True apenas se os argumentos introduzidos forem campos e forem iguais.
    '''
    return eh_campo(m1) and eh_campo(m2) and \
        obtem_ultima_coluna(m1) == obtem_ultima_coluna(m2) and\
        obtem_ultima_linha(m1) == obtem_ultima_linha(m2) and \
        m1 == m2

#Transformador

def campo_para_str(m):
    '''
    campo_para_str: lista --> str
    Devolve uma cadeia de caracteres que representa o campo de minas

    Corrigido com a proposta do Professor da cadeira
    '''
    num_cols = ord(obtem_ultima_coluna(m)) - ord('A')+1
    caracteres = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'[:num_cols]
    car = '   ' + caracteres + '\n'
    margem = '  +' + '-' * num_cols + '+' #para representar :+-----+...
    car += margem + '\n'
    
    for linha in range(len(m)):
        car += ('{:02d}'.format(linha + 1) + '|')
        for c in caracteres:
            coordenada = cria_coordenada(c,linha + 1)
            parc = obtem_parcela(m, coordenada)
            if eh_parcela_limpa(parc) and not eh_parcela_minada(parc):
                if obtem_numero_minas_vizinhas(m,coordenada) == 0:
                    car += ' '
                else:
                    car += str(obtem_numero_minas_vizinhas(m,coordenada))
            else:
                car += parcela_para_str(parc)
        
        car += '|\n'
    return car + margem

#Funções de alto nível

def coloca_minas(m, c, g, n):
    '''
    coloca_minas: lista x tuplo x lista x int --> lista
    Modifica destrutivamente o campo escondendo minas em parcelas dentro do campo.
    '''
    not_here = (coordenada_para_str(c),) + tuple(coordenada_para_str(coor) for coor in obtem_coordenadas_vizinhas(c) if eh_coordenada_do_campo(m, coor))
    minas_colocadas = []
    lim = cria_coordenada(obtem_ultima_coluna(m),obtem_ultima_linha(m))

    while n > 0:
        al = obtem_coordenada_aleatoria(lim,g)
        if coordenada_para_str(al) not in not_here and coordenada_para_str(al) not in minas_colocadas:
            
            esconde_mina(obtem_parcela(m,al))
            minas_colocadas.append(coordenada_para_str(al))
            n -= 1
    return m

def limpa_campo(m,c):
    '''
    limpa_campo: lista x tuplo --> lista
    Modifica destrutivamente o campo limpando a parcela na coordenada indicada,
    devolvendo o próprio campo.
    '''
    if eh_campo(m) and eh_coordenada_do_campo(m,c):
        if not eh_parcela_limpa(obtem_parcela(m,c)):
            limpa_parcela(obtem_parcela(m,c))
            if not eh_parcela_minada(obtem_parcela(m,c)) and obtem_numero_minas_vizinhas(m,c) == 0:
            #se não houver minas por perto, limpar também as coordenadas vizinhas
                for coor in obtem_coordenadas_vizinhas(c):
                    if eh_coordenada_do_campo(m,coor) and eh_parcela_tapada(obtem_parcela(m,coor)):
                        limpa_campo(m,coor)
        return m

#FUNCOES ADICIONAIS

def jogo_ganho(m):
    '''
    jogo_ganho: lista --> booleano
    Devolve True se todas as parcelas sem minas se encontram limpas, 
    ou False caso contrário.
    '''
    if eh_campo(m):
        res = (ord(obtem_ultima_coluna(m)) - ord('A') + 1)*(obtem_ultima_linha(m))
        return len(obtem_coordenadas(m,'limpas')) == res - \
            len(obtem_coordenadas(m,'minadas'))
        # ou seja, se todas as parcelas sem mina forem limpas

def turno_jogador(m):
    '''
    turno_jogador: lista --> booleano
    Modifica destrutivamente o campo de acordo com ação escolhida, devolvendo 
    False caso o jogador tenha limpo uma parcela que continha uma mina, 
    ou True caso contrário.

    Leitura da acao e da coordenada corrigida com a proposta do Professor da cadeira.
    '''
    acao = ''
    while not (acao == 'L' or acao == 'M'):
        acao = input('Escolha uma ação, [L]impar ou [M]arcar:')
    coordenada = ''
    while not(len(coordenada)==3 and 'A' <= coordenada[0] <= obtem_ultima_coluna(m) \
              and coordenada[1] in '0123456789'  and coordenada[2] in '0123456789' \
              and 1 <= int(coordenada[1:]) <= obtem_ultima_linha(m)):
        coordenada = input('Escolha uma coordenada:')

    coordenada_str = str_para_coordenada(coordenada)
    parc = obtem_parcela(m,coordenada_str)
    if acao == 'L':
        limpa_campo(m,coordenada_str)
        if eh_parcela_minada(parc):
            return False
        else:
            return True
    else:
        alterna_bandeira(parc)
        return True


def minas(c, l, n, d, s):
    '''
    minas: str x int x int x int x int --> booleano
    Devolve True se o jogador conseguir ganhar o jogo, ou False caso contrário.
    
    Leitura das coordenadas corrigido com a proposta do Professor da cadeira.
    '''
    if not (type(c) == str  and len(c) == 1 and 'A' <= c <= 'Z' and \
        type(l) == int and 1 <= l <= 99) :
        raise ValueError('minas: argumentos invalidos')
    if not (type(n) == int and n > 0 and n < (l * (ord(c) - ord('A')))):
        raise ValueError('minas: argumentos invalidos')
    if not (type(d) == int and (d == 32 or d == 64) and\
        type(s) == int and 0 < s <= (2**d -1)):
        raise ValueError('minas: argumentos invalidos')
    if ((ord(c) - ord('A') + 1) * l) - 9 < n:
        #tamanho do campo -> (nº colunas * nº linhas)
        raise ValueError('minas: argumentos invalidos')
    g = cria_gerador(d,s)
    m = cria_campo(c,l)
    print('   [Bandeiras {}/{}]'.format(len(obtem_coordenadas(m,'marcadas')),n))
    print(campo_para_str(m))
    coordenada = ''
    while not(len(coordenada)==3 and 'A' <= coordenada[0] <= c \
              and coordenada[1] in '0123456789'  and coordenada[2] in '0123456789' \
              and 1 <= int(coordenada[1:]) <= l):
        coordenada = input('Escolha uma coordenada:')
    coordenada_str = str_para_coordenada(coordenada)
    coloca_minas(m,coordenada_str,g,n)
    limpa_campo(m,coordenada_str)
    while not jogo_ganho(m):
        print('   [Bandeiras {}/{}]'.format(len(obtem_coordenadas(m,'marcadas')),n))
        print(campo_para_str(m))
        if not turno_jogador(m):
            print('   [Bandeiras {}/{}]'.format(len(obtem_coordenadas(m,'marcadas')),n))
            print(campo_para_str(m))
            print("BOOOOOOOM!!!")
            return False
        
    print('   [Bandeiras {}/{}]'.format(len(obtem_coordenadas(m,'marcadas')),n))
    print(campo_para_str(m))
    print("VITORIA!!!")
    return True