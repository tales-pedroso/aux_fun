# Projeto Graviola 
==============================================================

## O que é?

Um projeto de automação que foi usado em um processo no IBGE. Trata-se de um RPA (Robotic Process Automation) feito para o Departamento de Orçamento e Finanças. Resumidamente, ele substitui um ser humano ao extrair informação de um pdf e lançá-la no Siafi (sistema de pagamentos do Governo Federal). Usado como prova de conceito para um programa maior de automação dentro da empresa. 

## Veja o Graviola em ação
https://www.youtube.com/watch?v=QTp-RSuUNtI
(vídeo de 1:30 - se meu sotaque for difícil de entender, é só ligar a legenda)

## E funciona?

Sim! 

## Como funciona?

Extrai a string de um pdf; usa regex para extrair as partes importantes da string; usa Selenium para preencher os formulários do Siafi.

## Quero ver o código, por onde é melhor começar?

Por pipeline.py para ver o processamento dos dados. Ou por dh_creation.py, se quiser ver a parte do RPA (Selenium).

## Mas o código não está comentado

Como o programa só é útil para o pessoal do IBGE, eu foquei em escrever só para funcionar. Eu era o único que programava da equipe, então não valia a pena descrever todas as funções.

## E vai ter continuidade?

Não, este projeto está encerrado.

## Dependências

- geckodriver 0.30.0 (https://github.com/mozilla/geckodriver/releases)
- Mozilla Firefox 94.0.1

## Como executar?

É preciso ter credenciais do Siafi (CPF e senha) e inseri-las em main.py.

## Algo mais?

Por lei, dados financeiros do Governo Federal são públicos e podem ser consultados no Portal da Transparência: https://www.portaltransparencia.gov.br/
