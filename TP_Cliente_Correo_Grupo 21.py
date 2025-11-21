class Servidor:
    def __init__(self,direccion):
        self.direccion=direccion
        self.usuarios = []
    
    def registrar_registrar(self, usuario):
        self.usuarios.append(usuario)
    
    def ingresar_usuario(self, direccion, contrasenia):
        for dato in self.usuarios:
            if direccion == dato.correo:
                if contrasenia == dato.contrasenia:
                    return dato
        return False
    
    def enviar_msj(self, usuario, mensaje):
        receptor = mensaje.receptor
        print("\nEl receptor es {}".format(receptor))
        for dato in self.usuarios:
            if dato.correo == receptor:
                dato.buzon.mensajes.append(mensaje) 
                print("\nEl mensaje se envió con éxito.")
                usuario.enviados.mensajes.append(mensaje) 
                return 
        print("\nEl usuario {} no existe,".format(mensaje.receptor))

class Usuario:
    def __init__(self, correo, contrasenia):
        self.correo = correo
        self.contrasenia = contrasenia
        self.carpeta_raiz = Carpeta("Raiz")
        self.buzon = Carpeta("Buzón de entrada")
        self.enviados = Carpeta("Enviados")
        # Se agrega las carpetas buzon y enviados a la raiz para poder imprimirlas
        self.carpeta_raiz.agregar_carpeta(self.buzon)
        self.carpeta_raiz.agregar_carpeta(self.enviados)  
        # Se crea la cola de prioridades por usuario
        self.cola_mensajes_urgentes=ColaDePrioridades()
        self.reglas_filtro = {}
    #Funcion para poder cargar los msj urgentes al principio del buzon
    def desencolar_mensajes_urgentes(self):
        mensajes_nuevos = []
        while True:
            mensaje_actual = self.cola_mensajes_urgentes.desencolar()
            if mensaje_actual is None:
                break
            mensajes_nuevos.append(mensaje_actual)
        self.buzon.mensajes=mensajes_nuevos + self.buzon.mensajes
    # Metodos para agregar reglas
    def agregar_regla_filtro(self, nombre_carpeta, tipo_filtro, valor_a_buscar):
        tipo_filtro = tipo_filtro.lower()
        if tipo_filtro not in ["asunto", "remitente"]:
            print(" ERROR: El tipo de filtro debe ser 'asunto' o 'remitente'.")
            return
        if nombre_carpeta in self.reglas_filtro:
            self.reglas_filtro[nombre_carpeta].append((tipo_filtro, valor_a_buscar.lower()))
        else:
            self.reglas_filtro[nombre_carpeta]=[]
            self.reglas_filtro[nombre_carpeta].append((tipo_filtro, valor_a_buscar.lower()))
        if not self.carpeta_raiz.encontrar_carpeta(nombre_carpeta):
            nueva_carpeta = Carpeta(nombre_carpeta)
            self.carpeta_raiz.agregar_carpeta(nueva_carpeta)
            print("Regla agregada y Carpeta '{}' creada.".format(nombre_carpeta))
        else:
            print("Regla para '{}' actualizada.".format(nombre_carpeta))
    # Metodo para aplicar las reglas al buzón de entrada
    def aplicar_filtros_a_buzon(self):
        mensajes_para_revisar = self.buzon.mensajes.copy()
        self.buzon.mensajes = []
        for mensaje in mensajes_para_revisar:
            mensaje_clasificado = False
            for nombre_carpeta, regla in self.reglas_filtro.items():
                for reglas in regla:
                    tipo_filtro = reglas[0]
                    valor_esperado = reglas[1]
                    valor_real = ""
                    if tipo_filtro == "asunto":
                        valor_real = mensaje.asunto.lower()
                    elif tipo_filtro == "remitente":
                        valor_real = mensaje.remitente.lower()
                    if valor_esperado in valor_real:
                        carpeta_destino = self.carpeta_raiz.encontrar_carpeta(nombre_carpeta)
                        if carpeta_destino:
                            carpeta_destino.agregar_mensaje(mensaje)
                            mensaje_clasificado = True
                            break
            if not mensaje_clasificado:
                self.buzon.mensajes.append(mensaje)
    def mostrar_filtros(self):
        print("\n--REGLAS DE FILTRO--")
        if not self.reglas_filtro:
            print("\nNo hay filtros")
            return
        
        for self.nombre_carpeta, datos in self.reglas_filtro.items():
            print("CARPETA:", self.nombre_carpeta)
            for dato in datos:
                tipo_filtro, valor = dato                
                print("---asunto/remitente:", tipo_filtro)
                print("---palabra clave:", valor)
                
    def borrar_filtros(self):
        borrado = input("\nNombre de el asunto o remitente a borrar filtro: ")
        if not self.reglas_filtro:
            print("\nNo hay filtros")
            return
        for self.nombre_carpeta, datos in self.reglas_filtro.items():
            for dato in datos:
                tipo_filtro, valor = dato
                if valor==borrado:
                    datos.remove(dato)
                    print("El filtro fue borrado.")                                
        print(self.reglas_filtro)
