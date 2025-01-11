# teste-poc-idade-simples
PoC em Python para cruzamento de dados de idade, sexo e ano

# Estrutura do código
## Objetivo
- O código deve ler um arquivo xlsx e fazer um cruzamento entre:
-- SEXO x LOCAL 
-- LOCAL x IDADE
-- SEXO x IDADE

## Arquivo
- O arquivo é uma planilha no formato xlsx.
- Os dados válidos para cruzamento começam a partir da linha 5 (cabecalho)

## Classes
- A classe BuildDF reune os parâmetros necessários para criar o dataframe.
- O dataframe é criado em chunks para otimizar o desempenho.
- A classe DbConnect reune os métodos para conexão ao db PostgreSQL
- A classe DataCrossing cria os objetos da classe BuildDF e roda os cruzamentos de dados.
- A classe MemoryUse possui os metodos para monitorar o consumo de memoria na execução do código.

## Critérios
- O arquivo é carregado utilizando o openpyxl.
- Cada chunk corresponde a 1 dataframe.
- A lista de dataframes criada é concatenada em 1 dataframe final.
- O yield é um gerador que permite processar os chunks vez por vez na memória.

## Método
- Os cruzamentos são agrupamentos com a soma do valor total de anos para cada combinação.

### Cruzamento SEXO x LOCAL
- Significa que para cada sexo e local há um total de casos somados entre os anos 2000 e 2070.

### Cruzamento LOCAL x IDADE
- Significa que para cada individuo com certa idade em um local há um total de casos somados entre os anos 2000 e 2070.

### Cruzamento SEXO x IDADE
- Significa que para cada sexo de indivído e idade há um total de casos somados entre os anos de 2000 e 2070.

# Explicação
- O código usa a função groupby() do Pandas para agrupar as combinações
- O código usa a função agg() para somar os valores de todos os anos de cada cruzamento.
- O .reset_index() é usado para que a soma dos anos seja uma coluna normal e não um índice.