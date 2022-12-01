import threading
import sys
import socket
import pickle
import os
import random # Para generar num. aleatorios en la A y B 
import math
import multiprocessing as mp # Para trabajar en paralelo
import time

class Cliente():

    def __init__(self, host=input("Introduzca la IP del Servidor: "), port=int(input("Introduzca el puerto del servidor: ")), nick=input('Introduzca su Nickname: ')):
            
            c = """
    
    ██████╗ ██╗  ██╗██████╗  ██████╗ 
    ██╔══██╗██║ ██╔╝╚════██╗██╔════╝ 
    ██║  ██║█████╔╝  █████╔╝███████╗ 
    ██║  ██║██╔═██╗  ╚═══██╗██╔═══██╗
    ██████╔╝██║  ██╗██████╔╝╚██████╔╝
    ╚═════╝ ╚═╝  ╚═╝╚═════╝  ╚═════╝ 
    Developer: Diego Rodriguez Sanz
    Nº Expediente: 22167749
                                                                           
                                            
                                                              
            """
            print(c)
            
            self.s = socket.socket()
            self.s.connect((host, int(port)))
            
            print('\n    Proceso con PID = ',os.getpid(), '\n    Hilo Principal con ID = ',threading.current_thread().name, '\n    Hilo en Modo DAEMON=FALSE',
                  '\n    Hilos activos en este punto de programa = ', threading.active_count())

            threading.Thread(target=self.recibir, daemon=True).start()
            
            while True:
            
            A = [[1 for i in range(4)] for j in range(4)] # Genero A[21535220][6]con num. aleatorios del 0 al 215, ver excel 
            B = [[1 for i in range(4)] for j in range(4)] # Genero B[6][21535220]con num. aleatorios del 0 al 215, ver excel
    
            n_fil_A = len(A) # Obtengo num de filas de A 
            n_col_A = len(A[0]) # Obtengo num de colunmas de A 
            n_fil_B = len(B) # Obtengo num de filas de B
            n_col_B = len(B[0]) # # Obtengo num de filas de B
    
            if n_col_A != n_fil_B: raise Exception('Dimensiones no validas') # Compruebo que se puedan multiplicar A y B
    
            inicioS = time.time()
            X = self.sec_mult(A, B, n_fil_A, n_col_A, n_fil_B, n_col_B) # Ejecuto multiplicacion secuencial
            finS = time.time()
            msg = (nick,X)
            print('\n    ',msg)
            self.enviar(msg)
            
            print('\n\n    Matriz  A y B se han multiplicado con exito en SECUENCIAL ha tardado ', finS-inicioS)
            print('    El resultado de la multiplicación de matrices de manera secuencial es = ', X)
            print('\n')

    def recibir(self):

            while True:
                try:
                        data = self.s.recv(4096)
                        if data: data_arr = pickle.loads(data)
                        

                except: print('ERROR: Mensaje demasiado grande')

            
    def enviar(self,msg):
        self.s.send(pickle.dumps(msg))
        
        
    def sec_mult(self, A, B, n_fil_A, n_col_A, n_fil_B, n_col_B): # f() que calcula la mult. en secuencial, como toda la vida se ha hecho 
        C = [[0] * n_col_B for i in range(n_fil_A)] # Crear y poblar la matrix  C = A*B
        for i in range(n_fil_A): # Hago la multiplicacion de AxB = C, i para iterar sobre las filas de A
            for j in range(n_col_B): # j para iterar sobre las columnas de B
                for k in range(n_col_A): # k para iterar en C
                    C[i][j] += A[i][k] * B[k][j] # Aqui se hace la multiplicación y guardo en C.
        return C
        

    
arrancar = Cliente()