class Mensaje:
    def __init__(self, remitente, receptor, asunto, cuerpo,urgencia=""):
        self.remitente = remitente
        self.receptor = receptor
        self.asunto = asunto
        self.cuerpo = cuerpo
        # Solo es un detalle
        self.urgencia = urgencia 
           
    def __str__(self):
        return "[{}]De: {}\nPara: {}\nAsunto: {} \nMensaje: {}\n".format(self.urgencia,self.remitente, self.receptor, self.asunto, self.cuerpo)
# Se implementó la Clase Carpeta para crear el árbol de carpetas y administrar los mensajes
class Carpeta():
    def __init__(self, nombre):
        self.nombre = nombre
        self.mensajes = [] 
        self.lista_carpetas = [] 

    def agregar_carpeta(self, carpeta):
        self.lista_carpetas.append(carpeta)

    def agregar_mensaje(self, mensaje):
        self.mensajes.append(mensaje)

    def arbol_carpetas(self, nivel=0):
        contador = "  " * nivel
        print("{} ├── {}".format(contador, self.nombre))
        for carpeta in self.lista_carpetas: 
            carpeta.arbol_carpetas(nivel + 1)

    def mostrar_carpetas_con_msj(self, nivel=0):
        contador = "  " * nivel
        print("{} ├── {} ({} mensajes)".format(contador, self.nombre, len(self.mensajes)))
        for msj in self.mensajes:
            print("{} ├── {} {}".format(contador, msj.asunto,msj.receptor))
        for carpeta in self.lista_carpetas:
            carpeta.mostrar_carpetas_con_msj(nivel + 1)

    def agregar_carpeta_en(self, carpeta_a_agregar, n_c_destino):
        if self.nombre == n_c_destino:
            self.lista_carpetas.append(carpeta_a_agregar)
            return True
        for car in self.lista_carpetas:
            if car.agregar_carpeta_en(carpeta_a_agregar, n_c_destino):
                return True
        return False
    
    # Metodo para eliminar el primer mensaje con el asunto dado
    def encontrar_carpeta(self, nombre_carpeta):
        if self.nombre == nombre_carpeta:
            return self
        
        for carpeta in self.lista_carpetas:
            encontrada = carpeta.encontrar_carpeta(nombre_carpeta)
            if encontrada:
                return encontrada        
        return None 
    
    def eliminar_mensaje_por_asunto(self, asunto):
        mensaje_eliminado = None
        nueva_lista_mensajes = []
        eliminado = False

        for mensaje in self.mensajes:
            if mensaje.asunto == asunto and not eliminado:
                mensaje_eliminado = mensaje
                eliminado = True
            else:
                nueva_lista_mensajes.append(mensaje)            
        if mensaje_eliminado is not None:
            self.mensajes = nueva_lista_mensajes        
        return mensaje_eliminado          
    
    def buscar_y_extraer_mensaje(self,asunto):
        mensaje = self.eliminar_mensaje_por_asunto(asunto)
        if mensaje:
            return mensaje
        for carpeta in self.lista_carpetas:
            mensaje = carpeta.buscar_y_extraer_mensaje(asunto)
            if mensaje:
                return mensaje
        return None
    
    def mover_mensaje(self, asunto, destino):
        mensaje = self.buscar_y_extraer_mensaje(asunto)        
        if mensaje is None:
            return None  
        carpeta_destino = self.encontrar_carpeta(destino)
        
        if carpeta_destino is None:
            return False
        carpeta_destino.agregar_mensaje(mensaje)        
        return True 
