class Usuario:
    def __init__(self, correo, contrasenia):
        self.correo = correo
        self.contrasenia = contrasenia
        self.carpeta_raiz = Carpeta("Raiz")
        self.buzon = Carpeta("Buzón de entrada")
        self.enviados = Carpeta("Enviados")
        self.carpeta_raiz.agregar_carpeta(self.buzon)
        self.carpeta_raiz.agregar_carpeta(self.enviados) 
        self.cola_prioridad_entrada = ColaPrioridadMensajes()
        self.reglas_filtro = {} 
    
    def procesar_mensajes_urgentes(self):
        mensajes_procesados = 0
        while not self.cola_prioridad_entrada.esta_vacia():
            mensaje = self.cola_prioridad_entrada.extraer_primero()
            self.buzon.agregar_mensaje(mensaje)
            mensajes_procesados += 1
        return mensajes_procesados
    
    def aplicar_filtros_automaticos(self, mensaje):
        regla_asunto = "asunto:{}".format(mensaje.asunto.lower())
        if regla_asunto in self.reglas_filtro:
            return self.reglas_filtro[regla_asunto]
        regla_remitente = "remitente:{}".format(mensaje.remitente.lower())
        if regla_remitente in self.reglas_filtro:
            return self.reglas_filtro[regla_remitente] 
        return None

class Mensaje:
    def __init__(self, remitente, receptor, asunto, cuerpo, es_urgente=False):
        self.remitente = remitente
        self.receptor = receptor
        self.asunto = asunto
        self.cuerpo = cuerpo
        self.es_urgente = es_urgente
    
    def __str__(self):
        urgencia = "[URGENTE] " if self.es_urgente else ""
        return "{}De: {}\nPara: {}\nAsunto: {}\nMensaje: {}\n".format(urgencia, self.remitente, self.receptor, self.asunto, self.cuerpo)

class Carpeta:
    def __init__(self, nombre):
        self.nombre = nombre
        self.mensajes = [] 
        self.lista_carpetas = [] 

    def agregar_carpeta(self, carpeta):
        self.lista_carpetas.append(carpeta)

    def agregar_mensaje(self, mensaje):
        if hasattr(mensaje, 'es_urgente') and mensaje.es_urgente:
            self.mensajes.insert(0, mensaje)
        else:
            self.mensajes.append(mensaje)
    def colectar_mensajes_recursivo(self, lista):
        for msj in self.mensajes:
            lista.append((msj, self.nombre)) 
        for carpeta in self.lista_carpetas:
            carpeta.colectar_mensajes_recursivo(lista)

    def arbol_carpetas(self, nivel=0):
        contador = "    " * nivel
        print("{}├── {}".format(contador, self.nombre))
        for carpeta in self.lista_carpetas: 
            carpeta.arbol_carpetas(nivel + 1)

    def mostrar_carpetas_con_msj(self, nivel=0):
        contador = "    " * nivel
        print("{}├── {} ({} mensajes)".format(contador, self.nombre, len(self.mensajes)))
        for msj in self.mensajes:
            urgencia = "[!]" if hasattr(msj, 'es_urgente') and msj.es_urgente else " "
            print("{}|   ├── {} {} ({})".format(contador, urgencia, msj.asunto, msj.receptor))
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

class Servidor:
    def __init__(self):
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
                usuario.enviados.agregar_mensaje(mensaje) 
                print("\nEl mensaje se envió con éxito.")
                dato.buzon.agregar_mensaje(mensaje)
                return 
        print("\nEl usuario {} no existe,".format(mensaje.receptor))

class NodoMensaje:
    def __init__(self, mensaje):
        self.mensaje = mensaje
        self.siguiente = None
        
