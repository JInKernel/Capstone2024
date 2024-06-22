from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
import cv2
import dlib
import numpy as np
from PIL import Image
import json
from io import BytesIO
import base64
import uuid
import os
from django.conf import settings
from tensorflow.keras.models import load_model 
from tensorflow.keras.preprocessing.image import img_to_array 
import time
from .models import Beverage
from django.contrib.auth.models import User
import random


age_list = ['under', 'over']
emotion_list = ['Red', 'Green']
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("model_library/shape_predictor_68_face_landmarks.dat")
face_rec_model = dlib.face_recognition_model_v1("model_library/dlib_face_recognition_resnet_model_v1.dat")

age_model = load_model("model_library/model_age_estimation15.h5")
emotion_model = load_model("model_library/model_estimation6.h5")

def index(request):
    return render(request, "justfortest/mega_start.html")

def under60(request):
    return render(request,"justfortest/mega_under50.html")

def over60(request):
    return render(request,"justfortest/mega_over50.html")


def get_face_feature_vector(img_path):
    img = cv2.imread(img_path)
    if img is None:
        raise ValueError(f"Image not loaded properly from path: {img_path}")

    # Check if the image is in RGB format
    if len(img.shape) < 3 or img.shape[2] != 3:
        raise ValueError("Image is not in RGB format")

    # Convert the image to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Ensure the image is 8-bit grayscale
    if gray.dtype != np.uint8:
        gray = cv2.normalize(gray, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)

    # Debugging: Check the shape and type of the grayscale image
    print(f"Gray image shape: {gray.shape}, dtype: {gray.dtype}")

    # Detect faces in the image
    faces = detector(gray)
    if len(faces) == 0:
        raise ValueError("Cannot find any face")

    # Process the first face found
    face = faces[0]
    shape = predictor(gray, face)
    face_descriptor = face_rec_model.compute_face_descriptor(img, shape)

    return np.array(face_descriptor)

# db_face_vector_path = "images"
# db_face_feature_vectors = []
# db_face_vector_files = []
# for file_name in os.listdir(db_face_vector_path):
#     if file_name.endswith(".npy"):
#         file_path = os.path.join(db_face_vector_path, file_name)
#         db_face_feature_vectors.append(np.load(file_path))
#         db_face_vector_files.append(file_name)
start = time.time()
def process_image(filepath, detector, age_model, emotion_model, age_list, emotion_list):

    img = cv2.imread(filepath)
    print("시작함")
    faces = detector(img, 1)
    try:
        faces = detector(img, 1)
        if len(faces) < 1:  # 얼굴이 탐지되지 않았을 때
            raise ValueError("No faces detected in the image.")
    except Exception as e:
        print("Error occurred during face detection: ", str(e))
        return

    for face in faces:
        x1, y1, x2, y2 = face.left(), face.top(), face.right(), face.bottom()

        # 얼굴 영역의 크기와 위치를 확인하여 적절한 프레임인지 판단
        face_area = (x2 - x1) * (y2 - y1)
        frame_area = img.shape[0] * img.shape[1]
        face_ratio = face_area / frame_area
        age = None
        emotion = None

        if face_ratio > 0.1:  # 얼굴 영역이 프레임의 20% 이상일 때만 처리
            face_img = img[y1:y2, x1:x2].copy()
            face_img_gray = cv2.cvtColor(face_img, cv2.COLOR_BGR2GRAY)

            # Age estimation preprocessing
            face_img_age = cv2.resize(face_img_gray, (128, 128))
            face_img_age = face_img_age.astype("float") / 255.0
            face_img_age = img_to_array(face_img_age)
            face_img_age = np.expand_dims(face_img_age, axis=0)

            # Emotion estimation preprocessing
            face_img_emotion = cv2.resize(face_img_gray, (48, 48))
            face_img_emotion = face_img_emotion.astype("float") / 255.0
            face_img_emotion = img_to_array(face_img_emotion)
            face_img_emotion = np.expand_dims(face_img_emotion, axis=0)

            # Prediction
            age_preds = age_model.predict(face_img_age)
            age = age_list[np.argmax(age_preds)]
            emotion_preds = emotion_model.predict(face_img_emotion)
            emotion = emotion_list[np.argmax(emotion_preds)]

            
            # Visualize result
            cv2.rectangle(img, (x1, y1), (x2, y2), (255, 255, 255), 2)
            overlay_text = '%s, %s' % (age, emotion)
            cv2.putText(img, overlay_text, (x1, y1-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
            # print("Age :", age)
            # print("Emotion :", emotion)
        
    return age, emotion

def get_matched_files(db_face_feature_vectors, live_face_feature_vector, db_face_vector_files):
    distances = np.linalg.norm(np.array(db_face_feature_vectors) - live_face_feature_vector, axis=1)
    min_distances = np.where(distances < 0.5)[0]
    matched_files = []

    if len(min_distances) > 0:
        matched_files = [db_face_vector_files[idx] for idx in min_distances]
        print("기존 회원:")
        for file_name in matched_files:
            print("이순재 님 환영합니다.")
    else:
        print("등록되지 않은 회원입니다.")

    return matched_files


def get_prediction(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        image_data = data.get('image')

        db_face_vector_path = "images/feature_vectors"
        db_face_feature_vectors = []
        db_face_vector_files = []
        for file_name in os.listdir(db_face_vector_path):
            if file_name.endswith(".npy"):
                file_path = os.path.join(db_face_vector_path, file_name)
                db_face_feature_vectors.append(np.load(file_path))
                db_face_vector_files.append(file_name)
        

        format, imgstr = image_data.split(';base64,')
        ext = format.split('/')[-1]

        image = Image.open(BytesIO(base64.b64decode(imgstr)))
        rgb_image = image.convert('RGB')

        filename = '{}.{}'.format(uuid.uuid4(), 'jpg')
        filepath = os.path.join(settings.MEDIA_ROOT, filename)
        
        os.makedirs(os.path.dirname(filepath), exist_ok=True)

        rgb_image.save(filepath)

        # 이미지를 저장한 후, 저장된 파일이 존재하는지 확인합니다.
        if not os.path.exists(filepath):
            raise ValueError(f"Image file was not saved properly at path: {filepath}")

        
        # 얼굴 특징 벡터를 추출합니다.
        face_feature_vector = get_face_feature_vector(filepath)
        print(face_feature_vector)

        age,emotion = process_image(filepath, detector, age_model, emotion_model, age_list, emotion_list)
        print("Age :", age)
        print("Emotion :", emotion)

        users = User.objects.all()
        for user in users:
            print(user.username)

        get_matched_files(db_face_feature_vectors, face_feature_vector, db_face_vector_files)

        beverages = Beverage.objects.all()
        random_beverages = random.sample(list(beverages), 6)

        beverage_names = [beverage.name for beverage in random_beverages]
        # 출력
        recommendation = "추천 음료: " + ', '.join(beverage_names)

        print(recommendation)

        if os.path.exists(filepath):
            os.remove(filepath)
        
    # 나이에 따른 URL 반환
        if age =='over':
            return JsonResponse({"prediction": "over"})
        else:
            return JsonResponse({"prediction": "under"})
    else:
        return JsonResponse({"error": "Invalid request method"}, status=400)
