-- Banco de Dados
USE BD240226114;

-- Tabela de funcionários
CREATE TABLE funcionarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    cargo VARCHAR(50)
);

-- Tabela de processos
CREATE TABLE processos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    descricao VARCHAR(200) NOT NULL,
    urgencia INT,
    id_funcionario INT,

    FOREIGN KEY (id_funcionario)
        REFERENCES funcionarios(id)
);
