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

class Mensaje:
    def __init__(self, remitente, receptor, asunto, cuerpo):
        self.remitente = remitente
        self.receptor = receptor
        self.asunto = asunto
        self.cuerpo = cuerpo
    
    def __str__(self):
        return "De: {}\nPara: {}\nAsunto: {}\nMensaje: {}\n".format(self.remitente, self.receptor, self.asunto, self.cuerpo)

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
        print("{} {}".format(contador, self.nombre))
        for carpeta in self.lista_carpetas: 
            carpeta.arbol_carpetas(nivel + 1)

    def mostrar_carpetas_con_msj(self, nivel=0):
        contador = "  " * nivel
        print("{} {} ({} mensajes)".format(contador, self.nombre, len(self.mensajes)))
        for msj in self.mensajes:
            print("{} {}".format(contador, msj.asunto))
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
    def encontrar_carpeta(self, nombre_carpeta):
        if self.nombre == nombre_carpeta:
            return self
        
        for carpeta in self.lista_carpetas:
            encontrada = carpeta.encontrar_carpeta(nombre_carpeta)
            if encontrada:
                return encontrada        
        return None    

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

servidor = Servidor()
# se crean usuarios para facilitar las pruebas
usuario1 = Usuario("Julio", "123")
usuario2 = Usuario("Cristian", "123")
usuario3 = Usuario("Ruben", "123")
servidor.registrar_registrar(usuario1)
servidor.registrar_registrar(usuario2)
servidor.registrar_registrar(usuario3) 

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
        menu_usuario()
    else:
        print("\nEl usuario o la contraseña no es correcta")

def menu_usuario():
    global usuario_logeado
    while True:
        print("\nBienvenido al Menú del Usuario")
        print("\nElija una opción:")
        print("1. Enviar un mensaje")
        print("2. Gestionar Carpetas y Ver Mensajes")
        print("3. Cerrar sesión")
        opcion = input("\nIngrese la opcion deseada: ")

        if opcion == "1":
            remitente = usuario_logeado.correo
            receptor = input("\nIngrese el correo del receptor: ")
            asunto = input("\nIngrese el asunto: ")
            cuerpo = input("\nIngrese el mensaje: ")
            mensa = Mensaje(remitente, receptor, asunto, cuerpo)
            servidor.enviar_msj(usuario_logeado, mensa)

        elif opcion == "2":
            menu_carpetas(usuario_logeado)

        elif opcion == "3":
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
        print("6. Volver al Menú Principal") 
        
        opcion = int(input("\nSeleccione una opción: "))
        raiz = usuario.carpeta_raiz

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
            raiz.arbol_carpetas()
            origen_nombre = input("\nIngrese el NOMBRE de la carpeta de ORIGEN: ")
            asunto_msj = input("\nIngrese el ASUNTO EXACTO del mensaje a mover: ")
            destino_nombre = input("\nIngrese el NOMBRE de la carpeta de DESTINO: ")
            carpeta_origen = raiz.encontrar_carpeta(origen_nombre)
            carpeta_destino = raiz.encontrar_carpeta(destino_nombre)
            if carpeta_origen:
                if carpeta_destino:
                    mensaje_a_mover = carpeta_origen.eliminar_mensaje_por_asunto(asunto_msj)
                    if mensaje_a_mover:
                        carpeta_destino.agregar_mensaje(mensaje_a_mover)
                        print("\nMensaje '{}' movido de '{}' a '{}'.".format(asunto_msj, origen_nombre, destino_nombre))
                    else:
                        print("\nMensaje con asunto '{}' no encontrado en '{}'.".format(asunto_msj, origen_nombre))
                else:
                    print("\nLa carpeta de destino '{}' no existe.".format(destino_nombre))
            else:
                print("\nLa carpeta de origen '{}' no existe.".format(origen_nombre))

        elif opcion == 6:
            break

        else:
            print("\nOpción incorrecta.")
menu_principal()