# Cola de prioridades Nodo 
class Nodo:
    def __init__(self,mensaje, prioridad):
        self.mensaje=mensaje
        self.prioridad=prioridad
        self.siguiente=None

class ColaDePrioridades:
    def __init__(self):
        self.frente = None
    def encolar(self, mensaje, prioridad):
        #detalle solamente
        mensaje.urgencia="!"
        nuevo = Nodo(mensaje, prioridad)
        # Si la cola está vacía o el nuevo es más urgente que el primero:
        if self.frente is None or prioridad < self.frente.prioridad:
            nuevo.siguiente = self.frente
            self.frente = nuevo
        else:
            actual = self.frente
 # buscamos el lugar correcto según la prioridad
            while (actual.siguiente is not None and
                actual.siguiente.prioridad <= prioridad):
                actual = actual.siguiente
            nuevo.siguiente = actual.siguiente
            actual.siguiente = nuevo
    def desencolar(self):
        if self.frente is None:
            return None
        mensaje = self.frente.mensaje
        self.frente = self.frente.siguiente
        return mensaje


#Implementacion de Red de grafo

class NodoServidor:
    def __init__(self, servidor):
        self.servidor = servidor
    def mostrar_nombre(self):
        return self.servidor.direccion
        
    def __str__(self):
        return self.servidor.direccion
class Conexion:
    def __init__(self, nodo_origen, nodo_destino):
        self.nodo_origen = nodo_origen
        self.nodo_destino = nodo_destino
        
    def mostrar_origen(self):
        return self.nodo_origen
        
    def mostrar_destino(self):
        return self.nodo_destino
class RedServidores:
    def __init__(self):
        self.grafo = {}
    def agregar_nodo(self, nodo):
        if nodo not in self.grafo:
            self.grafo[nodo] = []
    # Conexion sin direccion
    def agregar_conexione(self, conexion):
        nodo_1 = conexion.mostrar_origen()
        nodo_2 = conexion.mostrar_destino()
        if nodo_1 not in self.grafo or nodo_2 not in self.grafo:
            raise ValueError("Error: Ambos nodos deben ser agregados al grafo antes de conectarlos.")

        if nodo_2 not in self.grafo[nodo_1]:
            self.grafo[nodo_1].append(nodo_2)
            
        if nodo_1 not in self.grafo[nodo_2]:
            self.grafo[nodo_2].append(nodo_1)
    
    def mostrar_nodo(self, servidor_nombre):
        for v in self.grafo:
            if servidor_nombre == v.servidor.direccion:
                return v
        print("El nodo '{}' no existe".format(servidor_nombre))
        return None

    def __str__(self):
        """Muestra el grafo imprimiendo todas las conexiones únicas."""
        total_conexiones = "Mapa de Red de Servidores:\n"
        aristas_impresas = set()
        
        for v1 in self.grafo:
            for v2 in self.grafo[v1]:
                # Crea una tupla ordenada para identificar la arista de forma única (ej. ('A', 'B'))
                arista = tuple(sorted((v1.mostrar_nombre(), v2.mostrar_nombre())))
                
                if arista not in aristas_impresas:
                    total_conexiones += "- {} <--> {}\n".format(v1.mostrar_nombre(),v2.mostrar_nombre())
                    aristas_impresas.add(arista)
                    
        return total_conexiones
    
