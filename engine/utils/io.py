import json, os
from engine.utils.assets import load_img

def load_dirs(path):
    dirs = {}
    for folder in os.listdir(path):
        dirs[folder] = load_dir(f'{path}/{folder}')
    return dirs

def load_dir(path):
    image_dir = {}
    for f in os.listdir(path):
        image_dir[f.split('.')[0]] = f'{path}/{f}'
    return image_dir

def write_f(path, data):
    f = open(path, 'w')
    f.write(data)
    f.close()

def read_f(path):
    f = open(path, 'r')
    data = f.read()
    f.close()
    return data

def read_json(path):
    f = open(path, 'r')
    data = json.load(f)
    f.close()
    return data

def write_json(path, data):
    f = open(path, 'w')
    json.dump(data, f)
    f.close()

def set_working_dir(path):
    os.chdir(path)