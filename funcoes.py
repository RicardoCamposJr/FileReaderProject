import os
from pickle import dump, load

'''FUNÇÃO RESPONSÁVEL PELA LEITURA DO ARQUIVO QUE CONTÉM O DICIONÁRIO COM A LÓGICA DE ÍNDICE INVERTIDO,
CASO NÃO HAJA O ARQUIVO AINDA, RETORNA SOMENTE UM DICIONÁRIO VAZIO.'''
def abertura_dicionario(dicionario):
    try:
        with open('estruturas.dat', 'rb') as armazenamento:
            dicionario = load(armazenamento)
        return dicionario
    except:
        dicionario = {}
        print('Bem vindo ao buscador de termos!')
        return dicionario

'''FUNÇÃO RESPONSÁVEL PELA LEITURA DA LISTA QUE CONTÉM OS ARQUIVOS LIDOS ATÉ O MOMENTO,
CASO NÃO HAJA AINDA, RETORNA SOMENTE UMA LISTA VAZIA.'''
def abertura_arquivo(arquivos_lidos):
    try:
        with open('estruturas.dat', 'rb') as armazenamento:
            dicionario = load(armazenamento)
            arquivos_lidos = load(armazenamento)
        return arquivos_lidos
    except:
        arquivos_lidos = []
        return arquivos_lidos

'''FUNÇÃO QUE RECEBE OS ARGUMENTOS DE LINHA DE COMANDO E UMA LISTA VAZIA, RETORNANDO QUAIS SÃO OS 
ARQUIVOS DE TEXTO PRESENTES NO DIRETÓRIO INSERIDO PELO USUÁRIO.'''
def listar_txt(argumentos,lista_txt):
    for txt in os.listdir(argumentos[1]):
        if txt.endswith('.txt'):
            lista_txt.append(txt)
    
#RECEBE A LEITURA DO ARQUIVO E REALIZA O TRATAMENTO DO TEXTO DESSE ARQUIVO;
def tratamento(leitura_arquivo_txt, lista_caracteres):
    leitura_arquivo_txt_palavras = []
    '''RETIRADA DE QUALQUER CARACTERE ESPECIAL UTILIZANDO A LISTA DE CARACTERES ESPECIAIS PARA ESSA FINALIDADE.'''
    for linha in leitura_arquivo_txt:
        posicao = leitura_arquivo_txt.index(linha)
        for caractere in lista_caracteres:
            while caractere in linha:
                linha_nova = linha.replace(caractere,'')
                linha = linha_nova
                leitura_arquivo_txt[posicao] = linha_nova

    '''SEPARAÇÃO DE CADA PALAVRA NAS FRASES PRESENTES NO ARQUIVO.'''
    for palavra in leitura_arquivo_txt:
        if ' ' in palavra:
            separacao = palavra.split()
            for elementos in separacao:
                leitura_arquivo_txt_palavras.append(elementos)
        else:
            leitura_arquivo_txt_palavras.append(palavra)
        
                
    '''RETIRADA DOS ESPAÇOS EM BRANCO APÓS O TRATAMENTO ACIMA.'''
    for palavra in leitura_arquivo_txt_palavras:
        posicao = leitura_arquivo_txt_palavras.index(palavra)
        palavra_sem_espaços = palavra.strip()
        leitura_arquivo_txt_palavras[posicao] = palavra_sem_espaços.lower()
    
    return leitura_arquivo_txt_palavras

'''FUNÇÃO RESPONSÁVEL PELA FORMAÇÃO DO ÍNDICE INVERTIDO A PARTIR DAS PALAVRAS LIDAS NOS ARQUIVOS DE TEXTO
E ANTERIORMENTE TRATADAS.'''
def indice_invertido(txt, leitura_arquivo_txt, dicionario, arquivos_lidos):
    if txt not in arquivos_lidos:   
        for termo in leitura_arquivo_txt:
            if termo not in dicionario:
                dicionario[termo.lower()] = [[txt, 1]]   #CRIAÇÃO DA CHAVE COM O TERMO NO DICIONÁRIO;
            else:
                aparicoes = []
                for valores in dicionario[termo]:
                    aparicoes.append(valores[0])
                    if valores[0] == txt:
                        valores[1] += 1   #ATUALIZAÇÃO DOS DADOS, CASO O TERMO JÁ ESTEJA NO DICIONÁRIO, CONTABILIZANDO O NÚMERO DE VEZES QUE O TERMO APARECE NO ARQUIVO;
                if txt not in aparicoes:
                    dicionario[termo].append([txt, 1])   #ATUALIZAÇÃO DAS APARIÇÕES NO DICIONÁRIO, ADICIONANDO O ARQUIVO EM QUE O MESMO TERMO APARECE.
    
