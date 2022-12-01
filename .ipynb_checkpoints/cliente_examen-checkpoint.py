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
                
                msg1 = input("Desea calcular la multiplicacion de matrices? -> **Si = 1 **No = 0")
                if msg1 == '1':
                
                    self.s.send(pickle.dumps(msg1))
            
                    A = [[random.randint(0,215) for i in range(data_arr[0])] for j in range(data_arr[1])] # Genero A[21535220][6]con num. aleatorios   
                    B = [[random.randint(0,215) for i in range(data_arr[2])] for j in range(data_arr[3])] # Genero B[6][21535220]con num. aleatorios 
    
                    n_fil_A = len(A) # Obtengo num de filas de A 
                    n_col_A = len(A[0]) # Obtengo num de colunmas de A 
                    n_fil_B = len(B) # Obtengo num de filas de B
                    n_col_B = len(B[0]) # # Obtengo num de filas de B
    
                    if n_col_A != n_fil_B: raise Exception('Dimensiones no validas') # Compruebo que se puedan multiplicar A y B
    
                    inicioS = time.time()
                    X = ('El resultado en secuencial es : ', self.sec_mult(A, B, n_fil_A, n_col_A, n_fil_B, n_col_B)) # Ejecuto multiplicacion secuencial
                    finS = time.time()
            
                    inicioP = time.time()
                    #Y = ('El resultado en paralelo es : ', self.par_mult(A, B, n_fil_A, n_col_A, n_fil_B, n_col_B)) # Ejecuto multiplicacion paralela
                    finP = time.time()
            
                    msg = (nick,X)
            
                    print('\n    ',msg)
                    self.enviar(msg)
            
                    print('\n\n    Matriz  A y B se han multiplicado con exito en SECUENCIAL ha tardado ', finS-inicioS)
                    print('\n\n    Matriz  A y B se han multiplicado con exito en PARALELO ha tardado ', finP-inicioP)
                    print('\n')
                
                else: pass
            

    def recibir(self):

            while True:
                try:
                        data = self.s.recv(4096)
                        data_arr = pickle.loads(data)
                        

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
        
    def par_mult(self, A, B, n_fil_A, n_col_A, n_fil_B, n_col_B): # f() que prepara el reparto de trabajo para la mult. en paralelo
        n_cores = mp.cpu_count() # Obtengo los cores de mi pc
        size_col = math.ceil(n_col_B/n_cores) # Columnas  a procesar x c/cpre, ver Excel adjunto
        size_fil = math.ceil(n_fil_A/n_cores) # Filas a procesar x c/cpre, ver Excel adjunto
        MC = mp.RawArray('i', n_fil_A * n_col_B) # Array MC de memoria compartida donde se almacenaran los resultados, ver excel adjunto
        cores = [] # Array para guardar los cores y su trabajo
    
        for core in range(n_cores):# Asigno a cada core el trabajo que le toca, ver excel adjunto
            i_MC = min(core * size_fil, n_fil_A) # Calculo i para marcar inicio del trabajo del core en relacion a las filas
            f_MC = min((core + 1) * size_fil, n_fil_A) # Calculo f para marcar fin del trabajo del core, ver excel
            cores.append(mp.Process(target=self.par_core, args=(A, B, MC, i_MC, f_MC)))# Añado al Array los cores y su trabajo
    
        for core in cores:
            core.start()# Arranco y ejecuto el trabajo para c/ uno de los cores que tenga mi equipo, ver excel
    
        for core in cores:
            core.join()# Bloqueo cualquier llamada hasta que terminen su trabajo todos los cores
        C_2D = [[0] * n_col_B for i in range(n_fil_A)] # Convierto el array unidimensional MC en una matrix 2D (C_2D) 
    
        for i in range(n_fil_A):# i para iterar sobre las filas de A
            for j in range(n_col_B):# j para iterar sobre las columnas de B
                C_2D[i][j] = MC[i*n_col_B + j] # Guardo el C_2D los datos del array MC
        return C_2D

    def par_core(self, A, B, MC, i_MC, f_MC): # La tarea que hacen todos los cores
        for i in range(i_MC, f_MC): # Size representado en colores en el excel que itera sobre las filas en A
            for j in range(len(B[0])): # Size representado en colores en el excel que itera sobre las columnas en B
                for k in range(len(A[0])): # n_fil_B o lo que es l mismo el n_col_A
                    MC[i*len(B[0]) + j] += A[i][k] * B[k][j]# Guarda resultado en MC[] de cada core


    
arrancar = Cliente()