# 📇 Agenda de Contatos CLI (Python)

Sistema de gerenciamento de contatos desenvolvido como projeto final da disciplina de **Lógica de Programação II**. O sistema utiliza uma interface de linha de comando (CLI) robusta, colorida e interativa para realizar operações CRUD completas com persistência em arquivos CSV.

## 🚀 Funcionalidades

- **CRUD Completo:**
    - **C**reate: Adição de novos contatos com validação.
    - **R**ead: Visualização de contatos com paginação e busca inteligente.
    - **U**pdate: Edição de contatos existentes.
    - **D**elete: Remoção de registros com confirmação.
- **Validação Inteligente:** Uso de Expressões Regulares (Regex) para validar:
    - Nomes (apenas letras e acentuação).
    - E-mails (formato padrão RFC).
    - Telefones (formatos comuns).
- **Interface Premium:**
    - Cores em degradê via True Color ANSI.
    - Menu interativo e intuitivo.
    - Limpeza automática do console entre ações.
- **Persistência de Dados:** Armazenamento automático em arquivo `agenda.csv` com ordenação alfabética automática.

## 🛠️ Tecnologias Utilizadas

- **Linguagem:** Python 3
- **Bibliotecas Nativas:**
    - `re`: Validação via Regex.
    - `csv`: Manipulação da base de dados.
    - `subprocess` & `sys`: Controle de interface e limpeza de tela.
    - `argparse`: (Preparado para expansão).

## 📂 Estrutura do Projeto

- `main.py`: Ponto de entrada da aplicação.
- `ui.py`: Gerenciamento da interface visual e menus.
- `contatos.py`: Lógica de validação e processamento de dados.
- `arquivo.py`: Camada de persistência e manipulação do CSV.

## 📖 Como Executar

1. Certifique-se de ter o Python 3 instalado.
2. Clone este repositório.
3. Execute o comando:
   ```bash
   python main.py
   ```

---
**Autor:** Jeronimo Silva  
**Status:** Finalizado e Entregue (Maio/2026)
