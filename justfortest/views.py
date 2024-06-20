from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse


def index(request):
    return render(request, "justfortest/mega_start.html")

def under60(request):
    return render(request,"justfortest/mega_under50.html")

def over60(request):
    return render(request,"justfortest/mega_over50.html")


def get_prediction(request):
    return JsonResponse({"prediction": "over"})

def receive_stream_data(request):
    if request.method == 'POST':
        # 클라이언트에서 보낸 영상 데이터를 받아 저장
        video_data = request.FILES.get('video_data')
        if video_data:
            file_path = os.path.join('media', 'received_video.webm')
            with open(file_path, 'wb') as file:
                for chunk in video_data.chunks():
                    file.write(chunk)
            return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'})