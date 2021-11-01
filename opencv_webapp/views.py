from django.shortcuts import render, redirect
from .forms import SimpleUploadForm, ImageUploadForm
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from .cv_functions import cv_detect_face
# Create your views here.
def first_view(request):

    return render(request, 'opencv_webapp/first_view.html', {})


def simple_upload(request):


    if request.method == 'POST':
        # print(request.POST) : <QueryDict: {'csrfmiddlewaretoken': [‘~~~’], 'title': ['upload_1']}>
        # print(request.FILES) : <MultiValueDict: {'image': [<InMemoryUploadedFile: ses.jpg (image/jpeg)>]}>
        # 비어있는 Form에 사용자가 업로드한 데이터를 넣고 검증합니다.
        form = SimpleUploadForm(request.POST, request.FILES)

        if form.is_valid():
            myfile = request.FILES['image'] # 'ses.jpg'
            #FileSystemStorage(),.save(myfile.name, myfile),.url(filename) 한 세트
            fs = FileSystemStorage()
            filename = fs.save(myfile.name, myfile) # 경로명을 포함한 파일명 & 파일 객체
            # 업로드된 이미지 파일의 URL을 얻어내 Template에게 전달
            uploaded_file_url = fs.url(filename) # '/media/ses.jpg'

            context = {'form': form, 'uploaded_file_url': uploaded_file_url} # filled form
            return render(request, 'opencv_webapp/simple_upload.html', context)
# POST 요청 처리 부분 요기까, ImageUploadForm

    else: # request.method == 'GET' (DjangoBasic 실습과 유사한 방식입니다.)
        form = SimpleUploadForm()
        context = {'form': form} # empty form
        return render(request, 'opencv_webapp/simple_upload.html', context)


def detect_face(request):

    if request.method == 'POST' :
        form = ImageUploadForm(request.POST, request.FILES)

        if form.is_valid():
            post = form.save(commit=False)
            post.save()

            imageURL = settings.MEDIA_URL + form.instance.document.name

            cv_detect_face(settings.MEDIA_ROOT_URL + imageURL) 

            context = {'form':form, 'post':post}
            return render(request, 'opencv_webapp/detect_face.html', context)

    else:
        form = ImageUploadForm()

        context = {'form': form} # empty form
        return render(request, 'opencv_webapp/detect_face.html', context)
