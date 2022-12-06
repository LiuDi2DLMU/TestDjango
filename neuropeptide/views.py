import json
import os
import random
import string

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.core.files.storage import default_storage
from django.conf import settings
from Bio import SeqIO
from io import StringIO

from .forms import add_task


# 验证是否为fasta格式、长度是否小于100、是否是二十种氨基酸
def is_fasta(str_fasta):
    fasta = SeqIO.parse(StringIO(str_fasta), "fasta")
    if not any(fasta):
        return False
    else:
        count = 0
        for record in fasta:
            count += 1
            if len(record.seq) > 100:
                return False
            else:
                temp = ['A', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'K', 'L',
                        'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'V', 'W', 'Y']
                for i in record.seq:
                    if i not in temp:
                        return False
            if count == 100:
                return False
    return True


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
    fasta_content = None
    if email == "":
        content["state"] = 0
        content["content"] = "Submit failed, the email is required."
    elif fasta_file and fasta_str:
        content["state"] = 0
        content["content"] = "Only one submission is required for file and data."
    elif not (fasta_file or fasta_str):
        content["state"] = 0
        content["content"] = "A file or data must be submitted."
    else:
        if fasta_file:
            fasta_content = fasta_file.read()
            if len(fasta_file) > 512000:
                content["state"] = 0
                content["content"] = "The file size needs to be less than 500kb."
        else:
            fasta_content = fasta_str
        if not is_fasta(fasta_content):
            content["state"] = 0
            content["content"] = "The data you entered or the file you uploaded does not meet the requirements."
    if content["state"] == 1:
        try:
            # 文件保存
            new_file_name = "".join(random.sample([x for x in string.ascii_letters + string.digits], 10)) + ".fasta"
            file_path = os.path.join(settings.STORAGE_LOCATION, "neuropeptide")
            # 暴力尝试9999次无重复即可
            for i in range(9999):
                if os.path.exists(os.path.join(file_path, new_file_name)):
                    new_file_name = "".join(random.sample([x for x in string.ascii_letters + string.digits], 10))
                else:
                    break
            if os.path.exists(os.path.join(file_path, new_file_name)):
                raise Exception("Unknown error")
            with open(os.path.join(file_path, new_file_name), "a+") as file:
                file.writelines(fasta_content)
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