# Metodo de busqueda DFS 
    
    def encontrar_ruta_dfs(self, nodo_inicio, nodo_destino):
        if nodo_inicio not in self.grafo:
            print("Error: El nodo de inicio {} no existe.".format(nodo_inicio.mostrar_nombre()))
            return None

        pila = [(nodo_inicio, [nodo_inicio.mostrar_nombre()])]
        visitados = {nodo_inicio}

        while pila:
            item_actual = pila.pop() 

            nodo_actual = item_actual[0] 
            camino = item_actual[1]      

            if nodo_actual == nodo_destino:
                return camino

            for vecino in self.grafo[nodo_actual]:
                if vecino not in visitados:
                    visitados.add(vecino)
                    
                    nuevo_camino = camino + [vecino.mostrar_nombre()]
                    
                    pila.append((vecino, nuevo_camino)) 

        return None

# Metodo de busqueda BFS no implementado  

    def encontrar_ruta_bfs(self, nodo_inicio, nodo_destino):

        if nodo_inicio not in self.grafo:
            print("Error: El nodo de inicio {} no existe.".format(nodo_inicio.mostrar_nombre()))
            return None

        cola = [(nodo_inicio, [nodo_inicio.mostrar_nombre()])]
        visitados = {nodo_inicio}

        while cola:
            #  Sacamos el primer elemento (la tupla completa)
            item_actual = cola.pop(0) 

            #  Accedemos a los elementos por su índice:
            nodo_actual = item_actual[0] # El nodo Servidor es el primer elemento de la tupla
            camino = item_actual[1]      # La lista del camino es el segundo elemento de la tupla

            if nodo_actual == nodo_destino:
                return camino # (Contiene la ruta más corta)

            # Exploramos los vecinos
            for vecino in self.grafo[nodo_actual]:
                if vecino not in visitados:
                    visitados.add(vecino)
                    
                    nuevo_camino = camino + [vecino.mostrar_nombre()]
                    
                    cola.append((vecino, nuevo_camino)) 

        return None

# Metodo para enviar msj utilizando la busqueda en profundidad
    def enviar_mensaje_por_red(self, usuario_remitente, mensaje):
        receptor_correo = mensaje.receptor
        
        try:
            nombre_servidor_destino = receptor_correo.split('@')[1] 
            nombre_servidor_origen = usuario_remitente.correo.split('@')[1]
        except IndexError:
            print("Error: El correo del receptor o remitente no tiene el formato correcto (usuario@servidor).")
            return

        nodo_origen = self.mostrar_nodo(nombre_servidor_origen)
        nodo_destino = self.mostrar_nodo(nombre_servidor_destino)

        if nodo_origen is None or nodo_destino is None:
            return

        # DETERMINAR LA RUTA USANDO DFS
        if nodo_origen == nodo_destino:
            ruta = [nombre_servidor_destino]
        else:
            #ruta = self.encontrar_ruta_dfs(nodo_origen, nodo_destino) 
            ruta = self.encontrar_ruta_bfs(nodo_origen, nodo_destino) 

        servidor_destino = nodo_destino.servidor
        
        #  VERIFICAR RUTA Y ENVIAR
        if ruta is not None:
            print("\n--- Ruta Encontrada (DFS): {} ---".format(' -> '.join(ruta)))
            
            servidor_destino.enviar_msj(usuario_remitente, mensaje)
            
        else:
            print("Error: El servidor {} no es accesible desde {}.".format(nombre_servidor_destino, nombre_servidor_origen))
    
    
    # Se agrega un metodo para ingresar secion desde la red
    def iniciar_sesion(self, correo_completo, contrasenia):
        if '@' not in correo_completo:
            print("Error: El correo '{}' no tiene un formato válido.".format(correo_completo))
            return None
            
        pos_arroba = correo_completo.index('@')
        nombre_servidor = correo_completo[pos_arroba + 1:] 
            
        if not nombre_servidor:
            print("Error: El correo '{}' no especifica un servidor.".format(correo_completo))
            return None
        
        # Buscar el NodoServidor en el grafo usando la dirección del servidor
        nodo_encontrado = self.mostrar_nodo(nombre_servidor)

        if nodo_encontrado is None:
            print("Error: No se encontró el servidor '{}' en la red.".format(nombre_servidor))
            return None

        servidor_destino = nodo_encontrado.servidor 
        usuario_encontrado = servidor_destino.ingresar_usuario(correo_completo, contrasenia)
        return usuario_encontrado
    # Se agrega metodo para registrar usuarios por la red 
    def registrar_usuario(self, correo_completo, contrasenia):
        if '@' not in correo_completo:
            print("Error: El correo '{}' no tiene un formato válido.".format(correo_completo))
            return False
            
        pos_arroba = correo_completo.index('@')
        nombre_servidor = correo_completo[pos_arroba + 1:] 
            
        if not nombre_servidor:
            print("Error: El correo '{}' no especifica un servidor.".format(correo_completo))
            return False

        # Buscar el NodoServidor en el grafo 
        nodo_encontrado = self.mostrar_nodo(nombre_servidor)

        if nodo_encontrado is None:
            print("Error: No se encontró el servidor '{}' en la red.".format(nombre_servidor))
            return False
            
        # Crear el nuevo usuario
        nuevo_usuario = Usuario(correo_completo, contrasenia)
            
        # Registrar el usuario en el servidor asociado al nodo
        servidor_destino = nodo_encontrado.servidor
        servidor_destino.registrar_registrar(nuevo_usuario)             
        print("Usuario '{}' registrado con éxito en el servidor '{}'.".format(correo_completo, nombre_servidor))
        return True
    
