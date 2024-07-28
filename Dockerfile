FROM python:3.9


# Copia os arquivos de requisitos e instala as dependências
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copia o código da aplicação para o contêiner
COPY ./app ./app

COPY ./.env ./.env


# Define o comando para iniciar a aplicação com as configurações especificadas
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8011"]

