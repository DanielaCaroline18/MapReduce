# -*- coding: utf-8 -*-
import mincemeat
import glob
import csv
import string
import os

caminho = 'C:\\Users\\danie\\Documents\\Aulas\\dani\\TrabalhoPos\\TRAB1\\Trab2.3\\'
text_files = glob.glob(os.path.join(caminho,'*'))

#glob.glob('C:\\Users\\danie\\Documents\\Aulas\\dani\\TrabalhoPos\\TRAB1\\Trab2.3\\*')

def file_contents(file_name):
	f = open(file_name, 'r')
	try:
		return f.read()
	finally:
		f.close()
		
source = dict((file_name, file_contents(file_name))for file_name in text_files)

def retirarPontuacaoTitulo(titulo):
    return ' '.join(word.strip(string.punctuation) for word in titulo.split())

def retirarStopWordsTitulo(titulo):
    tituloSeparado = ""
    
    from stopwords import allStopWords
    for word in titulo.split():
        if (word not in allStopWords):
            tituloSeparado += word + ":"
            print (tituloSeparad)
    return tituloSeparado
    
def obterListaDeAutores(autores):
    return autores.split('::')
    
def mapfn(k, v):
    print ('map '+ k)
    for line in v.splitlines():  
       titulo = line.split(':::')[2] 
       tituloSemPotuacao = ' '.join(word.strip('!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~') for word in titulo.split())
       tituloSeparado = ""    
       listaDeAutores = line.split(':::')[1].split('::')        
       from stopwords import allStopWords
       for word in tituloSemPotuacao.split():
          if (word not in allStopWords):
            for autor in listaDeAutores:             
               yield autor, word
				
def reducefn(k, v):
    print ('reduce ' + k) 
    listaPalavras = list()    
    for index, item in enumerate(v):
       listaPalavras.append(item)        
       
    from collections import Counter
    contador = Counter(listaPalavras)
    
    return contador
    
	 
s= mincemeat.Server()
s.datasource = source
s.mapfn =  mapfn
s.reducefn = reducefn

results =  s.run_server(password = "changeme")

w= csv.writer(open("C:\\Users\\danie\\Documents\\Aulas\\dani\\TrabalhoPos\\TRAB1\\RESULT_trab1.csv", "w"))
for k, v in results.items():
    if (str(k) == 'Grzegorz Rozenberg') | (str(k) == 'Philip S. Yu'):
      print ('\n')
      print ('As duas palavras que mais ocorrem para o autor '+ k + ':')
      print (v.most_common(2))
    w.writerow([k, str(v).replace('Counter(', "").replace(')', "")])