# Registrar usuarios en cualquier servidor
    
# Iniciamos el Grafo de servidores
RED=RedServidores()
# Creamos servidores y nodos y los agragamos al grafo.
guernica = Servidor("guernica")
glew = Servidor("glew")
burzaco=Servidor("burzaco")
nodo_guernica = NodoServidor(guernica)
nodo_glew = NodoServidor(glew)
nodo_burzaco = NodoServidor(burzaco)
RED.agregar_nodo(nodo_guernica)
RED.agregar_nodo(nodo_glew)
RED.agregar_nodo(nodo_burzaco)

# CONEXIONES DEL GRAFO
# 1. Guernica <--> Glew
conexion_1 = Conexion(nodo_guernica, nodo_glew)
RED.agregar_conexione(conexion_1)

# 2. Glew <--> Burzaco
conexion_2 = Conexion(nodo_glew, nodo_burzaco)
RED.agregar_conexione(conexion_2)

# 3. Guernica <--> Burzaco
conexion_3 = Conexion(nodo_guernica, nodo_burzaco)
RED.agregar_conexione(conexion_3)

# se crean usuarios para facilitar las pruebas
usuario1 = Usuario("Julio@guernica", "123")
usuario2 = Usuario("Cristian@glew", "123")
usuario3 = Usuario("Ruben@burzaco", "123")
guernica.registrar_registrar(usuario1)
burzaco.registrar_registrar(usuario3)
glew.registrar_registrar(usuario2)
 
#se crean msj genericos
msj1 = Mensaje("Julio", "Ruben", "Urgente", "Llegaré tarde a la reunión. Empiecen sin mí.")
msj2 = Mensaje("Cristian", "Ruben", "Pendiente", "Recuerda enviar el informe de ventas hoy.")
msj3 = Mensaje("Julio", "Ruben", "Confirmar", "¿Ya tienes la clave de acceso al servidor nuevo?")
msj4 = Mensaje("Ruben", "Cristian", "Revisa", "Necesito tu opinión sobre el nuevo logo.")
msj5 = Mensaje("Ruben", "Julio", "Llamada", "Te llamo en diez minutos para coordinar el viaje.")
#se cra carpetas
borrador=Carpeta("borrador")
inp=Carpeta("inportantes")
propaganda=Carpeta("propaganda")
no_leidos=Carpeta(("no leidos"))
# se crean carpetas extras en el usuario Ruben
usuario3.carpeta_raiz.agregar_carpeta_en(borrador,"Enviados")
usuario3.carpeta_raiz.agregar_carpeta_en(inp,"Buzón de entrada")
usuario3.carpeta_raiz.agregar_carpeta_en(propaganda,"Buzón de entrada")
usuario3.carpeta_raiz.agregar_carpeta_en(no_leidos,"Buzón de entrada")
usuario3.buzon.agregar_mensaje(msj1)
usuario3.buzon.agregar_mensaje(msj2)
usuario3.buzon.agregar_mensaje(msj3)
usuario3.enviados.agregar_mensaje(msj4)
usuario3.enviados.agregar_mensaje(msj5)

