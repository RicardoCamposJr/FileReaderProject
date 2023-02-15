'''
/*******************************************************************************
Autor: Ricardo Campos de Oliveira Júnior
Componente Curricular: MI - Algoritmos 
Concluido em: 03/07/2022
Declaro que este código foi elaborado por mim de forma individual e não contém nenhum
trecho de código de outro colega ou de outro autor, tais como provindos de livros e
apostilas, e páginas ou documentos eletrônicos da Internet. Qualquer trecho de código
de outra autoria que não a minha está destacado com uma citação para o autor e a fonte
do código, e estou ciente que estes trechos não serão considerados para fins de avaliação.
******************************************************************************************/'''

import sys
from funcoes import *

#VARÁVEIS, E ESTRUTURAS UTILIZADAS NO PROGRAMA
lista_txt = []   #LISTA DE ARQUIVOS DE TEXTO PRESENTES NO DIRETÓRIO ESPECIFICADO PELO USUÁRIO;
lista_caracteres = ['\n', ',', '<', '.', '>', ';', ':', '/', '?', '\\', '|', '~', '^', ']', '}', '´', '`', '[', '{', '"', "'", '!', '@', '#', '$', '%', '¨', '&', '*', '(', ')', '-', '_', '=', '+']
dicionario = {}   #ESTRUTURA DE DADOS UTILIZADA PARA A IMPLEMENTAÇÃO DO ÍNDICE INVERTIDO;
arquivos_lidos = []   #LISTA COM OS CAMINHOS ABSOLUTOS DOS ARQUIVOS LIDOS;


argumentos = sys.argv   #RECEBIMENTO DOS ARGUMENTOS DE LINHA DE COMANDO EM UMA LISTA;
argumentos.pop(0)   #TRATAMENTO DA LISTA, RETIRANDO O NOME DO ARQUIVO EM QUE O SISTEMA SE ENCONTRA;

#VARIÁVEL QUE POSSIBILITA O FUNCIONAMENTO DO SISTEMA;
sistema = validar_arquivo(argumentos)

