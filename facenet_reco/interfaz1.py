from tkinter import filedialog, Tk, Frame, Label, PhotoImage, Button, Text
from tkinter import Scrollbar, INSERT, END, VERTICAL
from retrain_evaluate import evaluate_face, add_face, process_image
from PIL import Image, ImageTk
import os
import shutil
import yaml

global coordenada_x
coordenada_x = 0
global coordenada_y
coordenada_y = 40
global foto_actual
global lista_imagenes
global texto

with open("config.yaml") as f:
    conf = yaml.load(f.read())

# Se obtiene el nombre de todas las fotos de la carpeta imShow
lista_imagenes = os.listdir(
    conf["lista_imagenes"])

# se elimina el case sensitive
for i in range(len(lista_imagenes)):
    lista_imagenes[i] = lista_imagenes[
        i].lower()

# print(lista_imagenes)

# inicializacion de las caracteristicas de la ventana
raiz = Tk()
raiz.title("Sistema de detección facial")


# Funcion que es llamada por el boton "cargar" esta abre un ventana de dialogo
# para escoger la carpeta donde estaran las imagenes
def OpenFile():

    textbox.delete('1.0', END)

    # se valida si existe el directorio (no sirve si no se borran las fotos)
    validar = (
        os.path.isdir(conf['images_dir'])
    )
    if validar:
        # Se elimina el directorio
        shutil.rmtree(
            conf['images_dir']
        )
    a = os.getcwd()
    print(a)
    name = filedialog.askopenfilename(
        initialdir="../output/intermediate"
    )

    # se abre el directorio para seleccionar la foto a reconocer, la variable
    # name corresponde a todo el path con la imagen print(name)
    # se obtiene el nombre de la foto
    photo_name = name.split("/")[-1]
    if not os.path.isdir(conf['images_dir']):
        os.makedirs(conf['images_dir'])

    shutil.copy(name, conf['images_dir'])


miFrame = Frame()
miFrame.pack()


# Funcion para adquirir el texto de la informacion de la persona, esta se
# activa dentro de la funcion provFunc
def get_text():
    textbox.insert(INSERT, evaluate_face())
    texto = textbox.get("1.0", END + "-2c")  # Se obtiene el texto del textbox
    texto_espaciosV = texto.split("\n")
    # Se separa en un arreglo teniendo en cuenta los saltos de línea (la V
    # indica que es arreglo)
    texto_nombre_esp = texto_espaciosV[0]
    texto_nombre_puntosV = texto_nombre_esp.split(
        "="
    )  # se separa por igual para obtener el resto (la primera parte es un
    # numero)
    texto_nombre_puntos = texto_nombre_puntosV[
        1]  # se obtiene el nombrey el accurracy separado por puntos y espacios
    # print(texto_nombre_puntos)
    nombre_sin_puntoV = texto_nombre_puntos.split(
        ":")  # se separa por puntos para obtener el nombre y la probabilidad
    nombre_sin_guion = nombre_sin_puntoV[0]
    nombre_sin_guion_sp = nombre_sin_guion.split("_")
    print(nombre_sin_guion)
    buscar_foto_nombre = nombre_sin_guion.lower(
    )  # variable para buscar la foto por el nombre
    buscar_foto_nombre = buscar_foto_nombre + ".png"
    print(buscar_foto_nombre)
    validar_sujeto = buscar_foto_nombre in lista_imagenes
    print(validar_sujeto)
    # if validar_sujeto==True:
    img_file = 'imShow/' + buscar_foto_nombre
    img_file = img_file.replace(" ", "")
    face_delete.config(image="")
    foto_actual = PhotoImage(file=img_file)
    label = Label(miFrame, image=foto_actual)
    label.image = foto_actual
    label.place(x=100, y=200)
    nombre_sin_guion1 = nombre_sin_guion_sp[0]
    nombre_sin_guion2 = nombre_sin_guion_sp[1]
    espacio = " "
    nombreSujeto = nombre_sin_guion1 + espacio + nombre_sin_guion2
    # Aqui empieza la obtencion de la probabilidad
    probabilidad = nombre_sin_puntoV[1]

    textbox_nombre.configure(
        state='normal'
    )  # se debe settear como normal para poder borrar el contenido anterior
    textbox_probabilidad.configure(state='normal')
    textbox_nombre.delete(
        '1.0', END)  # se borra el contenido anterior en caso de haberlo
    textbox_probabilidad.delete('1.0', END)
    textbox_nombre.insert(INSERT, nombreSujeto)  # se inserta el nombre
    textbox_probabilidad.insert(INSERT, probabilidad)
    textbox_nombre.configure(
        state='disabled')  # el boton se vuelve a settear para no ser editado
    textbox_probabilidad.configure(state='disabled')
    # textbos imagen

    # print(prob_sin_puntos)