'''FUNÇÃO QUE RECEBE OS ARGUMENTOS DE LINHAS DE COMANDO, A LISTA DE ARQUIVOS PRESENTES NO DIRETÓRIO, A LISTA
DE CARACTERES ESPECIAIS E AS ESTRUTURAS DE ARMAZENAMENTO, REALIZANDO A LEITURA DE TODOS ESSES ARQUIVOS.'''
def leitura_diretorio(argumentos, lista_txt, lista_caracteres, arquivos_lidos, dicionario):
    for txt in lista_txt:
        txt = argumentos[1] + '\\' + txt
        if txt not in arquivos_lidos or argumentos[1] == 'ATT':
            try:
                with open(txt, 'r', encoding='utf-8') as arquivo_txt:
                    leitura_arquivo_txt = arquivo_txt.readlines()
                leitura_arquivo_txt_tratada = tratamento(leitura_arquivo_txt, lista_caracteres)   #FUNÇÃO QUE TRATA O TEXTO DOS ARQUIVOS .TXT;
                indice_invertido(txt, leitura_arquivo_txt_tratada, dicionario, arquivos_lidos)   #FORMAÇÃO DA ESTRUTURA DE ÍNDICE INVERTIDO;
                arquivos_lidos.append(txt)   #INCREMENTAÇÃO DO ARQUIVO LIDO NA LISTA DE ARQUIVOS LIDOS;
                print('\nArquivo lido com sucesso!\n')
            except:
                print(f'Não foi possível realizar a leitura do arquivo: {txt}.')
        elif txt in arquivos_lidos and argumentos[1] != 'ATT':
            print('\nArquivo já lido. Caso queira atualizá-lo, insira o comando ATT.\n')

'''FUNÇÃO QUE RECEBE OS ARGUMENTOS DE LINHAS DE COMANDO, A LISTA DE CARACTERES 
ESPECIAIS E AS ESTRUTURAS DE ARMAZENAMENTO, REALIZANDO A LEITURA DO ARQUIVO ESPECIFICADO PELO USUÁRIO.'''
def leitura_arquivo(argumentos,lista_caracteres, arquivos_lidos, dicionario):
    txt = argumentos[1]
    if txt not in arquivos_lidos or argumentos[1] == 'ATT':
        try:
            with open(txt, 'r', encoding='utf-8') as arquivo_txt:
                leitura_arquivo_txt = arquivo_txt.readlines()
            leitura_arquivo_txt_tratada = tratamento(leitura_arquivo_txt, lista_caracteres)   #FUNÇÃO QUE TRATA O TEXTO DOS ARQUIVOS .TXT;
            indice_invertido(txt, leitura_arquivo_txt_tratada, dicionario, arquivos_lidos)   #FORMAÇÃO DA ESTRUTURA DE ÍNDICE INVERTIDO;
            arquivos_lidos.append(txt)   #INCREMENTAÇÃO DO ARQUIVO LIDO NA LISTA DE ARQUIVOS LIDOS;
            print('\nArquivo lido com sucesso!\n')
        except:
            print(f'\nNão foi possível realizar a leitura do arquivo: {txt}.\n\nInsira somente arquivos de texto (formato ".txt").\n')
    elif txt in arquivos_lidos and argumentos[1] != 'ATT':
        print('\nArquivo já lido. Caso queira atualizá-lo, insira o comando ATT.\n')

#FUNÇÃO QUE RECEBE O DICIONÁRIO CONTENDO A ESTRUTURA DE ÍNDICE INVERTIDO E A LISTA DE ARQUIVOS LIDOS, ARMAZENANDO-OS;
def armazenamento(dicionario, arquivos_lidos):
    with open('estruturas.dat', 'wb') as armazenamento:
        dump(dicionario, armazenamento)
        dump(arquivos_lidos, armazenamento)
    
        

