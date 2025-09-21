class Usuario:
    def __init__(self, correo, contraseña):
        self.correo = correo
        self.contraseña = contraseña
        self.buzon = []       
        self.enviados = []    

class Mensaje:
    def __init__(self, remitente, receptor, asunto, cuerpo):
        self.remitente = remitente
        self.receptor = receptor
        self.asunto = asunto
        self.cuerpo = cuerpo

    def __str__(self):
        return f"De: {self.remitente}\nPara: {self.receptor}\nAsunto: {self.asunto}\nMensaje: {self.cuerpo}\n"

personas = []
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
    contraseña = input("\nCree su contraseña: ")
    per = Usuario(correo, contraseña)
    personas.append(per)
    print("\nUsuario creado con éxito.")

def iniciar_sesion():
    global usuario_logeado
    correo = input("\nIngrese su correo: ")
    usuario = None
    for u in personas:
        if correo == u.correo:
            usuario = u
            break
    if usuario is None:
        print("\nEl usuario no existe")
        return
    print("\nEl usuario es correcto")
    contraseña = input("\nIngrese su contraseña: ")
    if contraseña == usuario.contraseña:
        print("\nContraseña correcta")
        usuario_logeado = usuario
        menu_usuario()
    else:
        print("\nLa contraseña no es correcta")

def menu_usuario():
    global usuario_logeado
    while True:
        print("\nBienvenido al Menú del Usuario")
        print("\nElija una opción:")
        print("1. Enviar un mensaje")
        print("2. Buzón de entrada")
        print("3. Mensajes enviados")
        print("4. Cerrar sesión")
        opcion = input("\nIngrese la opcion deseada: ")

        if opcion == "1":
            remitente = usuario_logeado.correo
            receptor = input("\nIngrese el correo del receptor: ")
            asunto = input("\nIngrese el asunto: ")
            cuerpo = input("\nIngrese el mensaje: ")
            mensa = Mensaje(remitente, receptor, asunto, cuerpo)

            receptor_encontrado = False
            for u in personas:
                if u.correo == receptor:
                    u.buzon.append(mensa)
                    receptor_encontrado = True
                    break
            if receptor_encontrado:
                print("\nMensaje enviado.")
            else:
                print("\nEl receptor no existe. Mensaje no enviado.")
            usuario_logeado.enviados.append(mensa)

        elif opcion == "2":
            print("\nBUZÓN DE ENTRADA:")
            if usuario_logeado.buzon:
                for m in usuario_logeado.buzon:
                    print(m)
            else:
                print("\nNo tienes mensajes.")

        elif opcion == "3":
            print("\nMENSAJES ENVIADOS:")
            if usuario_logeado.enviados:
                for m in usuario_logeado.enviados:
                    print(m)
            else:
                print("\nNo has enviado mensajes.")
            input("\nPresiona Enter para continuar...")

        elif opcion == "4":
            print("\nSesión cerrada con éxito.")
            usuario_logeado = None
            break
        else:
            print("\nOpción incorrecta")

menu_principal()