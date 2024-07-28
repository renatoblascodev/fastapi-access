-- Cria um novo usuário
CREATE USER postgres WITH PASSWORD 'Yuri100100';

-- Cria um banco de dados
CREATE DATABASE acesso;

-- Concede permissões ao usuário no banco de dados
GRANT ALL PRIVILEGES ON DATABASE acesso TO postgres;