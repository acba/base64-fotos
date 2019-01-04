# base64-fotos

Aplicação que converte as imagens da base em arquivos csv para serem importados no banco de dados.

## 1. Arquivos gerados

### 1.1 tb_fotos.csv

Colunas

1. *cpf* - **CHAR(11)**
2. *tp_hash* - **INT** - Tipo de hash utilizado
3. *hash* - **CHAR(64)** - Valor do Hash
4. *tp_img* - **INT** - Tipo de imagem salva
5. *img_base64* - **VARCHAR(1416501)** - Imagem codificada em base64, esse tamanho representa o valor máximo para imagens de **1MB**
    * Atualmente no nosso conjunto de imagens a de maior tamanho apresenta 56KB.

### 1.2 tb_tp_hash.csv

2. *tp_hash* - **INT** - Tipo de hash utilizado
3. *de_hash* - **CHAR(64)** - Descrição do Hash

### 1.3 tb_tp_img.csv

2. *tp_img* - **INT** - Tipo de imagem
3. *de_img* - **CHAR(64)** - Descrição da imagem

## 2. Execução

```
  $ virtualenv venv
  $ source venv/bin/activate
  $ python run.py
```