if sistema == True:
    if argumentos[0].upper() == 'LER':   #AÇÃO A SER REALIZADA NO CÓDIGO; 
        dicionario = abertura_dicionario(dicionario)   #ABERTURA DO DICIONÁRIO COM O ÍNDICE INVERTIDO;
        arquivos_lidos = abertura_arquivo(arquivos_lidos)   #ABERTURA DA LISTA DE ARQUIVOS JÁ LIDOS PELO SISTEMA;
        if os.path.isdir(argumentos[1]) == True:   #PROCESSO DE LEITURA PARA CASO O USUÁRIO INDIQUE UM DIRETÓRIO;
            listar_txt(argumentos,lista_txt)   #LEITURA DOS ARQUIVOS DE TEXTO PRESENTES NO DIRETÓRIO ESPECIFICADO;
            leitura_diretorio(argumentos, lista_txt, lista_caracteres, arquivos_lidos, dicionario)   #REALIZA A LEITURA DO DIRETÓRIO ESPECIFICADO PELO USUÁRIO;
        else:
            leitura_arquivo(argumentos,lista_caracteres, arquivos_lidos, dicionario)   #REALIZA A LEITURA DO ARQUIVO ESPECIFICADO PELO USUÁRIO;
        armazenamento(dicionario, arquivos_lidos)   #ARMAZENAMENTO DOS DADOS LIDOS;

        


    elif argumentos[0].upper() == 'REMOVER':   #REMOÇÃO DE UM DOCUMENTO;
        dicionario = abertura_dicionario(dicionario)    #ABERTURA DO DICIONÁRIO COM O ÍNDICE INVERTIDO;
        arquivos_lidos = abertura_arquivo(arquivos_lidos)   #ABERTURA DA LISTA DE ARQUIVOS JÁ LIDOS PELO SISTEMA;
        if dicionario:
            #CASO O USUARIO INFORME UM ARQUIVO
            if argumentos[1].endswith('.txt'):
                arquivos_lidos = remocao_arquivo(argumentos, dicionario, arquivos_lidos)
            #CASO O USUÁRIO INFORME UM DIRETÓRIO
            elif not argumentos[1].endswith('.txt') and os.path.isdir(argumentos[1]):
                arquivos_lidos = remocao_diretorio(argumentos, lista_txt,dicionario, arquivos_lidos)
            
            tratamento_dicionario(dicionario)   #TRATAMENTO DO DICIONÁRIO PARA A RETIRADA DOS TERMOS SEM APARIÇÕES;
            armazenamento(dicionario, arquivos_lidos)   #ARMAZENAMENTO DOS DADOS LIDOS;
        else:
            print('\nO sistema ainda não possui dados. Não é possível realizar a operação.\n')


        '''PARA O CASO DE ATUALIZAÇÃO, É NECESSÁRIA A REMOÇÃO DOS TERMOS E POSTERORMENTE SUA LEITURA NOVAMENTE,
        ATUALIZANDO ASSIM OS TERMOS PRESENTES NOS ARQUIVOS'''
    elif argumentos[0].upper() == 'ATT':   #ATUALIZAÇÃO DE UM DOCUMENTO;
        dicionario = abertura_dicionario(dicionario)   #ABERTURA DO DICIONÁRIO COM O ÍNDICE INVERTIDO;
        arquivos_lidos = abertura_arquivo(arquivos_lidos)   #ABERTURA DA LISTA DE ARQUIVOS JÁ LIDOS PELO SISTEMA;
        if dicionario:
            #CASO O USUARIO INFORME UM ARQUIVO
            if argumentos[1].endswith('.txt'):
                arquivos_lidos = remocao_arquivo(argumentos, dicionario, arquivos_lidos)
            #CASO O USUÁRIO INFORME UM DIRETÓRIO
            elif not argumentos[1].endswith('.txt') and os.path.isdir(argumentos[1]):
                arquivos_lidos = remocao_diretorio(argumentos, lista_txt,dicionario, arquivos_lidos)

            tratamento_dicionario(dicionario)

            #CASO O USUÁRIO INFORME UM DIRETÓRIO
            if os.path.isdir(argumentos[1]) == True:
                leitura_diretorio(argumentos, lista_txt, lista_caracteres, arquivos_lidos, dicionario)   #REALIZA A LEITURA DO DIRETÓRIO ESPECIFICADO PELO USUÁRIO;
            else:
                #CASO O USUARIO INFORME UM ARQUIVO
                leitura_arquivo(argumentos,lista_caracteres, arquivos_lidos, dicionario)   #REALIZA A LEITURA DO ARQUIVO ESPECIFICADO PELO USUÁRIO;

            armazenamento(dicionario, arquivos_lidos)   #ARMAZENAMENTO DOS DADOS LIDOS;
            print('\nDiretório atualizado com sucesso!\n')
        else:
            print('\nO sistema ainda não possui dados. Não é possível realizar a operação.\n')

    elif argumentos[0].upper() == 'BUSCAR':   #BUSCA DE UM TERMO NOS ARQUIVOS JÁ LIDOS;
        dicionario = abertura_dicionario(dicionario)   #ABERTURA DO DICIONÁRIO COM O ÍNDICE INVERTIDO;
        arquivos_lidos = abertura_arquivo(arquivos_lidos)   #ABERTURA DA LISTA DE ARQUIVOS JÁ LIDOS PELO SISTEMA;
        if dicionario:
            lista_aparicoes_arquivos = busca(argumentos, dicionario)   #REALIZA A BUSCA NO DICIONÁRIO;
            casos = ordenacao(lista_aparicoes_arquivos,argumentos)   #ORDENA AS APARIÇÕES DE FORMA DECRESCENTE;
            exibicao_ordenada(casos, argumentos)   #EXIBIÇÃO ORDENADA DAS APARIÇÕES;
        else:
            print('\nO sistema ainda não possui dados. Não é possível realizar a operação.\n')

    elif argumentos[0].upper() == 'VER':   #VISUALIZAÇÃO DA ESTRUTURA DE ÍNDICE INVERTIDO DO SISTEMA;
        dicionario = abertura_dicionario(dicionario)   #ABERTURA DO DICIONÁRIO COM O ÍNDICE INVERTIDO
        arquivos_lidos = abertura_arquivo(arquivos_lidos)   #ABERTURA DA LISTA DE ARQUIVOS JÁ LIDOS PELO SISTEMA;
        exibicao_indice(dicionario)   #EXIBE A ESTRUTURA DE ÍNDICE INVERTIDO DO SISTEMA;

        '''EXIBIÇÃO DE COMO UTILIZAR O SISTEMA.'''
    elif argumentos[0].upper() == 'HELP' or argumentos[0].upper() != 'LER' and argumentos[0].upper() != 'REMOVER' and argumentos[0].upper() != 'ATT' and argumentos[0].upper() != 'BUSCAR' and argumentos[0].upper() != 'VER':
        ajuda()   #EXIBE COMO O SISTEMA DEVE SER OPERADO;