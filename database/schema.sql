-- ==============================================================================
-- Projeto Integrador 1 - SCSC
-- Aluno: Jorge Rodrigues dos Santos Neto
-- Script de Criação e Povoamento do Banco de Dados (DDL + DML)
-- ==============================================================================

-- 1. Aponta para o seu schema do servidor da faculdade
USE BD240226114;

-- 2. Limpeza prévia (Se rodar o script 2x, ele não dá erro)
DROP TABLE IF EXISTS solicitacoes;
DROP TABLE IF EXISTS usuarios;

-- ==============================================================================
-- ESTRUTURA (DDL)
-- ==============================================================================

CREATE TABLE usuarios (
    id_usuario INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL, 
    perfil ENUM('solicitante', 'operador', 'tecnico') NOT NULL
);

CREATE TABLE solicitacoes (
    id_solicitacao INT AUTO_INCREMENT PRIMARY KEY,
    id_solicitante INT NOT NULL,
    categoria VARCHAR(50) NOT NULL,
    descricao TEXT NOT NULL,
    fator_urgencia INT NOT NULL,
    fator_impacto INT NOT NULL,
    prioridade VARCHAR(20) NOT NULL, 
    status ENUM('Aberta', 'Em andamento', 'Fechada') DEFAULT 'Aberta',
    data_abertura DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_solicitante) REFERENCES usuarios(id_usuario)
);

-- ==============================================================================
-- DADOS PARA O TESTE DO PROFESSOR (DML)
-- ==============================================================================

INSERT INTO usuarios (nome, email, perfil) VALUES
('Ana Silva', 'ana.silva@empresa.com', 'solicitante'),
('Carlos Operador', 'carlos.op@empresa.com', 'operador'),
('Roberto Técnico', 'roberto.ti@empresa.com', 'tecnico');

INSERT INTO solicitacoes (id_solicitante, categoria, descricao, fator_urgencia, fator_impacto, prioridade, status) VALUES
(1, 'Hardware', 'O monitor da mesa 04 está piscando e apagando.', 3, 2, 'Alta', 'Aberta'),
(2, 'Manutenção', 'Ar condicionado da recepção pingando água.', 1, 1, 'Baixa', 'Aberta'),
(3, 'Rede', 'Cabo de rede rompido no laboratório.', 2, 2, 'Média', 'Em andamento');
