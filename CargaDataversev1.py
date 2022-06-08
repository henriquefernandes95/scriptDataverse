#CargaDataversev0
#from google.colab import files
import glob, os
from pickle import PERSID

from zipfile import *

import json
import requests



def defType(extension):#retorna o tipo de arquivo
  if(extension=="R" or extension=="py" or extension=="c" or extension=="cpp"):
    return "/script"
  else:
    return "/data"


def loadFile(filename,arquivo,persID):#com base no código fornecido pelo Dataverse
  # --------------------------------------------------
  # Update the 4 params below to run this code
  # --------------------------------------------------
  dataverse_server = 'http://172.16.16.119:8080' # ip do servidor para as requisições
  api_key = '1387b05b-a5c5-46c5-b960-e3c9a2696264'
  persistentId='doi:'+persID
  # --------------------------------------------------
  # Prepare "file"
  # --------------------------------------------------
  files = {'file': (filename, arquivo)}

  # --------------------------------------------------
  # Using a "jsonData" parameter, add optional description + file tags
  # --------------------------------------------------
  extension = os.path.splitext(filename)[-1].replace(".","")
  extpath=defType(extension)
  params = dict(description='File2!', directoryLabel=extpath,categories=[extension, 'TEST'])
  params_as_json_string = json.dumps(params)
  print(params_as_json_string)
  payload = dict(jsonData=params_as_json_string)


  # --------------------------------------------------
  # Add file using the Dataset's persistentId (e.g. doi, hdl, etc)
  # --------------------------------------------------
  url_persistent_id = '%s/api/datasets/:persistentId/add?persistentId=%s&key=%s' % (dataverse_server, persistentId, api_key)


  # -------------------
  # Make the request
  # -------------------
  print ('-' * 40)
  print ('making request: %s' % url_persistent_id)
  r = requests.post(url_persistent_id, data=payload, files=files)

  # -------------------
  # Print the response
  # -------------------
  print ('-' * 40)
  print (r.json())
  print (r.status_code)


def acessaCont(caminho):#varre os diretórios de forma recursiva, acionando a carga com os arquivos
  basepath = caminho
  for elemento in os.listdir(basepath):
    if os.path.isdir(os.path.join(basepath, elemento)):
      acessaCont(os.path.join(basepath, elemento))
    else:
      persID=basepath.replace("./","")#remove o início do caminho para formar o doi
      persID=persID.replace("\\","/")#troca a posição das barras para a adequada
      arq = open(basepath.replace("./",".\\")+"\\"+elemento, "rb")
      loadFile(elemento,arq,persID)

acessaCont("./")#Executa o processo no local onde está sendo executado o script