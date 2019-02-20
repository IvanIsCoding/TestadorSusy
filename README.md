# Testador em Python do Susy [![](https://img.shields.io/badge/python-3.5+-blue.svg)](https://www.python.org/download/releases/3.5.0/) [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)
## Objetivos 
A ideia do testador é agilizar a detecção de erros no código, evitar submissões incorretas e além de tudo mostrar para
os alunos da disciplina de Introdução à Programação que os conhecimentos que eles aprendem possuem aplicações práticas. 
## Utilidade
Este script foi feito para facilitar a verificação de seu programa pelos casos
teste do *SuSy*. O que não representa que o programa está correto, mas que passou
pelos casos **abertos** do *SuSy*.

## O que é feito pelo script
O script baixa os arquivos de teste do servidor da Unicamp, roda seu programa nesses casos e compara com a saída esperada.
Nenhum arquivo adicional é criado.
## Como utilizar
1. Certifique-se que os arquivos que você deseja executar estejam na mesma pasta;
2. Caso o arquivo seja um executável, certifique-se que você tem permissão de executar o arquivo;
3. Coloque o testador.py nesta pasta;
4. Execute o testador com o comando:
>     python3 testador.py <turma> <laboratorio> <nome do arquivo>

## Exemplo de uso
>     python3 testador.py mc102qrst 01 lab01.py
>     python3 testador.py mc202abc 00 lab00
### Obs:
* O script é compatível com versões do *Python* a partir da versão 3.5 
