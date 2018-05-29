# Testador em Python do Susy
## Objetivos 
A ideia do testador é agilizar a detecção de erros no código, evitar submissões incorretas e além de tudo provar os poderes da linguagem Python. 
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
