from .models import *
from django.shortcuts import render
from django.http import Http404
from django.http import HttpResponse
from .forms import UploadFileForm
from random import randint
from random import seed
from io import BytesIO
import numpy as np
import queue

NUMBER_OF_RESOURCES = 4

def index(request):
    file_list = FileDetails.objects.all()
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
        elif (random_int == 2):
            entry = FilePartitionTwo(byte_array=current, next_id=id, next_table=table)
        elif (random_int == 3):
            entry = FilePartitionThree(byte_array=current, next_id=id, next_table=table)
        elif (random_int == 4):
            entry = FilePartitionFour(byte_array=current, next_id=id, next_table=table)
        if(entry == None):
            break #something went wrong
        else:
            entry.save()
            id = entry.id
            table = random_int
    FileDetails(owner="get from session", file_name = file.name, file_type = "later", head_id = id, head_table = table).save()

def select_table(id, table):
    if(table == 1):
        return FilePartitionOne.objects.get(pk=id)
    elif (table == 2):
        return FilePartitionTwo.objects.get(pk=id)
    elif (table == 3):
        return FilePartitionThree.objects.get(pk=id)
    elif (table == 4):
        return FilePartitionFour.objects.get(pk=id)

def download(request, filedetails_id):
    try:
        filedetail = FileDetails.objects.get(pk=filedetails_id)
    except FileDetails.DoesNotExist:
        raise Http404("File does not exist")
    chunk_queue = []
    id = filedetail.head_id
    table = filedetail.head_table
    while id != 0 and table != 0:
        current = select_table(id, table)
        chunk_queue.append(current.byte_array)
        id = current.next_id
        table = current.next_table
    #put it together
    #new_name = filedetail.file_name + "download"
    #f = open(new_name, 'wb')
    return HttpResponse("hi")