class ColaPrioridadMensajes:
    def __init__(self):
        self.cabeza = None 
        self.ultimo = None
        
    def esta_vacia(self):
        return self.cabeza is None
        
    def insertar(self, mensaje):
        nuevo_nodo = NodoMensaje(mensaje) 
        if self.esta_vacia():
            self.cabeza = nuevo_nodo
            self.ultimo = nuevo_nodo
            return
        
        if mensaje.es_urgente:
            anterior = None
            actual = self.cabeza
            while actual is not None and actual.mensaje.es_urgente:
                anterior = actual
                actual = actual.siguiente 
            if anterior is None:
                nuevo_nodo.siguiente = self.cabeza
                self.cabeza = nuevo_nodo
            else:
                anterior.siguiente = nuevo_nodo
                nuevo_nodo.siguiente = actual
        else:
            self.ultimo.siguiente = nuevo_nodo
            self.ultimo = nuevo_nodo
            
    def extraer_primero(self):
        if self.esta_vacia():
            return None 
        mensaje_extraido = self.cabeza.mensaje
        self.cabeza = self.cabeza.siguiente 
        if self.cabeza is None:
            self.ultimo = None 
        return mensaje_extraido

servidor = Servidor()
usuario1 = Usuario("Julio", "123")
usuario2 = Usuario("Cristian", "123")
usuario3 = Usuario("Ruben", "123")
servidor.registrar_registrar(usuario1)
servidor.registrar_registrar(usuario2)
servidor.registrar_registrar(usuario3) 
msj1 = Mensaje("Julio", "Ruben", "Reunion", "Llegaré tarde a la reunión. Empiecen sin mí.")
msj2 = Mensaje("Cristian", "Ruben", "Pendiente", "Recuerda enviar el informe de ventas hoy.")
msj3 = Mensaje("Julio", "Ruben", "Confirmar", "¿Ya tienes la clave de acceso al servidor nuevo?")
msj4 = Mensaje("Ruben", "Cristian", "Revisa", "Necesito tu opinión sobre el nuevo logo.")
msj5 = Mensaje("Ruben", "Julio", "Llamada", "Te llamo en diez minutos para coordinar el viaje.")
borrador=Carpeta("borrador")
inp=Carpeta("Importantes")
propaganda=Carpeta("propaganda")
no_leidos=Carpeta("no leidos")
usuario3.carpeta_raiz.agregar_carpeta_en(borrador,"Enviados")
usuario3.carpeta_raiz.agregar_carpeta_en(inp,"Buzón de entrada")
usuario3.carpeta_raiz.agregar_carpeta_en(propaganda,"Buzón de entrada")
usuario3.carpeta_raiz.agregar_carpeta_en(no_leidos,"Buzón de entrada")
usuario3.reglas_filtro = {
    'asunto:reunion': 'Importantes',
    'remitente:julio': 'Importantes',
    'remitente:cristian': 'no leidos'}
usuario3.buzon.agregar_mensaje(msj1)
usuario3.buzon.agregar_mensaje(msj2)
usuario3.buzon.agregar_mensaje(msj3)
usuario3.enviados.agregar_mensaje(msj4)
usuario3.enviados.agregar_mensaje(msj5)

usuario_logeado = None

# --- FUNCIONES DE MENÚ ---

def menu_principal():
    while True:
        print("\nBienvenido al Menú principal")
        print("\nElija una opción:\n1.Creación de un usuario\n2.Iniciar sesión\n3.Salir")
        num = int(input("\nIngrese la opción deseada: "))
        if num == 1:
            menu_creacion()
        elif num == 2:
            iniciar_sesion()
        elif num == 3:
            print("\nSaliendo del programa")
            break
        else:
            print("\nOpción incorrecta")

def menu_creacion():
    correo = input("\nCree su correo: ")
    contrasenia = input("\nCree su contraseña: ")
    per = Usuario(correo, contrasenia)
    servidor.registrar_registrar(per)
    print("\nUsuario creado con éxito.")

def iniciar_sesion():
    global usuario_logeado
    correo = input("\nIngrese su correo: ")
    contrasenia = input("\nIngrese su contraseña: ")
    usuario = servidor.ingresar_usuario(correo, contrasenia)
    if usuario:
        print("\nUsuario y contraseña correctos")
        usuario_logeado = usuario
        disparar_procesamiento(usuario_logeado)
        menu_usuario()
    else:
        print("\nEl usuario o la contraseña no es correcta")
        
def menu_envio(usuario_logeado, servidor):
    remitente = usuario_logeado.correo
    receptor = input("\nIngrese el correo del receptor: ")
    asunto = input("\nIngrese el asunto: ")
    cuerpo = input("\nIngrese el mensaje: ")
    
    mensa = Mensaje(remitente, receptor, asunto, cuerpo, es_urgente=False)
    servidor.enviar_msj(usuario_logeado, mensa)
    disparar_procesamiento(usuario_logeado)