# imagen de fondo en el frame (si el frame no se pone primero lo demás no
# aparece)

fondo = PhotoImage(file="fondoF.png")
fondo = fondo.subsample(1, 1)
label = Label(miFrame, image=fondo)
label.place(x=0, y=0, relwidth=1.0, relheight=1.0)

# aquí se añadira un cuadro de texto
textbox = Text(miFrame, height=7, width=70)
# textbox.place(x=370, y=440) Es mejor pasar el parametro como una variable,
# asi se puede manipular mas facil, la variable "a" es la que debería ir por
# defecto e informacion es la que se debe recibir por parametro de docker
a = "N.A"
informacion = "N.A "
textbox.insert(INSERT, a)
# foto inicializada (estandar antes de reconocer fotos)
currentPhoto = PhotoImage(file="faceInit.png")
face_delete = Label(miFrame, image=currentPhoto)
face_delete.place(x=100, y=200)
# miFrame.config(bg="white")
miFrame.config(width="1400", heigh=("1200"))
# labels con las caracteristicas basicas de la persona en la foto
# Label nombre
Label(
    miFrame, text="Nombre:", font="30").place(
        x=370 + coordenada_x, y=150 + coordenada_y)
# Textbox nombre
textbox_nombre = Text(miFrame, height=1, width=37)
textbox_nombre.place(x=440 + coordenada_x, y=150 + coordenada_y)
# Label historia judicial
Label(
    miFrame, text=" Historial judicial: ", font="30").place(
        x=365 + coordenada_x, y=394 + coordenada_y)
# label probabilidad
Label(
    miFrame, text="Probabilidad de que sea el sujeto:", font="30").place(
        x=365 + coordenada_x, y=194 + coordenada_y)
# Textbox de la probabilidad
textbox_probabilidad = Text(miFrame, height=1, width=37)
textbox_probabilidad.place(x=640 + coordenada_x, y=194 + coordenada_y)
# label cedula
Label(
    miFrame, text="Documento de identidad:", font="30").place(
        x=370 + coordenada_x, y=234 + coordenada_y)
Label(
    miFrame, text="Dirección: ", font="30").place(
        x=370 + coordenada_x, y=274 + coordenada_y)
Label(
    miFrame, text="Estado: ", font="30").place(
        x=370 + coordenada_x, y=314 + coordenada_y)
Label(
    miFrame, text="Estatura: ", font="30").place(
        x=370 + coordenada_x, y=354 + coordenada_y)


# boton cargar
btn = Button(raiz, text="Cargar")
btn.place(x=100, y=454)
btn.config(command=OpenFile)


# call the preproccessing script on the pictures in the main folder.
def preprocess():
    textbox.delete('1,0', END)
    textbox.insert(INSERT, process_image(filedialog.askdirectory()))


# call the retraining script with the pictures on the main folder as
# the source for the new person.
def retrain():
    textbox.delete('1.0', END)
    textbox.insert(INSERT, add_face(filedialog.askdirectory()))


# boton reconocer
btn2 = Button(raiz, text="Reconocer")
btn2.place(x=262, y=454)
btn2.config(command=get_text)

# boton pre procesar
btn3 = Button(raiz, text="Pre procesar")
btn3.place(x=262, y=494)
btn3.config(command=preprocess)

# botón reentrenar
btn4 = Button(raiz, text="Añadir persona")
btn4.place(x=100, y=494)
btn4.config(command=retrain)

raiz.mainloop()
