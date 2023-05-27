from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.http import HttpResponseBadRequest
from PIL import Image
from io import BytesIO
from base64 import b64decode
import base64
import cv2
import numpy as np
import os
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.lite.python.interpreter import Interpreter
from .models import MyImage,MyVoiceParent
from .api.serializers import MyImageModelSerializer,MyVoiceParentModelSerializer
from rest_framework.response  import Response
#--------------
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from pydub import AudioSegment
from django.core.files.storage import FileSystemStorage
from django.core.files import File

from .models import Challenges,WordsExam,LettersExam,CorrectionWords,CorrectionLetters



# Create your views here.
# Create your views here.
arabic_letters = {
    'ء': {46: 'ء'},
    'أ': {91: 'أ',40: 'ـأ'},
    'ؤ': {41: 'ؤ'},
    'إ': {19: 'إ',90: 'ـإ'},
    'ا': {105: 'ا',39: 'ـا'},
    'ئ': {37: 'ـئ',  74: 'ـئـ'},
    'ب': {16: 'ب', 31: 'ـب', 100: 'بـ', 4: 'ـبـ'},
    'ت': {1: 'ت', 77: 'ـت', 61: 'تـ', 102: 'ـتـ'},
    'ث': {82: 'ث', 23: 'ـث', 2: 'ثـ', 58: 'ـثـ'},
    'ج': {99: 'ج', 27: 'ـج', 48: 'جـ', 89: 'ـجـ'},
    'ح': {9: 'ح', 54: 'ـح', 81: 'حـ', 17: 'ـحـ'},
    'خ': {12: 'خ', 73: 'ـخ', 76: 'خـ',79: 'ـخـ'},
    'د': {93: 'د', 84: 'ـد'},
    'ذ': {65: 'ذ', 94: 'ـذ'},
    'ر': {34: 'ر', 71: 'ـر'},
    'ز': {88: 'ز', 8: 'ـز'},
    'س': {63: 'س', 0: 'ـس', 49: 'سـ', 43: 'ـسـ'},
    'ش': {22: 'ش', 38: 'ـش', 62: 'شـ', 20: 'ـشـ'},
    'ص': {52: 'ص', 5: 'ـص', 80: 'صـ', 104: 'ـصـ'},
    'ض': {68: 'ض', 75: 'ـض', 29: 'ضـ', 69: 'ـضـ'},
    'ط': {28: 'lط', 87: 'ـط', 50: 'طـ', 98: 'ـط'}, #i am not sure
    'ظ': {45: 'ظ',26: 'ـظ', 70: 'ظـ', 15: 'ـظـ', 'medial2': '\uFECA'},#i am not sure
    'ع': {13: 'ع', 3: 'ـع', 32: 'عـ', 14: 'ـعـ'},
    'غ': {57: 'غ', 96: 'ـغ', 85: 'غـ', 21: 'gyn middle'},# iam not sure
    'ف': {107: 'ف', 25: 'ـف', 55: 'فـ', 51: 'ـفـ'},
    'ق': {47: 'ق', 101: 'ـق', 18: 'قـ', 97: 'ـقـ', 'medial2': '\uFEDE'},
    'ك': {44: 'ك', 103: 'ـك', 78: 'كـ', 66: 'ـكـ'},
    'ل': {106: 'ل', 7: 'ـل', 30: 'لـ', 56: 'ـلـ'},
    'م': {35: 'م', 11: 'ـم', 64: 'مـ', 95: 'ـمـ'},
    'ن': {72: 'ن', 86: 'ـن',24: 'نـ', 92: 'ـنـ'},
    'ه': {67: 'اه', 60: 'ـه', 6: 'هـ', 42: 'ـهـ'},
    'و': {33: 'و',36: 'ـو'},
    'ي': {59: 'ي', 10: 'ـي', 83: 'يـ', 35: 'م', 'medial2': '\uFEF6'},
 
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


def post_letter_to_rest_api(prediction_class,AcutalClass,letterid):
    if prediction_class!=AcutalClass:
        correction=0
    else:
        correction=1
    print(correction)
    CorrectionLetters_object = CorrectionLetters()
    CorrectionLetters_object.correction=correction
    CorrectionLetters_object.letter_ID=LettersExam(id=letterid)
    CorrectionLetters_object.save()
    
 



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
        text = request.POST.get('text')
        letter_id = request.POST.get('letter_id')
        print(text,letter_id)
        #-----------convert------------------
        new_image=convert_base64_image(image)
        #-----------classification--------------------
        class_name,parent_class_name=model_classification(new_image)

        #----------------post to api-------------------
        post_letter_to_rest_api(parent_class_name,text,letter_id)
        post_text_to_rest_api(parent_class_name)
        #---------------------------

        return HttpResponse('succ')
    else:
        # Handle GET requests here
        # ...

        return HttpResponse('something in post :()')




class AudioUploadView(APIView):
    parser_classes = [MultiPartParser]

    def post(self, request):
        audio_file =request.POST.get('audio')
        text =request.POST.get('text')
        #print(audio_file)
        print(type(audio_file))
        wav_file = open("voice.mp3", "wb")
        decode_string = base64.b64decode(audio_file)
        wav_file.write(decode_string)
        voice_in_mp3_format =os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),  'voice.mp3')

        # creating new object
        MyVoiceParent_object = MyVoiceParent()

        # saving the file 
        local_file = open(voice_in_mp3_format, 'rb')
        djangofile = File(local_file)
        MyVoiceParent_object.audio.save("voice.mp3", djangofile)
        local_file.close()

        # adding text 
        MyVoiceParent_object.text = "sdfsdf"

        # saving the object
        MyVoiceParent_object.save()
        return HttpResponse('succ')
        

