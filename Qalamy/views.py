from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.http import HttpResponseBadRequest
from PIL import Image
from io import BytesIO
from base64 import b64decode
import cv2
import numpy as np
import os
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.lite.python.interpreter import Interpreter
from .models import MyImage
from .api.serializers import MyImageModelSerializer
from rest_framework.response  import Response


# Create your views here.
arabic_letters = {
    'ء': {46: '\u0621'},
    'أ': {91: '\u0623',40: '\uFE84'},
    'ؤ': {41: '\u0624'},
    'إ': {19: '\u0625',90: '\uFE88'},
    'ا': {105: '\u0627',39: '\uFE8F'},
    'ئ': {37: '\u0626',  74: '\uFE8C'},
    'ب': {16: '\u0628', 31: '\uFE91', 100: '\uFE92', 4: '\uFE93'},
    'ت': {1: '\u062A', 77: '\uFE97', 61: '\uFE98', 102: '\uFE99'},
    'ث': {82: '\u062B', 23: '\uFE9B', 2: '\uFE9C', 58: '\uFE9D'},
    'ج': {99: '\u062C', 27: '\uFE9F', 48: '\uFEA0', 89: '\uFEA1'},
    'ح': {9: '\u062D', 54: '\uFEA3', 81: '\uFEA4', 17: '\uFEA5'},
    'خ': {12: '\u062E', 73: '\uFEA7', 76: '\uFEA8',79: '\uFEA9'},
    'د': {93: '\u062F', 84: '\uFEAA'},
    'ذ': {65: '\u0630', 94: '\uFEAB'},
    'ر': {34: '\u0631', 71: '\uFEAD'},
    'ز': {88: '\u0632', 8: '\uFEAF'},
    'س': {63: '\u0633', 0: '\uFEB3', 49: '\uFEB4', 43: '\uFEB5'},
    'ش': {22: '\u0634', 38: '\uFEB7', 62: '\uFEB8', 20: '\uFEB9'},
    'ص': {52: '\u0635', 5: '\uFEBB', 80: '\uFEBC', 104: '\uFEBD'},
    'ض': {68: '\u0636', 75: '\uFEBF', 29: '\uFEC0', 69: '\uFEC1'},
    'ط': {28: '\u0637', 87: '\uFEC3', 50: '\uFEC4', 98: '\uFEC5'}, #i am not sure
    'ظ': {45: '\u0638',26: '\uFEC7', 70: '\uFEC8', 15: '\uFEC9', 'medial2': '\uFECA'},#i am not sure
    'ع': {13: '\u0639', 3: '\uFECB', 32: '\uFECC', 14: '\uFECD'},
    'غ': {57: '\u063A', 96: '\uFECF', 85: '\uFED0', 21: '\uFED1'},# iam not sure
    'ف': {107: '\u0641', 25: '\uFED7', 55: '\uFED8', 51: '\uFED9'},
    'ق': {47: '\u0642', 101: '\uFEDB', 18: '\uFEDC', 97: '\uFEDD', 'medial2': '\uFEDE'},
    'ك': {44: '\u0643', 103: '\uFEF3', 78: '\uFEF4', 66: '\uFEF5'},
    'ل': {106: '\u0644', 7: '\uFEFB', 30: '\uFEFC', 56: '\uFEFD'},
    'م': {35: '\u0645', 11: '\uFEE3', 64: '\uFEE4', 95: '\uFEE5'},
    'ن': {72: '\u0646', 86: '\uFEEB',24: '\uFEEC', 92: '\uFEED'},
    'ه': {67: '\u0647', 60: '\uFEEF', 6: '\uFEF0', 42: '\uFEF1'},
    'و': {33: '\u0648',36: '\uFEE5'},
    'ي': {59: '\u064A', 10: '\uFEF3', 83: '\uFEF4', 35: '\uFEF5', 'medial2': '\uFEF6'},
 
}

model_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'DeepModel', 'model.tflite')


def get_outer_key(inner_key, my_dict):
    for outer_key, inner_dict in my_dict.items():
        if inner_key in inner_dict:
            value = inner_dict[inner_key]
            print(f"The value of '{inner_key}' is '{value}'")
            return outer_key
    return None

def post_text_to_rest_api(prediction_class):
            modified_text = str(prediction_class)
            text_object = MyImage.objects.create(text=modified_text)
            serializer = MyImageModelSerializer(text_object)


def convert_base64_image(base64_val):
            im = Image.open(BytesIO(b64decode(base64_val.split(',')[1])))
            new_image = Image.new("RGBA", im.size, "WHITE")
            new_image.paste(im, (0, 0), im)
            if new_image.mode not in ("L", "RGB"):
                new_image = new_image.convert("RGB")
            new_image= new_image.resize((224,224))
            new_image=np.array(new_image)
            return new_image

            





def model_classification(img):
            interpreter =Interpreter(model_path)
            interpreter.allocate_tensors()
            input_data = np.expand_dims(img.astype(np.uint8), axis=0)
            input_details = interpreter.get_input_details()
            interpreter.set_tensor(input_details[0]['index'], input_data)
            interpreter.invoke()
            output_details = interpreter.get_output_details()
            output_tensor = interpreter.get_tensor(output_details[0]['index'])
            output_array = output_tensor[0]
            predicted_class_index = np.argmax(output_array)
            print(predicted_class_index)
            inner_key = predicted_class_index
            outer_key = get_outer_key(inner_key, arabic_letters)
            print(f"The parent class of'{inner_key}' is '{outer_key}'")

            return inner_key,outer_key






# create a view to handle post requests
@csrf_exempt 
def index(request):

    if request.method == 'POST':

        #---------post request------------------
        image = request.POST.get('image')
        text = request.POST.get('text','')
        #-----------convert------------------
        new_image=convert_base64_image(image)
        #-----------classification--------------------
        class_name,parent_class_name=model_classification(new_image)
        #----------------post to api-------------------
        post_text_to_rest_api(parent_class_name)
        #---------------------------

        return HttpResponse('succ')
    else:
        # Handle GET requests here
        # ...

        return HttpResponse('something in post :()')







