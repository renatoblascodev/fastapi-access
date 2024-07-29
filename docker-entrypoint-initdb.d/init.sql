-- Verifica se o banco de dados "acesso" existe
DO $$
BEGIN
    IF NOT EXISTS (SELECT FROM pg_database WHERE datname = 'acesso') THEN
        -- Cria o banco de dados se ele não existir
        EXECUTE 'CREATE DATABASE acesso';
    END IF;
END
$$;

-- Verifica se o usuário "postgres" existe
DO $$
BEGIN
    IF NOT EXISTS (SELECT FROM pg_catalog.pg_user WHERE usename = 'postgres') THEN
        -- Cria o usuário se ele não existir
        EXECUTE 'CREATE USER postgres WITH PASSWORD ''Yuri100100''';
    END IF;
END
$$;

-- Concede permissões ao usuário no banco de dados, se ele existir
DO $$
BEGIN
    IF EXISTS (SELECT FROM pg_database WHERE datname = 'acesso') AND 
       EXISTS (SELECT FROM pg_catalog.pg_user WHERE usename = 'postgres') THEN
        -- Concede todas as permissões no banco de dados "acesso" ao usuário "postgres"
        EXECUTE 'GRANT ALL PRIVILEGES ON DATABASE acesso TO postgres';
    END IF;
END
$$;