usuario_logeado = None

def menu_principal():
    while True:
        print("\nBienvenido al Menú principal")
        print("\nElija una opción:\n1.Creación de un usuario\n2.Iniciar sesión\n3.Salir")
        num = input("\nIngrese la opción deseada: ")
        if num == "1":
            menu_creacion()
        elif num == "2":
            iniciar_sesion()
        elif num == "3":
            print("\nSaliendo del programa")
            break
        else:
            print("\nOpción incorrecta")
#editar para poder registrar en un servidor
def menu_creacion():
    correo = input("\nCree su correo: ")
    contrasenia = input("\nCree su contraseña: ")
    RED.registrar_usuario(correo, contrasenia)
    

def iniciar_sesion():
    correo = input("\nIngrese su correo: ")
    contrasenia = input("\nIngrese su contraseña: ")
    usuario = RED.iniciar_sesion(correo,contrasenia)
    if usuario:
        print("\nUsuario y contraseña correctos")
        usuario_logeado = usuario
        menu_usuario(usuario_logeado)
    else:
        print("\nEl usuario o la contraseña no es correcta")

def menu_usuario(usuario_logeado):
    while True:
        print("\nBienvenido al Menú del Usuario")
        print("\nElija una opción:")
        print("1. Enviar un mensaje")
        print("2. Gestionar Carpetas y Ver Mensajes")
        print("3. Marcar mensaje como urgente")
        print("4. Administrar Reglas de Filtro")
        print("5. Cerrar sesión")
        opcion = input("\nIngrese la opcion deseada: ")

        if opcion == "1":
            remitente = usuario_logeado.correo
            receptor = input("\nIngrese el correo del receptor: ")
            asunto = input("\nIngrese el asunto: ")
            cuerpo = input("\nIngrese el mensaje: ")
            mensaje = Mensaje(remitente, receptor, asunto, cuerpo)
            RED.enviar_mensaje_por_red(usuario_logeado, mensaje)

        elif opcion == "2":
            menu_carpetas(usuario_logeado)
        
        elif opcion == "3":
            print("\nBUZÓN DE ENTRADA:")
            if usuario_logeado.buzon.mensajes:
                for m in usuario_logeado.buzon.mensajes:
                    print(m)
            else:
                print("No hay mensajes.")
            asunto=input("Ingrese el asunto del mensaje a marcar como urgente: ")
            men=usuario_logeado.carpeta_raiz.buscar_y_extraer_mensaje(asunto)
            prioridad=int(input("ingrese el grado de priorida 1 = urgente, 2 = normal, 3 = baja : "))
            usuario_logeado.cola_mensajes_urgentes.encolar(men,prioridad)
            usuario_logeado.carpeta_raiz.eliminar_mensaje_por_asunto(asunto)
            print("Mensaje Marcado correctamente como urgente")
        
        elif opcion == "4":
            print(" 1. Agregar filtro o 2. Borrar filtro")
            eleccion = input(" Ingrese '1' o '2': ")
            if eleccion == "1":
                print("\nAdministrar reglas de filtrado")
                usuario_logeado.carpeta_raiz.arbol_carpetas()
                nombre_carpeta = input("Ingrese el nombre de la carpeta de destino: ")
                print("\nElija el tipo de filtro: ")
                print(" 1. Asunto o 2. Remitente")
                tipo = input("   Ingrese '1' o '2': ")
                tipo_filtro = ""
                if tipo == "1":
                    tipo_filtro = "asunto"
                    valor = input("Ingrese palabra clave en el asunto: ")
                    usuario_logeado.agregar_regla_filtro(nombre_carpeta, tipo_filtro, valor)
                elif tipo == "2" :
                    tipo_filtro = "remitente"
                    valor = input("Ingrese el remitente a filtrar: ")
                    usuario_logeado.agregar_regla_filtro(nombre_carpeta, tipo_filtro, valor)
                else:
                    print(" Tipo de filtro no válido.")
            elif eleccion == "2" :
                if not usuario_logeado.reglas_filtro:
                    print("No hay filtros")
                    
                else:
                    usuario_logeado.mostrar_filtros()
                    usuario_logeado.borrar_filtros()
        elif opcion == "5":
            print("\nSesión cerrada con éxito.")
            usuario_logeado = None
            break

        else:
            print("\nOpción incorrecta")

