from .models import *
from django.shortcuts import render
from django.http import Http404
from django.http import HttpResponse
from .forms import UploadFileForm
from random import randint
from random import seed
from io import BytesIO
import numpy as np

NUMBER_OF_RESOURCES = 4

def index(request):
    file_list = FileDetails.objects
    context = {'file_list': file_list }
    return render(request, 'cloudsecurity/index.html', context)

def upload(request): #URL
    if request.method == 'POST' and request.FILES['myfile']:
        file = request.FILES['myfile']
        process_file(file)
        return HttpResponse("File has been uploaded")
    else:
        form = UploadFileForm
    return render(request, 'cloudsecurity/upload.html', {'form': form})

def process_file(file):
    chunk_stack = []
    for chunk in file.chunks():
        file_chunk = BytesIO(chunk)
        binary_chunk = list(file_chunk)
        chunk_stack.append(binary_chunk)
    id = 0
    table = 0
    while chunk_stack:
        current = np.asarray(chunk_stack.pop())
        seed(1)
        random_int = randint(1, 4)
        entry = None
        if(random_int == 1):
            entry = FilePartitionOne(byte_array=current, next_id = id, next_table = table)
        if (random_int == 2):
            entry = FilePartitionTwo(byte_array=current, next_id=id, next_table=table)
        if (random_int == 3):
            entry = FilePartitionThree(byte_array=current, next_id=id, next_table=table)
        if (random_int == 4):
            entry = FilePartitionFour(byte_array=current, next_id=id, next_table=table)
        if(entry == None):
            break #something went wrong
        else:
            entry.save()
            id = entry.id
            table = random_int
    FileDetails(owner="get from session", file_name = file.name, file_type = "later", head_id = id, head_table = table).save()

# def detail(request, question_id):
#     try:
#         question = Question.objects.get(pk=question_id)
#     except Question.DoesNotExist:
#         raise Http404("Question does not exist")
#     return render(request, 'polls/detail.html', {'question': question})