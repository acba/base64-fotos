import os
import multiprocessing
import hashlib
import base64
import csv

DATA_PATH = './data'

N_WORKERS = 8

TP_HASH = {
  'NONE': 0,
  'SHA256': 1,
  'SHA1': 2,
  'MD5': 3
}

TP_IMG = {
  'NONE': 0,
  'FACE': 1,
  'ASSINATURA': 2,
}

def get_tp_hash(de_hash):
  ''' Retorna o tipo de hash '''
  return TP_HASH[de_hash.upper()]

def get_tp_img(de_img):
  ''' Retorna o tipo de imagem '''
  return TP_IMG[de_img.upper()]

def get_num_workers():
  ''' Retorna o numero de workers processando em paralelo '''
  return N_WORKERS

def get_pasta_dados():
  ''' Retorna a pasta que contem os dados processados '''
  return DATA_PATH

def read_img(filepath):
  ''' Retorna o conteudo em binario da imagem '''

  with open(filepath, "rb") as f:
    return f.read()


def cria_pasta_dados():
  ''' Cria a pasta de dados processados '''

  dados_path = get_pasta_dados()
  if not os.path.exists(dados_path):
    os.makedirs(dados_path)

def cria_tb_tp_hash():
  ''' Gera um arquivo csv contendo o dicionario para o tipo de hash '''

  filepath = os.path.join(get_pasta_dados(), 'tb_tp_hash.csv')

  with open(filepath, mode='w') as f:
    header = ['tp_hash', 'de_hash']
    writer = csv.DictWriter(f, fieldnames=header)

    writer.writeheader()
    writer.writerow({'tp_hash': TP_HASH['NONE'],    'de_hash': 'NONE'})
    writer.writerow({'tp_hash': TP_HASH['SHA256'],  'de_hash': 'SHA256'})
    writer.writerow({'tp_hash': TP_HASH['SHA1'],    'de_hash': 'SHA1'})
    writer.writerow({'tp_hash': TP_HASH['MD5'],     'de_hash': 'MD5'})

def cria_tb_tp_img():
  ''' Gera um arquivo csv contendo o dicionario para o tipo de imagem '''

  filepath = os.path.join(get_pasta_dados(), 'tb_tp_img.csv')

  with open(filepath, mode='w') as f:
    header = ['tp_img', 'de_img']
    writer = csv.DictWriter(f, fieldnames=header)

    writer.writeheader()
    writer.writerow({'tp_img': TP_IMG['NONE'],       'de_img': 'NONE'})
    writer.writerow({'tp_img': TP_IMG['FACE'],       'de_img': 'FACE'})
    writer.writerow({'tp_img': TP_IMG['ASSINATURA'], 'de_img': 'ASSINATURA'})

def decide_tp_img(filename):
  ''' Retorna o tipo da imagem processada '''

  if filename.endswith("-F.jpg"):
    tp_img = get_tp_img('FACE')
  elif filename.endswith("-A.jpg"):
    tp_img = get_tp_img('ASSINATURA')
  else:
    tp_img = get_tp_img('NONE')

  return tp_img

def converte_img_base64(img):
  ''' Retorna o codigo base64 da imagem '''
  return base64.b64encode(img).decode('utf-8')

def __worker_run(idx, filename, path):
  ''' Retorna um dicionario com os dados processados pelo worker para cada imagem '''

  if filename.endswith(".jpg"):
    filepath = os.path.join(path, filename)

    cpf = filename.split('-')[0]
    img = read_img(filepath)
    hash = hashlib.sha256(img).hexdigest().upper()
    tp_hash = get_tp_hash('SHA256')
    tp_img = decide_tp_img(filename)
    img_base64 = converte_img_base64(img)

    return {
      'cpf': cpf,
      'tp_img': tp_img,
      'hash': hash,
      'tp_hash': tp_hash,
      'img_base64':img_base64
    }
  else:
    print(f'Arquivo não identificado: {filename}')

  return None