# this is the program API, designed with the following capabilities in mind:
# + evaluate a single face against the model (easy),
# + add a new face to the model (intermediate),
# + render the facial landmark and HOG results to the GUI for extra points
#   (hard).
# thus it will host three main function calls.
import logging
import docker
import re
import os
import yaml
with open("config.yaml") as f:
    conf = yaml.load(f.read())


client = docker.from_env()
logger = logging.getLogger(__name__)

# absolute path of program in host os
dir_ls = os.getcwd().split('facial_recog')[0] + 'facial_recog/'


def save_config(directory):
    """
    saves the config when it is changed during the program.
    """

    with open("config.yaml", 'r+') as f:
        conf = yaml.load(f.read())
        conf["classifier_path"] = ''.join([directory, "classifier.pkl"])
        conf["embeddings_path"] = ''.join([directory, "embeddings.pkl"])
        f.write(yaml.dump(conf, default_flow_style=False))


# formats the directory nicely for Docker
def docker_dir(abspath):
    dir_list = abspath.split('facial_recog')[1].split('/')[1:]
    return '/'.join(['', 'facial_recog'] + [x for x in dir_list] + [''])


def evaluate_face(input_dir="/home/chava/Documents/PythonProjects/facialReco"
                  "/facial_recog/temp/"):
    """
    function that recognizes the face on a picture.
    input: location of the picture. (str)
    output: predicted label of the picture. (str)
    errors:
    + picture_name does not exist/is not and image - throw type error
    + no positive match to any of the labels - throw nonexistent error
    """
    # print(input_dir)

    # directory = re.split("facialReco", input_dir)[1]

    command_string = ' '.join([
        "python3 /facial_recog/facenet_reco"
        "/train_classifier.py --input-dir", docker_dir(input_dir),
        "--model-path /facial_recog/etc/20170511-185253/"
        "20170511-185253.pb --classifier-path "
        "/facial_recog/output/classifier2.pkl "
        "--num-threads 16 --num-epochs 5 "
        "--min-num-images-per-class 1"
    ])

    return (client.containers.run(
        "colemurray/medium-facenet-tutorial",
        command_string,
        environment=["PYTHONPATH=$PYTHONPATH:/facial_recog"],
        volumes={
            '/home/chava/Documents/PythonProjects/'
            'facialReco/facial_recog/': {
                'bind': '/facial_recog',
                'mode': 'rw'
            }
        }))


def add_face(input_dir):
    """
    function that retrains the model to add a new face.
    input: location of the images. (str)
    output: error code, 0 otherwise. (exception, none)
    errors:
    + pictures_folder is not a folder - throw type error
    + pictures_folder contains a non-image - fail silently and continue
      for the rest
    + pictures_folder does not have [enough] pictures - throw exception and
      exit
    + pictures_folder contains pictures that are not from the same people -
      this kills the model.
    """

    # dir_list = input_dir.split('facial_recog')[1].split('/')
    # directory = '/'.join(['', 'facial_recog]'] + [x for x in dir_list])

    command_string = ' '.join([
        "python3 /facial_recog/facenet_reco"
        "/train_classifier.py --input-dir", docker_dir(input_dir),
        "--model-path /facial_recog/etc/20170511-185253/"
        "20170511-185253.pb --classifier-path", conf["classifier_path"],
        "--num-threads 16 --num-epochs 5 "
        "--min-num-images-per-class 10 --is-train --is-retrain"
    ])
    save_config(docker_dir(input_dir))

    return(client.containers.run(
        "colemurray/medium-facenet-tutorial",
        command_string,
        environment=["PYTHONPATH=$PYTHONPATH:/facial_recog"],
        volumes={
            dir_ls: {
                'bind': '/facial_recog',
                'mode': 'rw'
            }
        }))


def process_image(picture):
    """function that takes the pictures from the main folder and preprocesses
    them.
    """

    print(docker_dir(picture))

    command_string = ' '.join([
        "python3 /facial_recog/facenet_reco/preprocess.py "
        "--input-dir", docker_dir(picture),
        "--output-dir", conf["preprocessing_path"],
        "--crop-dim 180"
    ])

    return (client.containers.run(
        "colemurray/medium-facenet-tutorial",
        command_string,
        environment=["PYTHONPATH=$PYTHONPATH:/facial_recog"],
        volumes={
            dir_ls: {
                'bind': '/facial_recog',
                'mode': 'rw'
            }
        }))


def adjust_algo(direc):
    """
    function that trains a new model from the pictures in the selected folder.
    """

    command_string = ' '.join([
        "python3 /facial_recog/facenet_reco"
        "/train_classifier.py --input-dir", docker_dir(direc),
        "--model-path /facial_recog/etc/20170511-185253/"
        "20170511-185253.pb --classifier-path", conf["classifier_path"],
        "--num-threads 16 --num-epochs 5 "
        "--min-num-images-per-class 10 --is-train"
    ])
    save_config(docker_dir(direc))

    return(client.containers.run(
        "colemurray/medium-facenet-tutorial",
        command_string,
        environment=["PYTHONPATH=$PYTHONPATH:/facial_recog"],
        volumes={
            dir_ls: {
                'bind': '/facial_recog',
                'mode': 'rw'
            }
        }))
