import os
import multiprocessing
import hashlib
import base64
import csv

import utils as ut

def main(rootpath):
  pastas = os.listdir(rootpath)
  print(f'Pastas de fotos: {pastas}')

  ut.cria_pasta_dados()
  ut.cria_tb_tp_hash()
  ut.cria_tb_tp_img()

  filepath = os.path.join(ut.get_pasta_dados(), 'tb_fotos.csv')
  with open(filepath, mode='w') as f:
    header = ['cpf', 'hash', 'tp_hash', 'tp_img', 'img_base64']
    writer = csv.DictWriter(f, fieldnames=header)

    writer.writeheader()

    for p in pastas:
      path    = os.path.join(rootpath, p)
      n_files = len(os.listdir(path))
      print(f'Processando {n_files} arquivos de {path}')

      entradas = [(idx, filename, path) for idx, filename in enumerate(os.listdir(path))]
      print('Entradas preparadas.')

      with multiprocessing.Pool(ut.get_num_workers()) as p:
        res = p.starmap(ut.__worker_run, entradas)
        res = filter(lambda x: x is not None, res)

        writer.writerows(res)

rootpath = '/home/cesar/workspace/dados/fotos'
main(rootpath)