@csrf_exempt 
def LetterChallUploadView(request):
   

    if request.method == 'POST':
        voice_file =request.POST.get('voice')
        text =request.POST.get('text')
        chall_ID =request.POST.get('challenges_ID')
        print(chall_ID)
        #print(audio_file)
        print(type(voice_file))
        wav_file = open("voice.mp3", "wb")
        decode_string = base64.b64decode(voice_file)
        wav_file.write(decode_string)
        voice_in_mp3_format =os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),  'voice.mp3')

        # creating new object
        LettersExam_object = LettersExam()


        # adding text 
        LettersExam_object.text = text
        #challenges_object_data=Challenges.objects.get(id=chall_ID)
        #c_id=int(challenges_object_data)
        LettersExam_object.challenges_ID = Challenges(id=chall_ID)
        # saving the file 
        local_file = open(voice_in_mp3_format, 'rb')
        djangofile = File(local_file)
        LettersExam_object.voice.save("voice.mp3", djangofile)
        local_file.close()
        # saving the object
        LettersExam_object.save()
        return HttpResponse('succ')
    else:
        return HttpResponse('something in post :()')



@csrf_exempt 
def WordChallUploadView(request):
   

    if request.method == 'POST':
   
        voice_file =request.POST.get('voice')
        text =request.POST.get('text')
        chall_ID =request.POST.get('challenges_ID')
        letterNo=request.POST.get('letter_No')
        print(chall_ID)
        #print(audio_file)
        print(type(voice_file))
        wav_file = open("voice.mp3", "wb")
        decode_string = base64.b64decode(voice_file)
        wav_file.write(decode_string)
        voice_in_mp3_format =os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),  'voice.mp3')

        # creating new object
        WordsExam_object = WordsExam()


        # adding text 
        WordsExam_object.text = text
        #challenges_object_data=Challenges.objects.get(id=chall_ID)
        #c_id=int(challenges_object_data)
        WordsExam_object.challenges_ID = Challenges(id=chall_ID)
        
        WordsExam_object.letter_No=letterNo
        
        # saving the file 
        local_file = open(voice_in_mp3_format, 'rb')
        djangofile = File(local_file)
        WordsExam_object.voice.save("voice.mp3", djangofile)
        local_file.close()
        # saving the object
        WordsExam_object.save()
        return HttpResponse('succ')
    else:
        return HttpResponse('something in post :()')

        

           
def post_word_to_rest_api(prediction_class,AcutalClass,Wordid):
    if prediction_class!=AcutalClass:
        correction=0
    else:
        correction=1
    print(correction)
    CorrectionWord_object = CorrectionWords()
    CorrectionWord_object.correction=correction
    CorrectionWord_object.words_ID=WordsExam(id=Wordid)
    CorrectionWord_object.save()
    
 


# create a view to handle post requests
@csrf_exempt 
def indexWord(request):

    if request.method == 'POST':

        #---------post request------------------
        print("shhsu")
        word=''
        image0 = request.POST.get('image0')
        image1 = request.POST.get('image1')
        image2 = request.POST.get('image2')
        image3 = request.POST.get('image3')
        text = request.POST.get('text')
        words_id = request.POST.get('words_id')
        print(words_id,text)
        imagesForWord=[image0,image1,image2,image3]

        for x in imagesForWord:
            new_image=convert_base64_image(x)
            class_name,parent_class_name=model_classification(new_image)
            print(parent_class_name)
            word+=parent_class_name

        post_word_to_rest_api(word,text,words_id)
        print(word)
        print("محمد")
        

        return HttpResponse('succ')
    else:
        # Handle GET requests here
        # ...

        return HttpResponse('something in post :()')