def menu_carpetas(usuario):
    while True:
        print("\nGESTOR DE CARPETAS")
        print("1. Ver estructura completa de carpetas y mensajes")
        print("2. Entrar a Buzón de Entrada")
        print("3. Entrar a Mensajes Enviados")
        print("4. Crear una nueva subcarpeta") 
        print("5. Mover un Mensaje a otra Carpeta")
        print("6. Ver Mensajes de una carpeta") 
        print("7. Volver al Menú Principal") 
        
        opcion = input("\nSeleccione una opción: ")
        raiz = usuario.carpeta_raiz   
        # Se agregan los mensajes al principio del Buzón de entrada 
        usuario.desencolar_mensajes_urgentes()
        usuario.aplicar_filtros_a_buzon()
        if opcion == "1":
            raiz.mostrar_carpetas_con_msj()

        elif opcion == "2":
            print("\nBUZÓN DE ENTRADA:")
            if usuario.buzon.mensajes:
                for m in usuario.buzon.mensajes:
                    print(m)
            else:
                print("No hay mensajes.")

        elif opcion == "3":
            print("\nMENSAJES ENVIADOS:")
            if usuario.enviados.mensajes:
                for m in usuario.enviados.mensajes:
                    print(m)
            else:
                print("No has enviado mensajes.")

        elif opcion == "4":
            carp = input("\nIngrese nombre de la carpeta a agregar: ")
            carpeta = Carpeta(carp)
            raiz.arbol_carpetas()
            subcarpeta = input("\nIngrese nombre de carpeta destino: ")
            if raiz.agregar_carpeta_en(carpeta, subcarpeta):
                print("\nCarpeta '{}' agregada correctamente a '{}'.".format(carp, subcarpeta))
            else:
                print("\nCarpeta destino '{}' no encontrada.".format(subcarpeta))

        elif opcion == "5":
            print("\n--- Mover Mensaje ---")
            raiz.mostrar_carpetas_con_msj()
            print("\n--- Carpetas Disponibles (por nombre) ---")
            asunto= input("\nIngrese el ASUNTO EXACTO del mensaje a mover: ")
            destino = input("\nIngrese el NOMBRE de la carpeta de DESTINO: ")
            estado=raiz.mover_mensaje(asunto,destino)   
            if estado is None:
                print("Mensaje con asunto '{}' no encontrado en ninguna carpeta." .format(asunto))  
            elif estado is False:
                print("La carpeta de destino '{}' no fue encontrada." .format(destino))
            elif estado is True:
                print("Mensaje '{}' movido con éxito a '{}'." .format(asunto,destino))
        elif opcion == "6":
            print("\n--- Ver Mensajes de Carpeta ---")
            raiz.arbol_carpetas()
            nombre_carpeta = input("\nIngrese el NOMBRE de la carpeta que desea ver: ")
            carpeta_a_ver = raiz.encontrar_carpeta(nombre_carpeta)
            if carpeta_a_ver:
                print("\nContenido de la carpeta '{}':".format(nombre_carpeta))
                if carpeta_a_ver.mensajes:
                    for m in carpeta_a_ver.mensajes:
                        print(m)
                else:
                    print("La carpeta no contiene mensajes.")
            else:
                print("ERROR: Carpeta '{}' no encontrada.".format(nombre_carpeta))        
        elif opcion == "7":
            break
        else:
            print("\nOpción incorrecta.")
            
print(RED)
menu_principal()
