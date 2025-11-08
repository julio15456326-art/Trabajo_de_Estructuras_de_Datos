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
    # Metodos par agregar reglas
    def agregar_regla_filtro(self, nombre_carpeta, tipo_filtro, valor_a_buscar):
        tipo_filtro = tipo_filtro.lower()
        if tipo_filtro not in ["asunto", "remitente"]:
            print(" ERROR: El tipo de filtro debe ser 'asunto' o 'remitente'.")
            return
        self.reglas_filtro[nombre_carpeta] = [tipo_filtro, valor_a_buscar.lower()]
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
                tipo_filtro = regla[0]
                valor_esperado = regla[1]
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
        
            
    
class Mensaje:
    def __init__(self, remitente, receptor, asunto, cuerpo,urgencia=""):
        self.remitente = remitente
        self.receptor = receptor
        self.asunto = asunto
        self.cuerpo = cuerpo
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

servidor = Servidor()
# se crean usuarios para facilitar las pruebas
usuario1 = Usuario("Julio", "123")
usuario2 = Usuario("Cristian", "123")
usuario3 = Usuario("Ruben", "123")
servidor.registrar_registrar(usuario1)
servidor.registrar_registrar(usuario2)
servidor.registrar_registrar(usuario3) 
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
    correo = input("\nIngrese su correo: ")
    contrasenia = input("\nIngrese su contraseña: ")
    usuario = servidor.ingresar_usuario(correo, contrasenia)
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
        opcion = int(input("\nIngrese la opcion deseada: "))

        if opcion == 1:
            remitente = usuario_logeado.correo
            receptor = input("\nIngrese el correo del receptor: ")
            asunto = input("\nIngrese el asunto: ")
            cuerpo = input("\nIngrese el mensaje: ")
            mensaje = Mensaje(remitente, receptor, asunto, cuerpo)
            servidor.enviar_msj(usuario_logeado, mensaje)

        elif opcion == 2:
            menu_carpetas(usuario_logeado)
        
        elif opcion == 3:
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
        
        elif opcion == 4:
            print("\nAdministrar reglas de filtrado")
            usuario_logeado.carpeta_raiz.arbol_carpetas()
            nombre_carpeta = input("Ingrese el nombre de la carpeta de destino")
            print("\nElija el tipo de filtro:")
            print(" 1. Asunto o 2. Remitente")
            tipo = int(input("   Ingrese '1' o '2': "))
            tipo_filtro = ""
            if tipo == 1:
                tipo_filtro = "asunto"
                valor = input("Ingrese palabra clave en el asunto ")
            elif tipo == 2 :
                tipo_filtro = "remitente"
                valor = input("Ingrese el remitente a filtrar")
            else:
                print(" Tipo de filtro no válido.")
                continue

            usuario_logeado.agregar_regla_filtro(nombre_carpeta, tipo_filtro, valor)
        
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
        print("2. Entrar a Buzón de Entrada")
        print("3. Entrar a Mensajes Enviados")
        print("4. Crear una nueva subcarpeta") 
        print("5. Mover un Mensaje a otra Carpeta")
        print("6. Ver Mensajes de una carpeta") 
        print("7. Volver al Menú Principal") 
        
        opcion = int(input("\nSeleccione una opción: "))
        raiz = usuario.carpeta_raiz   
        # Se agregan los mensajes al principio del Buzón de entrada 
        usuario.desencolar_mensajes_urgentes()
        usuario.aplicar_filtros_a_buzon()
        if opcion == 1:
            raiz.mostrar_carpetas_con_msj()

        elif opcion == 2:
            print("\nBUZÓN DE ENTRADA:")
            if usuario.buzon.mensajes:
                for m in usuario.buzon.mensajes:
                    print(m)
            else:
                print("No hay mensajes.")

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
        elif opcion == 6:
            print("\n--- Ver Mensajes de Carpeta ---")
            raiz.arbol_carpetas()
            nombre_carpeta = input("\nIngrese el NOMBRE de la carpeta que desea ver: ")
            carpeta_a_ver = raiz.encontrar_carpeta(nombre_carpeta)
            if carpeta_a_ver:
                print(f"\nContenido de la carpeta '{nombre_carpeta}':")
                if carpeta_a_ver.mensajes:
                    for m in carpeta_a_ver.mensajes:
                        print(m)
                else:
                    print("La carpeta no contiene mensajes.")
            else:
                print(f"ERROR: Carpeta '{nombre_carpeta}' no encontrada.")        
        elif opcion == 7:
            break
        else:
            print("\nOpción incorrecta.")
menu_principal()