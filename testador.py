# -*- coding : utf-8 -*-

###########################################################
# Created: 26/05/2018
#
# Author: Ivan Carvalho

########################################################### 

"""This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    any later version.
    
    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>
"""

import subprocess
import sys
import shlex
import re

PATH_SUSY = "https://susy.ic.unicamp.br:9999/"
NOME_DO_ARQUIVO = ""

def roda_comando(comando,entrada = ""):
	""" Faz o parsing da string comando,executa o comando shell e retorna a saída.
	Caso haja uma entrada (stdin), fornece ela ao programa.
	"""
	args = shlex.split(comando) # transforma os comandos em uma lista
	entrada = entrada.encode("utf-8") # converte a entrada para bytes
	resultado = subprocess.run(args, stdout = subprocess.PIPE,input = entrada) # roda o comando e guarda a saída
	return resultado.stdout.decode("utf-8") # converte o resultado para UTF-8 e retorna

def faz_download(url):
	""" Captura a saída do comando curl com a url designada"""
	comando = "curl -s %s" % (url) # curl para baixar silenciosamente a página
	return roda_comando(comando)

def descobre_arquivos(texto):
	""" Dado o codigo html da pagina, descobre quais testes abertos o problema tem"""
	limite = re.search(r"Testes fechados",texto).span()[0] # obtemos a posicao em que começam os testes fechados
	return re.findall(r"arq\d\d.in",texto[:limite])

def remove_duplicatas(lista):
	""" Por algum motivo, alguns arquivos de teste apareciam duplicados no HTML. Essa função remove esses testes"""
	nova_lista = list(set(lista)) # removemos as duplicatas com o set e após transformamos o conjunto em uma lista novamente
	return sorted(nova_lista) # ordenamos pois o set pode alterar a ordem

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

	def __init__(self,nome):
		self.nome = nome.replace(".in","") # retiramos o in caso ocorra para ter o nome puro

	def roda(self):
		""" Roda o código do usuário, baixa o código esperado e compara"""
		PATH_DOWNLOAD_IN = PATH_SUSY +  "/dados/" + self.nome + ".in"
		PATH_DOWNLOAD_OUT = PATH_SUSY +  "/dados/" + self.nome + ".out"
		caso_teste = faz_download(PATH_DOWNLOAD_IN)
		saida_esperada = faz_download(PATH_DOWNLOAD_OUT)
		comando_python = "python3 %s" % NOME_DO_ARQUIVO
		saida_obtida = roda_comando(comando_python,caso_teste)
		if saida_esperada == saida_obtida:
			""" O código executou corretamente"""
			print(cores.NEGRITO + ("%s.in : " % self.nome) + cores.AZUL + "OK" + cores.FIM)
			return 0
		else:
			""" O código não executou corretamente. Iremos exibir a diferença"""
			print(cores.NEGRITO + ("%s.in :" % self.nome) + cores.VERMELHO + "Resposta Errada" + cores.FIM)
			print(">>> Saida esperada (SuSy):")
			print(saida_esperada, end = "") # usamos end = "" para evitar duas quebras de linha
			print(">>> Saida do seu programa:")
			print(saida_obtida)
			return 1

if __name__ == "__main__":
	
	argumentos = sys.argv
	if len(argumentos) < 4:
		# Usuário não forneceu numero suficiente de parâmetros
		print("Uso     : python3 testador.py <turma> <laboratorio> <nome do arquivo>")
		print("Exemplo : python3 testador.py mc102qrst 01 lab01.py")
		exit() # Nada acontece, feijoada
	
	turma = argumentos[1]
	numero = argumentos[2]
	
	NOME_DO_ARQUIVO = argumentos[3]
	PATH_SUSY = PATH_SUSY + turma + "/" + numero
	PATH_TESTE = PATH_SUSY + "/dados/testes.html"
	
	print("Executando os testes...")

	lista_de_arquivos = remove_duplicatas(descobre_arquivos(faz_download(PATH_TESTE))) # gera a lista com os arquivos do lab e remove testes que aparecem duas vezes
	testes_incorretos = 0

	for arquivo in lista_de_arquivos:
		teste_do_arquivo = TesteSusy(arquivo)
		testes_incorretos += teste_do_arquivo.roda() # chama a função responsável por rodar cada caso teste

	print("Total de erros encontrados: %d" % testes_incorretos)
	print(cores.NEGRITO + "Lembre-se que o testador" + cores.VERMELHO + " NÃO " + cores.FIM + cores.NEGRITO + "envia seu código!" + cores.FIM)
