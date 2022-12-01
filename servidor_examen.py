import socket
import threading
import sys
import pickle
import os

class Servidor():

    def __init__(self, host=socket.gethostname(), port=int(input("Que puerto quiere usar ? "))):
        
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

        self.clientes = []
        
        print('\n\tSu IP actual es : ',socket.gethostbyname(host))
        print('\n\tProceso con PID = ',os.getpid(), '\n\tHilo PRINCIPAL con ID =',threading.current_thread().name, '\n\tHilo en modo DAEMON = ', threading.current_thread().isDaemon(), 
              '\n\tHilos activos en este punto del programa =', threading.active_count())
        
        self.s = socket.socket()
        self.s.bind((str(host), int(port)))
        self.s.listen(30)
        self.s.setblocking(False)

        threading.Thread(target=self.aceptarC, daemon=True).start()
        threading.Thread(target=self.procesarC, daemon=True).start()

        while True:
            msg = input('\n << SALIR = 1 >> \n')
            if msg == '1':
                print("Me piro del servidor, cierro socket y mato SERVIDOR con PID = ", os.getpid())
                self.s.close()
                sys.exit()
            else: pass

    def aceptarC(self):
        print('\nHilo ACEPTAR con ID =',threading.current_thread().name, '\n\tHilo en modo DAEMON = ', threading.current_thread().isDaemon(),'\n\tPertenece al PROCESO con PID', os.getpid(), "\n\tHilos activos TOTALES ", threading.active_count())

        while True:
            try:
                conn, addr = self.s.accept()
                print(f"\nConexion aceptada via {addr}\n")
                conn.setblocking(False)
                self.clientes.append(conn)
            except: pass

    def procesarC(self):
        print('\nHilo PROCESAR con ID =',threading.current_thread().name, '\n\tHilo en modo DAEMON = ', threading.current_thread().isDaemon(),'\n\tPertenece al PROCESO con PID', os.getpid(), "\n\tHilos activos TOTALES ", threading.active_count())
        while True:
            if len(self.clientes) > 0:
                for c in self.clientes:
                    try:
                        data = c.recv(32)
                        if data: self.broadcast(data,c)
                    except: pass

    def broadcast(self, msg, cliente):
        for c in self.clientes:
            print("Clientes conectados ahora = ", len(self.clientes))
            print(pickle.loads(msg))
            try:
                if c != cliente: 
                    print(pickle.loads(msg))
                    c.send(msg)
            except: self.clientes.remove(c)

arrancar = Servidor() 