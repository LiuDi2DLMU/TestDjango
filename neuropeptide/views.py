import json
import os
import random
import string

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.core.files.storage import default_storage
from django.conf import settings

from .forms import add_task


def index(request):
    form_task = add_task()
    if request.method == "POST":
        form_task = add_task(request.POST)
    return render(request, 'neuropeptide/index.html', {"form_task": form_task})


def form_submit(request):
    form_task = add_task()
    if request.method == "POST":
        form_task = add_task(request.POST)
    data = form_task.data
    name = data["name"]
    email = data["email"]
    fasta_str = data["data"]
    if request.FILES.keys():
        fasta_file = request.FILES["file"]
    else:
        fasta_file = None
    temp = HttpResponse()
    temp.status_code = 200
    # 返回的state为1 表示成功  content为自定义返回内容
    # 返回值不为1 表示失败
    content = {
        "state": 1,
        "content": "Submit successfully. After the task is completed, the results will be sent to your email."
    }
    if email == "":
        content["state"] = 0
        content["content"] = "Submit failed, the email is required."
    elif fasta_file and fasta_str:
        content["state"] = 0
        content["content"] = "Only one submission is required for file and data."
    elif not (fasta_file or fasta_str):
        content["state"] = 0
        content["content"] = "A file or data must be submitted."
    elif fasta_file:
        if len(fasta_file) > 512000:
            content["state"] = 0
            content["content"] = "The file size needs to be less than 500kb."
        else:
            # TODO fasta格式文件的验证
            b = 1
    elif fasta_str:
        # TODO str的fasta格式验证
        a = 1
    if content["state"] == 1:
        try:
            # 文件保存
            new_file_name = "".join(random.sample([x for x in string.ascii_letters + string.digits], 10)) + ".fasta"
            file_path = settings.STORAGE_LOCATION
            for i in range(9999):
                if os.path.exists(os.path.join(file_path, new_file_name)):
                    new_file_name = "".join(random.sample([x for x in string.ascii_letters + string.digits], 10))
                else:
                    break
            if os.path.exists(os.path.join(file_path, new_file_name)):
                raise Exception("Unknown error")
            if fasta_file:
                default_storage.save(os.path.join(file_path, new_file_name), fasta_file)
            else:
                with open(os.path.join(file_path, new_file_name), "a+") as file:
                    file.writelines(fasta_str)
            # 数据保存到数据库
            from .models import Task
            task = Task()
            task.name = name
            task.email = email
            task.filename = new_file_name
            task.state = 0
            task.save()
        except Exception as e:
            temp.status_code = 500
            content["state"] = 0
            content["content"] = e.args
    temp.content = json.dumps(content)
    return temp


def main(request):
    return redirect("/main/")
