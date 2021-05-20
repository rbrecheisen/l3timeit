import os

from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from django.utils import timezone
from django.core.files import File
from .models import ImageModel


def upload(request):
    if request.method == 'GET':
        return render(request, 'upload.html')
    elif request.method == 'POST':
        files = request.FILES.getlist('files')
        images = []
        for f in files:
            img = ImageModel.objects.create(file_obj=f, file_name=f.name)
            images.append(img)
        return render(request, 'files.html', context={'images': images})


def files(request):
    images = ImageModel.objects.all()
    return render(request, 'files.html', context={'images': images})


def download(request):
    file_name = request.GET['file_name']
    img = ImageModel.objects.filter(file_name=file_name).first()
    img.downloaded_at = timezone.now()
    img.locked = True
    img.save()
    with open(img.file_obj.path, 'rb') as f:
        response = HttpResponse(File(f), content_type='application/octet-stream')
        response['Content-Disposition'] = 'attachment; filename="{}"'.format(img.file_name)
        return response


def timings(request):
    images = ImageModel.objects.all()
    fp = os.path.join(settings.MEDIA_ROOT, 'timings.txt')
    with open(fp, 'w') as f:
        f.write('File,Seconds\n')
        for img in images:
            if img.finished:
                f.write('{},{}\n'.format(img.file_name, img.seconds))
    with open(fp, 'rb') as f:
        response = HttpResponse(File(f), content_type='application/octet-stream')
        response['Content-Disposition'] = 'attachment; filename="timings.txt"'
        return response


def finished(request):
    file_name = request.GET['file_name']
    img = ImageModel.objects.filter(file_name=file_name).first()
    img.done_at = timezone.now()
    img.seconds = int((img.done_at - img.downloaded_at).total_seconds())
    img.finished = True
    img.save()
    images = ImageModel.objects.all()
    return render(request, 'files.html', context={'images': images})


def delete(request):
    images = ImageModel.objects.all()
    for img in images:
        img.delete()
    return render(request, 'files.html')
