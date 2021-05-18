import os
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage


def index(request):
    return render(request, 'index.html')


def upload(request):
    files = request.FILES.getlist('files')
    os.makedirs('/tmp/l3timeit', exist_ok=True)
    storage = FileSystemStorage(location='/tmp/l3timeit')
    file_urls = []
    for f in files:
        storage.save(f.name, f)
        file_urls.append(f.name)
    return render(request, 'upload_success.html', context={'file_names': file_urls})


def download(request):
    pass