def marcar_urgente(usuario):
    print("\n--- MARCAR MENSAJE COMO URGENTE ---")
    
    mensajes_disponibles = []
    usuario.buzon.colectar_mensajes_recursivo(mensajes_disponibles)
    
    if not mensajes_disponibles:
        print("No hay mensajes disponibles en el Buzón de Entrada ni sus subcarpetas para marcar como urgente.")
        return

    print("\nMENSAJES DISPONIBLES EN EL BUZÓN DE ENTRADA Y SUBCARPETAS:")
    for i, (msj, carpeta) in enumerate(mensajes_disponibles):
        urgencia_tag = "[Urgente]" if msj.es_urgente else "[Normal  ]"
        print("  - {} Asunto: '{}' | De: {} | Ubicación: {}".format(urgencia_tag, msj.asunto, msj.remitente, carpeta))
        
    print("\n-----------------------------------------------------------")
    asunto_a_urgente = input("Ingrese el ASUNTO EXACTO del mensaje que desea marcar como urgente: ")
 
    mensaje_a_urgente = usuario.carpeta_raiz.buscar_y_extraer_mensaje(asunto_a_urgente)

    if mensaje_a_urgente is not None:
        
        if mensaje_a_urgente.es_urgente:
             print("\n¡ADVERTENCIA! El mensaje '{}' ya estaba marcado como urgente.".format(asunto_a_urgente))
             usuario.cola_prioridad_entrada.insertar(mensaje_a_urgente)
             
        else:
            mensaje_a_urgente.es_urgente = True
            usuario.cola_prioridad_entrada.insertar(mensaje_a_urgente)
            print("\nMensaje '{}' marcado como urgente y añadido a la Cola de Prioridad.".format(asunto_a_urgente))
            disparar_procesamiento(usuario)
    else:
        print("\nERROR: Mensaje con asunto '{}' no encontrado en ninguna carpeta.".format(asunto_a_urgente))

def menu_usuario():
    global usuario_logeado
    while True:
        print("\nBienvenido al Menú del Usuario: {}".format(usuario_logeado.correo))
        print("\nElija una opción:")
        print("1. Enviar un mensaje")
        print("2. Gestionar Carpetas y Ver Mensajes")
        print("3. Marcar Mensaje (de cualquier carpeta) como Urgente") 
        print("4. Gestionar Reglas de Filtros Automáticos")
        print("5. Cerrar sesión")
        opcion = int(input("\nIngrese la opcion deseada: "))

        if opcion == 1:
            menu_envio(usuario_logeado, servidor)

        elif opcion == 2:
            menu_carpetas(usuario_logeado)
            
        elif opcion == 3:
            marcar_urgente(usuario_logeado)

        elif opcion == 4:
            menu_filtros(usuario_logeado)

        elif opcion == 5:
            print("\nSesión cerrada con éxito.")
            usuario_logeado = None
            break

        else:
            print("\nOpción incorrecta")

