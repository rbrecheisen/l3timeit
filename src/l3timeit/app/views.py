from django.shortcuts import render


def index(request):
    return render(request, 'index.html')


def upload(request):
    files = request.FILES.getlist('files')
    file_names = []
    for f in files:
        file_names.append(f.name)
    return render(request, 'upload_success.html', context={'file_names': file_names})


def download(request):
    pass