#FUNÇÃO RESPONSÁVEL POR REMOVER AS APARIÇÕES NO ARQUIVO INFORMADO PELO USUÁRIO;
def remocao_arquivo(argumentos, dicionario, arquivos_lidos):
    remocao = False   #VARIÁVEL RESPONSÁVEL POR INFORMAR SE HOUVE UMA REMOÇÃO DE FATO, CASO NÃO OCORRA, SIGNIFICA QUE O ARQUIVO INFORMADO NÃO ESTÁ PRESENTE NO SISTEMA;
    for matrizes in dicionario.values():
        for lista_aparicao in matrizes:
            posicao = matrizes.index(lista_aparicao)
            if argumentos[1] == lista_aparicao[0]:
                matrizes.pop(posicao)   #RETIRADA DA APARIÇÃO DO ARQUIVO SOLICITADO, EXCLUINDO-O DO DICIONÁRIO;
                if argumentos[1] in arquivos_lidos:   #RETIRADA DO ARQUIVO DA LISTA DE ARQUIVOS LIDOS;
                    posicao_lista_arquivos_lidos = arquivos_lidos.index(argumentos[1])
                    arquivos_lidos.pop(posicao_lista_arquivos_lidos)
                    remocao = True
    if argumentos[0].upper() == 'REMOVER' and remocao == True:   #CONFIRMAÇÃO DA REMOÇÃO;
        print('\nArquivo removido com sucesso!\n')
    elif argumentos[0].upper() == 'REMOVER' and remocao == False:   #CONFIRMAÇÃO DA NÃO EXISTÊNCIA DO ARQUIVO NO SISTEMA;
        print('\nO arquivo não está presente no sistema para realizar sua remoção.\n')
    return arquivos_lidos

def remocao_diretorio(argumentos, lista_txt,dicionario, arquivos_lidos):
    remocao = False
    listar_txt(argumentos,lista_txt)
    for arquivos in lista_txt:
        arquivos = argumentos[1] + '\\' + arquivos
        cont = 0
        for matrizes in dicionario.values():
            for lista_aparicao in matrizes:
                posicao = matrizes.index(lista_aparicao)
                if arquivos == lista_aparicao[0]:
                    matrizes.pop(posicao)
                    if cont == 0:
                        posicao_lista_arquivos_lidos = arquivos_lidos.index(arquivos)
                        arquivos_lidos.pop(posicao_lista_arquivos_lidos)
                        cont = 'Já excluído da lista.'
                        remocao = True
    if argumentos[0].upper() == 'REMOVER' and remocao == True:
        print('\nDiretório removido com sucesso!\n')
    elif argumentos[0].upper() == 'REMOVER' and remocao == False:
        print('\nOs arquivos não estâo presentes no sistema para realizar a remoção.\n')

    return arquivos_lidos

#FUNÇÃO RESPONSÁVEL POR RETIRAR TODOS OS TERMOS QUE NÃO CONTÉM APARIÇÕES NOS ARQUIVOS, REMOVENDO-OS DO DICIONÁRIO;
def tratamento_dicionario(dicionario):
    for chaves in dicionario.copy():
        if dicionario[chaves] == []:
            dicionario.pop(chaves)




#FUNÇÃO RESPONS´VEL POR REALIZAR A BUSCA DO TERMO NO DICIONÁRIO, RETORNANDO UMA LISTA COM SUAS APARIÇÕES;
def busca(argumentos, dicionario):
    lista_aparicoes_arquivos = []
    if argumentos[1] in dicionario:
        lista_aparicoes_arquivos = dicionario[argumentos[1]]
        return lista_aparicoes_arquivos


#FUNÇÃO RESPONSÁVEL POR REALIZAR A ORDENAÇÃO DE FORMA DECRESCENTE DAS APARIÇÕES, PARA SUA POSTERIOR EXIBIÇÃO;
def ordenacao(lista_aparicoes_arquivos,argumentos):
    casos = {}
    try:
        for aparicoes in lista_aparicoes_arquivos:
            casos[aparicoes[0]] = aparicoes[1]
        casos = sorted(casos.items(), key=lambda aparicao:aparicao[1], reverse=True)   #ORDENAÇÃO DE FORMA DECRESCENTE;
        return casos
    except TypeError:
        print(f'\nO termo "{argumentos[1]}" não tem aparição em nenhum arquivo.\n')
        

