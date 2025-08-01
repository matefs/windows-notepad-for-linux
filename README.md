# Bloco de Notas Python

Este projeto é um bloco de notas simples feito em Python com interface gráfica usando Tkinter.

## Pré-requisitos

- Python 3.9 ou superior
- [uv](https://github.com/astral-sh/uv) (gerenciador de dependências rápido)
- [cx_Freeze](https://pypi.org/project/cx-Freeze/) (para gerar executável)

## Instalação das dependências

1. Instale o `uv` (caso ainda não tenha):

   ```sh
   pip install uv
   ```

2. Instale as dependências do projeto:

   ```sh
   uv pip install -r requirements.txt
   ```

   > Se não houver um arquivo `requirements.txt`, crie um com o seguinte conteúdo:
   > ```
   > cx_Freeze
   > ```

## Executando o projeto

Para rodar diretamente com Python:

```sh
python main.py
```

## Gerando o executável com cx_Freeze

1. Instale o `cx_Freeze` (caso ainda não tenha):

   ```sh
   uv pip install --upgrade cx_Freeze
   ```

2. Gere o executável:

   ```sh
   cxfreeze --script main.py --target-dir dist
   ```

   O executável será criado na pasta `dist`.

## Observações

- No Linux, pode ser necessário instalar dependências do sistema para o Tkinter funcionar:
  ```sh
  sudo apt-get install python3-tk
  ```
- Para rodar o executável, basta executar o arquivo gerado na pasta `dist`.

---