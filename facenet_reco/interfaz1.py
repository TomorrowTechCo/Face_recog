from tkinter import filedialog, Tk, Frame, Label, PhotoImage, Button, Text
from tkinter import INSERT, END
from retrain_evaluate import evaluate_face, add_face, process_image
import os
import shutil
import yaml
import cv2

global coordenada_x
coordenada_x = 0
global coordenada_y
coordenada_y = 40
global foto_actual
global lista_imagenes
global texto

ROOT_DIR = os.getcwd().split("facial_recog")[0]

with open("config.yaml") as f:
    conf = yaml.load(f.read())

# Se obtiene el nombre de todas las fotos de la carpeta imShow
lista_imagenes = os.listdir(conf["lista_imagenes"])

# se elimina el case sensitive
for i in range(len(lista_imagenes)):
    lista_imagenes[i] = lista_imagenes[i].lower()

# print(lista_imagenes)

# inicializacion de las caracteristicas de la ventana
raiz = Tk()
raiz.title("Sistema de detección facial")


# Funcion que es llamada por el boton "cargar" esta abre un ventana de dialogo
# para escoger la carpeta donde estaran las imagenes
def OpenFile():

    textbox.delete('1.0', END)

    # se valida si existe el directorio (no sirve si no se borran las fotos)
    if os.path.isdir(conf['images_dir']):
        # Se elimina el directorio
        shutil.rmtree(conf['images_dir'])
    name = filedialog.askopenfilename(initialdir="../output/intermediate")

    # se abre el directorio para seleccionar la foto a reconocer, la variable
    # name corresponde a todo el path con la imagen print(name)
    # se obtiene el nombre de la foto
    photo_name = name.split("/")[-1]
    os.makedirs(conf['images_dir'])

    # guardar la foto en una carpeta provisionalmente
    shutil.copy(name, ROOT_DIR + conf['prov_img'])

    # mientras se preprocesa
    process_image(conf['prov_folder'])

    # y ahora sí se guarda en la carpeta definitiva
    shutil.copy(ROOT_DIR + conf['prov_img'] + photo_name,
                ROOT_DIR + conf['images_dir_prov'])


miFrame = Frame()
miFrame.pack()

# simple window to add number of existing classes
existing_classes = Text(raiz, height=1, width=20)
existing_classes.place(x=450 + coordenada_x, y=150)
Label(
    raiz, text=" num sujetos: ", font="30").place(
        x=300 + coordenada_x, y=110 + coordenada_y)

# Funcion para adquirir el texto de la informacion de la persona, esta se
# activa dentro de la funcion provFunc
def get_text():
    textbox.insert(INSERT, evaluate_face())
    texto = textbox.get("1.0", END + "-2c")  # Se obtiene el texto del textbox
    texto_espaciosV = texto.split("\n")
    print(texto_espaciosV)
    # Se separa en un arreglo teniendo en cuenta los saltos de línea (la V
    # indica que es arreglo)
    texto_nombre_esp = texto_espaciosV[2]
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
    buscar_foto_nombre = nombre_sin_guion.lower(
    )  # variable para buscar la foto por el nombre
    buscar_foto_nombre = buscar_foto_nombre + ".png"
    img_file = 'imShow/' + buscar_foto_nombre
    img_file = img_file.replace(" ", "")
    face_delete.config(image="")
    foto_actual = PhotoImage(file=img_file)
    label = Label(miFrame, image=foto_actual)
    label.image = foto_actual
    label.place(x=100, y=200)
    nombreSujeto = nombre_sin_guion_sp[0] + " " + nombre_sin_guion_sp[1]
    # Aqui empieza la obtencion de la probabilidad
    probabilidad = nombre_sin_puntoV[1]

    textbox_nombre.configure(state='normal')
    # se debe settear como normal para poder borrar el contenido anterior
    textbox_probabilidad.configure(state='normal')
    textbox_nombre.delete('1.0', END)
    # se borra el contenido anterior en caso de haberlo
    textbox_probabilidad.delete('1.0', END)
    textbox_nombre.insert(INSERT, nombreSujeto)  # se inserta el nombre
    textbox_probabilidad.insert(INSERT, probabilidad)
    textbox_nombre.configure(
        state='disabled')  # el boton se vuelve a settear para no ser editado
    textbox_probabilidad.configure(state='disabled')


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


# call the retraining script with the pictures on the main folder as
# the source for the new person.
def retrain_new():
    textbox.delete('1.0', END)
    webcam = cv2.VideoCapture(-1)
    classifier = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    while True:
        (rval, im) = webcam.read()
        im = cv2.flip(im, 1, 0)  # Flip to act as a mirror
        gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        faces = classifier.detectMultiScale(gray, 1.3, 5)
        for (x, y, w, h) in faces:
            cv2.rectangle(im, (x, y), (x + w, y + h), (255, 0, 0),
                          2)  # x+w y y+h
            roi_gray = gray[y:y + h, x:x + w]
            roi_color = im[y:y + h, x:x + w]
            sub_face = im[y:y + h, x:x + w]
            FaceFileName = "nuevacara/face_" + str(y) + ".jpg"
            res = cv2.resize(
                sub_face, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
            cv2.imwrite(FaceFileName, res)
        cv2.imshow('Capturar', im)
        key = cv2.waitKey(10)
        # if Esc key is press then break out of the loop
        if key == 27:  # The Esc key
            break
    webcam.release()
    cv2.destroyAllWindows()
    textbox.insert(INSERT, add_face(filedialog.askdirectory(),
                                    existing_classes.get("1.0", END))


# add a person from existing images to the model.
def retrain_old():
    add_face(filedialog.askdirectory())


# boton cargar
btn = Button(raiz, text="Cargar")
btn.place(x=100, y=454)
btn.config(command=OpenFile)

# boton reconocer
btn2 = Button(raiz, text="Reconocer")
btn2.place(x=262, y=454)
btn2.config(command=get_text)

# boton pre procesar
btn3 = Button(raiz, text="Añadir persona")
btn3.place(x=262, y=494)
btn3.config(command=retrain_old)

# botón reentrenar
btn4 = Button(raiz, text="Añadir fotos de sujeto")
btn4.place(x=100, y=494)
btn4.config(command=retrain_new)

raiz.mainloop()