#FUNÇÃO RESPONSÁVEL POR EXIBIR AS APARIÇÕES DO TERMO PROCURADO PELO USUÁRIO, DE FORMA DECRESCENTE;
def exibicao_ordenada(casos, argumentos):
    if casos:
        print(f'\nO termo "{argumentos[1]}" aparece em {len(casos)} documentos. São eles:\n')
        for tupla in casos:
            print(f'Arquivo: {tupla[0]};\nNúmero de aparicoes no arquivo acima: {tupla[1]}')
            print()

#FUNÇÃO RESPONSÁVEL PELA VISUALIZAÇÃO DA ESTRUTURA DE ÍNDICE INVERTIDO PRESENTE NO SISTEMA;
def exibicao_indice(dicionario):
    if dicionario:
        print('\nÍNDICE INVERTIDO\n')
        for chave in dicionario:
            print(f'Termo: {chave}')
            for valor in dicionario[chave]:
                print(f'Aparições: {valor}')
                print()
    else:
        print('\nO sistema ainda não possui dados. Não é possível realizar a operação.\n')

#FUNÇÃO QUE EXIBE A FORMA DE COMO OPERAR O SISTEMA PARA O USUÁRIO;
def ajuda():
    print('\nBem Vindo ao seu buscador pessoal!\n')
    print('Para o manuseio do sistema, o usuário deve optar por seguir as seguintes ações possíveis:\n')
    print('  [LER]   - Ler um diretório ou arquivo para ser acrescentado aos documentos:\n            O comando "LER" deve ser inserido como primeiro argumento de linha de comando;')
    print('            Logo após inserir o comando "LER", o usuário deve acrescentar como segundo argumento o caminho absoluto do diretório ou arquivo a ser lido;')
    print('            Caso a opção de leitura seja um arquivo, deve-se inserir o caminho absoluto do arquivo juntamente com sua extensão ".txt"\n')
    print('[REMOVER] - Remover um arquivo ou diretório dos documentos:')
    print('            O comando "REMOVER" deve ser inserido como primeiro argumento de linha de comando;')
    print('            Logo após inserir o comando "REMOVER", o usuário deve acrescentar como segundo argumento o caminho absoluto do diretório ou arquivo a ser removido;')
    print('            Caso a opção de remoção seja um arquivo, deve-se inserir o caminho absoluto do arquivo juntamente com sua extensão ".txt"\n')
    print('  [ATT]   - Atualizar as informações daquele documento:')
    print('          - Logo após inserir o comando "ATT", o usuário deve acrescentar como segundo argumento o caminho absoluto do diretório ou arquivo a ser atualizado;\n')
    print('[BUSCAR]  - Buscar por um termo nos já arquivos lidos:')
    print('            O comando "BUSCAR" deve ser inserido como primeiro argumento de linha de comando;')
    print('            Logo após o comando, o usuário deve inserir o termo a ser buscado no sitema;\n')
    print('  [VER]   - Visualizar a estrutura de índice invertido do sistema:')
    print('            O usuário deve inserir somente o comando "VER" como argumento de linha de comando.\n')
    print(' [HELP]   - Obter ajuda para a operação do sistema:')
    print('            O usuário deve inserir somente o comando "HELP", ou qualquer caractere irregular para o sistema, como argumento de linha de comando.\n')

#RECEBE OS ARGUMENTOS DE LINHA DE COMANDO E RETORNA "True" DE O ARQUIVO EXISTE DE FATO OU "False" SE NÃO EXISTE;
def validar_arquivo(argumentos):
    if argumentos[0].upper() == 'LER' or argumentos[0].upper() == 'REMOVER' or argumentos[0].upper() == 'ATT'  and os.path.exists(argumentos[1]) == True:
        return True
    elif argumentos[0].upper() == 'VER' or argumentos[0].upper() == 'BUSCAR' or argumentos[0].upper() == 'HELP':
        return True
    elif argumentos[0].upper() != 'VER' or argumentos[0].upper() != 'BUSCAR' or argumentos[0].upper() != 'HELP' or argumentos[0].upper() != 'LER' or argumentos[0].upper() != 'REMOVER' or argumentos[0].upper() != 'ATT':
        return True
    else:
        print('\nArquivo não encontrado.\n')
        return False