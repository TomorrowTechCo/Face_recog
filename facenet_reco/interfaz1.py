from tkinter import filedialog, Tk, Frame, Label, PhotoImage, Button, Text
from tkinter import Scrollbar, INSERT, END, VERTICAL
from retrain_evaluate import evaluate_face, add_face
from PIL import Image
import os
global name
global entrada
# inicializacion de las caracteristicas de la ventana
raiz = Tk()
raiz.title("Sistema de detección facial")

#GvR, forgive me for doing this
faces = [
    "Alvaro_Uribe:",
    "Arnold_Schwarzenegger",
    "David_Beckham",
    "Jennifer_Lopez",
    "Luiz_Inacio_Lula_da_Silva",
    "Meryl_Streep",
    "Recep_Tayyip_Erdogan",
    "Serena_Williams",
    "Silvio_Berlusconi",
    "Vicente_Fox"
]


# Funcion que es llamada por el boton "cargar" esta abre un ventana de dialogo
# para escoger la carpeta donde estaran las imagenes
def OpenFile():
    name = filedialog.askdirectory()
    get_text()


miFrame = Frame()
miFrame.pack()
# []
global texto


# Funcion para adquirir el texto de la informacion de la persona, esta se
# activa dentro de la funcion provFunc
def get_text():
    texto = textbox.get("1.0", END + "-2c")  # Se obtiene el texto del textbox
    texto_espacios = texto.split("\n")
    # Se separa en un arreglo teniendo en cuenta los saltos de línea
    texto_nombre_esp = texto_espacios[4]
    # El cuarto elemento debería corresponder a el nombre y la
    # probabilidad se parado por ":" y espacios
    # print(texto_nombre_esp)
    texto_nombre_esp = texto_nombre_esp.split(" ")
    # Se separa por espacios y solo queda el nombre (esto es un arreglo)
    # print(texto_nombre_esp)
    nombre = texto_nombre_esp[2]  # Se obtiene el nombre con dos puntos
    # print(nombre)
    nombre_sin_puntoV = nombre.split(":")
    # Se obtiene solo el nombre sin el punto (la V indica que es un arreglo)
    # print(nombre_sin_puntoV) Para ver lo que se tenia
    nombreFinal = nombre_sin_puntoV[0]
    nombre_sin_guion = nombreFinal.split("_")
    # print(nombre_sin_guion)
    nombre_sin_guion1 = nombre_sin_guion[0]
    nombre_sin_guion2 = nombre_sin_guion[1]
    Label(miFrame, text=nombre_sin_guion1, font="30").place(x=170, y=170)
    Label(miFrame, text=nombre_sin_guion2, font="30").place(x=230, y=170)
    # Aqui empieza la obtencion de la probabilidad
    prob = texto_espacios[len(texto_espacios) - 2]
    prob_sin_puntosV = prob.split(":")
    prob_sin_puntos = prob_sin_puntosV[1]
    Label(miFrame, text=prob_sin_puntos, font="30").place(x=680, y=194)
    print(prob_sin_puntos)


# imagen de fondo en el frame (si el frame no se pone primero lo demás no aparece)

fondo = PhotoImage(file="fondoF.png")
fondo = fondo.subsample(1, 1)
label = Label(miFrame, image=fondo)
label.place(x=0, y=0, relwidth=1.0, relheight=1.0)

# aquí se añadira un cuadro de texto
textbox = Text(miFrame, height=7, width=70)
textbox.place(x=370, y=440)
# Es mejor  pasar el parametro como una variable, asi se puede manipular mas facil, la variable "a" es la que debería ir por defecto e informacion es la que se debe recibir por parametro de docker
a = "N.A"
informacion = "INFO:root:Model filename: /facial_recog/etc/20170511-185253/20170511-185253.pb\nINFO:_main_:Processing iteration 0 batch of size: 93 \nINFO:_main_:Created 93 embeddings\nINFO:_main_:Evaluating classifier on 93 images\n0  Alvaro_Uribe: 0.883\n1  Alvaro_Uribe: 0.999\n2  Alvaro_Uribe: 1.000\n3  Alvaro_Uribe: 0.999\n4  Alvaro_Uribe: 1.000\n5  Alvaro_Uribe: 0.999\n6  Alvaro_Uribe: 1.000\n7  Alvaro_Uribe: 0.990  \n8  Alvaro_Uribe: 1.000\nAccuracy: 0.968\nINFO:_main_:Completed in 19.643153190612793 seconds "
textbox.insert(INSERT, informacion)
scroll = Scrollbar(raiz, command=textbox.yview, orient=VERTICAL)
scroll.config(command=textbox.yview)
textbox.configure(yscrollcommand=scroll.set)

# logo de la fiscalia
fiscalia = PhotoImage(file="fiscalia.png")
Label(miFrame, image=fiscalia).place(x=1100, y=0)
# foto inicializada (estandar antes de reconocer fotos)
currentPhoto = PhotoImage(file="faceInit.png")
Label(miFrame, image=currentPhoto).place(x=100, y=200)

# miFrame.config(bg="white")
miFrame.config(width="1400", heigh=("1200"))
# labels con las caracteristicas basicas de la persona en la foto
Label(miFrame, text="Nombre:", font="30").place(x=100, y=170)
# Label(miFrame, text=" Historial judicial: ",fg="red", font="30").place(x=360, y=394)
Label(miFrame, text=" Historial judicial: ", font="30").place(x=365, y=394)
Label(
    miFrame, text="Probabilidad de que sea el sujeto:", font="30").place(
        x=370, y=194)
Label(miFrame, text="Documento de identidad:", font="30").place(x=370, y=234)
Label(miFrame, text="Dirección: ", font="30").place(x=370, y=274)
Label(miFrame, text="Estado: ", font="30").place(x=370, y=314)
Label(miFrame, text="Estatura: ", font="30").place(x=370, y=354)
# Label(miFrame, text="recomendaciones basadas en sus antecedentes:",font="30").place(x=370, y=394)

btn = Button(raiz, text="Cargar")
btn.place(x=100, y=454)
btn.config(command=OpenFile)

# 65


# provisional function to test button
def provFunc():
    textbox.insert(INSERT, evaluate_face())
    name = textbox.get(1.0, END).split('\n')[0].split(' ')[5]
    if name[:len(name)-1] in faces:
        new_photo = PhotoImage(''.join(["show/", name]))
        Label(miFrame, image=new_photo).place(x=100, y=200)


btn2 = Button(raiz, text="Reconocer")
btn2.place(x=262, y=454)
btn2.config(command=provFunc)
# prueba Variables En funciones

# termina la prueba
raiz.mainloop()