def menu_carpetas(usuario):
    while True:
        print("\nGESTOR DE CARPETAS")
        print("1. Ver estructura completa de carpetas y mensajes")
        print("2. Entrar a Buzón de Entrada ") 
        print("3. Entrar a Mensajes Enviados")
        print("4. Crear una nueva subcarpeta") 
        print("5. Mover un Mensaje a otra Carpeta")
        print("6. Ver Mensajes de una carpeta ") 
        print("7. Volver al Menú Principal") 
        
        opcion = int(input("\nSeleccione una opción: "))
            
        raiz = usuario.carpeta_raiz

        if opcion == 1:
            raiz.mostrar_carpetas_con_msj()

        elif opcion == 2:
            print("\nBUZÓN DE ENTRADA (Mensajes directos):")
            if usuario.buzon.mensajes:
                for m in usuario.buzon.mensajes:
                    print(m)
            else:
                print("No hay mensajes en el buzón principal.")

        elif opcion == 3:
            print("\nMENSAJES ENVIADOS:")
            if usuario.enviados.mensajes:
                for m in usuario.enviados.mensajes:
                    print(m)
            else:
                print("No has enviado mensajes.")

        elif opcion == 4:
            carp = input("\nIngrese nombre de la carpeta a agregar: ")
            carpeta = Carpeta(carp)
            raiz.arbol_carpetas()
            subcarpeta = input("\nIngrese nombre de carpeta destino: ")
            if raiz.agregar_carpeta_en(carpeta, subcarpeta):
                print("\nCarpeta '{}' agregada correctamente a '{}'.".format(carp, subcarpeta))
            else:
                print("\nCarpeta destino '{}' no encontrada.".format(subcarpeta))

        elif opcion == 5:
            print("\n--- Mover Mensaje ---")
            print("NOTA: Se buscará el mensaje en TODAS sus carpetas.")
            raiz.mostrar_carpetas_con_msj()
            asunto= input("\nIngrese el ASUNTO EXACTO del mensaje a mover: ")
            destino = input("\nIngrese el NOMBRE de la carpeta de DESTINO: ")
            estado=raiz.mover_mensaje(asunto,destino) 
            if estado is None:
                print("Mensaje con asunto '{}' no encontrado en ninguna carpeta.".format(asunto)) 
            elif estado is False:
                print("La carpeta de destino '{}' no fue encontrada.".format(destino))
            elif estado is True:
                print("Mensaje '{}' movido con éxito a '{}'.".format(asunto,destino))
                
        elif opcion == 6:
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
        
        elif opcion == 7:
            break
        else:
            print("\nOpción incorrecta.")
            
def menu_filtros(usuario):
    while True:
        print("\n--- GESTIÓN DE REGLAS DE FILTRADO ---")
        print("Reglas actuales:")
        if not usuario.reglas_filtro:
            print("    (No hay reglas definidas)")
        for regla, destino in usuario.reglas_filtro.items():
            criterio, valor = regla.split(':')
            print("    - SI {} es '{}', mover a '{}'.".format(criterio.upper(), valor, destino)) 
            
        print("\n1. Agregar nueva regla (Asunto o Remitente)")
        print("2. Eliminar regla")
        print("3. Volver")
        opcion = int(input("\nSeleccione una opción: "))
        
        if opcion == 1:
            tipo = input("Filtrar por 'asunto' o 'remitente': ").lower()
            if tipo not in ["asunto", "remitente"]:
                print("Tipo de filtro no válido.")
                continue
                
            valor = input("Ingrese el valor exacto para el {} (se usará en minúsculas): ".format(tipo)).lower() 
            nombre_carpeta = input("Ingrese el NOMBRE EXACTO de la carpeta destino: ") 
            carpeta_destino = usuario.carpeta_raiz.encontrar_carpeta(nombre_carpeta)
            if not carpeta_destino:
                print("ERROR: La carpeta destino '{}' no existe.".format(nombre_carpeta)) 
                continue 
            llave_regla = "{}:{}".format(tipo, valor) 
            usuario.reglas_filtro[llave_regla] = nombre_carpeta
            print("Regla añadida con éxito.")
            
        elif opcion == 2:
            llave = input("Ingrese la llave de la regla a eliminar (ej: asunto:urgente): ").lower()
            if llave in usuario.reglas_filtro:
                del usuario.reglas_filtro[llave]
                print("Regla eliminada con éxito.")
            else:
                print("Regla no encontrada.")
                
        elif opcion == 3:
            break
        else:
            print("Opción incorrecta.")
            
def disparar_procesamiento(usuario):
    
    procesados_urgentes = usuario.procesar_mensajes_urgentes()
    
    mensajes_a_mover = []
    mensajes_restantes = [] 
    
    for msj in usuario.buzon.mensajes:
        destino_nombre = usuario.aplicar_filtros_automaticos(msj) 
        if destino_nombre and destino_nombre != "Buzón de entrada":
            mensajes_a_mover.append((msj, destino_nombre))
        else:
            mensajes_restantes.append(msj)
    
    if mensajes_a_mover:
        usuario.buzon.mensajes = mensajes_restantes 
        for msj, destino_nombre in mensajes_a_mover:
            carpeta_destino = usuario.carpeta_raiz.encontrar_carpeta(destino_nombre)
            if carpeta_destino:
                carpeta_destino.agregar_mensaje(msj)
            else:
                print("    - ERROR: Carpeta '{}' no encontrada para mover mensaje.".format(destino_nombre))

menu_principal()