# Usar uma imagem base do Python
FROM python:3.11

# Definir o diretório de trabalho dentro do container
WORKDIR /app

# Copiar os arquivos do projeto
COPY ./src /app

# Instalar as dependências
RUN pip install -r requirements.txt

# Comando para executar o script principal
CMD ["python", "app.py"]
