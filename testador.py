# -*- coding : utf-8 -*-

###########################################################
# Created: 26/05/2018
#
# Author: Ivan Carvalho

###########################################################

import subprocess
import sys
import shlex
import re
import urllib.request
import ssl

PATH_SUSY = "https://susy.ic.unicamp.br:9999/"
NOME_DO_ARQUIVO = ""
INPUT_EXTENSION = ".in"
OUTPUT_EXTENSION = ".out"


def descobre_comando(nome):
    """ Dado o nome do arquivo, descobre o comando que deve ser executado. Há duas opções:
    - python3 <nome>, caso o arquivo possua extensão .py
    - ./<nome>, caso o arquivo seja um executável qualquer (ex : programa compilado em C)
    """
    if ".py" in nome:
        """ Temos um arquivo Python. Retornamos o primeiro caso"""
        return "python3 {}".format(nome)
    else:
        """ Temos um executável qualquer. Retornamos o segundo caso"""
        return "./{}".format(nome)


def roda_comando(comando, entrada=""):
    """ Faz o parsing da string comando,executa o comando shell e retorna a saída.
    Caso haja uma entrada (stdin), fornece ela ao programa.
    """
    args = shlex.split(comando)  # transforma os comandos em uma lista
    entrada = entrada.encode("utf-8")  # converte a entrada para bytes
    resultado = subprocess.run(
        args, stdout=subprocess.PIPE, input=entrada
    )  # roda o comando e guarda a saída
    return resultado.stdout.decode("utf-8")  # converte o resultado para UTF-8 e retorna


def faz_download(url):
    """ Captura a saída de uma requisição wed a url designada"""
    return (
        urllib.request.urlopen(url, context=ssl.SSLContext(ssl.PROTOCOL_TLSv1))
        .read()
        .decode("utf-8")
    )


def descobre_arquivos(texto):
    """ Dado o código html da página, descobre quais testes abertos o problema tem"""
    limite = re.search(r"Testes fechados*", texto).span()[
        0
    ]  # obtemos a posicao em que começam os testes fechados
    return re.findall(r"arq\d*", texto[:limite])


def descobre_extensao(texto, arquivos):
    """ Dado o código html da página, descobre a extensão dos arquivos de saída : .out ou .res
    Esta função foi adicionada para dar compatilibilidade com turmas que não possuiam extensão .out .
    """
    final_com_out = arquivos[0] + ".out"  # vamos checar se há um arq*.out
    if final_com_out in texto:
        """ Há um arquivo com extensão .out, logo está extensão será a de todos outros arquivos"""
        return ".out"
    else:
        """ Não há um arquivo com extensão .out, logo a extensão .res será a de todos outros arquivos"""
        return ".res"


def remove_duplicatas(lista):
    """ Os arquivos de teste apareciam duplicados no HTML. Essa função remove esses testes"""
    nova_lista = list(
        set(lista)
    )  # removemos as duplicatas com o set e após transformamos o conjunto em uma lista novamente
    return sorted(nova_lista)  # ordenamos pois o set pode alterar a ordem


class cores:
    """ Armazena as contantes das cores"""

    ROXO = "\033[95m"
    CIANO = "\033[96m"
    CIANO_ESCURO = "\033[36m"
    AZUL = "\033[94m"
    VERDE = "\033[92m"
    AMARELO = "\033[93m"
    VERMELHO = "\033[91m"
    NEGRITO = "\033[1m"
    SUBLINHADO = "\033[4m"
    FIM = "\033[0m"


class TesteSusy:
    def __init__(self, nome):
        self.nome = nome.replace(
            ".in", ""
        )  # retiramos o in caso ocorra para ter o nome puro

    def roda(self):
        """ Roda o código do usuário, baixa o código esperado e compara"""
        PATH_DOWNLOAD_IN = PATH_SUSY + "/dados/" + self.nome + INPUT_EXTENSION
        PATH_DOWNLOAD_OUT = PATH_SUSY + "/dados/" + self.nome + OUTPUT_EXTENSION
        caso_teste = faz_download(PATH_DOWNLOAD_IN)
        saida_esperada = faz_download(PATH_DOWNLOAD_OUT)
        comando_executavel = descobre_comando(NOME_DO_ARQUIVO)
        saida_obtida = roda_comando(comando_executavel, caso_teste)
        if saida_esperada == saida_obtida:
            """ O código executou corretamente"""
            print(
                cores.NEGRITO + ("{}.in : ".format(self.nome)) + cores.AZUL + "OK" + cores.FIM
            )
            return 0
        else:
            """ O código não executou corretamente. Iremos exibir a diferença"""
            print(
                cores.NEGRITO
                + ("{}.in : ".format(self.nome))
                + cores.VERMELHO
                + "Resposta Errada"
                + cores.FIM
            )
            print(">>> Saida esperada (SuSy):")
            print(
                saida_esperada, end=""
            )  # usamos end = "" para evitar duas quebras de linha
            print(">>> Saida do seu programa:")
            print(saida_obtida)
            return 1


if __name__ == "__main__":

    argumentos = sys.argv
    if len(argumentos) < 4:
        # Usuário não forneceu numero suficiente de parâmetros
        print("Uso: python3 testador.py <turma> <laboratorio> <nome do arquivo>")
        print(
            "Exemplo: python3 testador.py mc102qrst 01 lab01.py"
        )  # exemplo de arquivo Python
        print(
            "Exemplo: python3 testador.py mc202abc 00 lab00"
        )  # exemplo de executável qualquer
        exit()  # Nada acontece, feijoada

    turma = argumentos[1]
    numero = argumentos[2]

    NOME_DO_ARQUIVO = argumentos[3]
    PATH_SUSY = PATH_SUSY + turma + "/" + numero
    PATH_TESTE = PATH_SUSY + "/dados/testes.html"

    print("Executando os testes...")

    codigo_fonte_pagina_teste = faz_download(
        PATH_TESTE
    )  # baixamos a página que contém os índices dos testes
    lista_de_arquivos = remove_duplicatas(
        descobre_arquivos(codigo_fonte_pagina_teste)
    )  # gera a lista com os arquivos do lab e remove testes que aparecem duas vezes
    OUTPUT_EXTENSION = descobre_extensao(
        codigo_fonte_pagina_teste, lista_de_arquivos
    )  # descobre se a extensão é .out ou .res

    testes_incorretos = 0

    for arquivo in lista_de_arquivos:
        teste_do_arquivo = TesteSusy(arquivo)
        testes_incorretos += (
            teste_do_arquivo.roda()
        )  # chama a função responsável por rodar cada caso teste

    print("Total de erros encontrados: {}".format(testes_incorretos))
    print(
        cores.NEGRITO
        + "Lembre-se que o testador"
        + cores.VERMELHO
        + " NÃO "
        + cores.FIM
        + cores.NEGRITO
        + "envia seu código!"
        + cores.FIM
    )
