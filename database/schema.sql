CREATE DATABASE IF NOT EXISTS projetoIntegrador;

USE projetoIntegrador;

DROP TABLE IF EXISTS solicitacoes;
DROP TABLE IF EXISTS usuarios;

CREATE TABLE usuarios (
    id_usuario INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    perfil ENUM(
        'solicitante',
        'operador',
        'tecnico'
    ) NOT NULL
);

CREATE TABLE solicitacoes (
    id_solicitacao INT AUTO_INCREMENT PRIMARY KEY,
    id_solicitante INT NOT NULL,
    id_responsavel INT,
    categoria VARCHAR(50) NOT NULL,
    descricao TEXT NOT NULL,
    fator_urgencia INT NOT NULL,
    fator_impacto INT NOT NULL,
    prioridade VARCHAR(20) NOT NULL,

    status ENUM(
        'Aberta',
        'Em andamento',
        'Fechada'
    ) DEFAULT 'Aberta',

    data_abertura DATETIME DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (id_solicitante)
    REFERENCES usuarios(id_usuario),

    FOREIGN KEY (id_responsavel)
    REFERENCES usuarios(id_usuario)
);

INSERT INTO usuarios(nome, email, perfil)
VALUES
('Ana Silva', 'ana@empresa.com', 'solicitante'),
('Carlos Operador', 'carlos@empresa.com', 'operador'),
('Roberto Técnico', 'roberto@empresa.com', 'tecnico');
