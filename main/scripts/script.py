import time
from neuropeptide.models import Task as NeuTask
from zsm.models import Task as ZsmTask
import os
import subprocess
import json
from django.conf import settings
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib


def sent_email(state, record, result_file_path=None):
    mail_host = settings.MAIL_HOST
    mail_sender = settings.MAIL_SENDER
    mail_passwd = settings.MAIL_PASSWD

    msg = MIMEMultipart()
    msg["Subject"] = "带有附件的邮件"
    msg["From"] = mail_sender
    msg["To"] = record.email

    success_mail_content = f'''
        Dear {record.name},
        您在XXX提交的任务已完成，结果将随这本邮件，以附件的形式发送给您。
    '''

    fail_mail_content = f'''
        Dear {record.name},
        出于未知原因，您的任务失败了，我们对此万分抱歉。
    '''

    if state:
        mail_content = success_mail_content
    else:
        mail_content = fail_mail_content

    msg.attach(MIMEText(mail_content, "plain", "utf-8"))

    # 附件
    if result_file_path is not None:
        att = MIMEText(open(result_file_path, "rb").read(), "base64", "utf-8")
        att["Content-Type"] = 'application/octet-stream'
        att["Content-Disposition"] = 'attachment; filename="result.csv"'
        msg.attach(att)

    s = smtplib.SMTP()
    s.connect(mail_host, 25)
    s.login(mail_sender, mail_passwd)
    s.sendmail(mail_sender, [record.email], msg.as_string())
    s.quit()


def run_neuropeptide(record):
    file_path = os.path.join(settings.STORAGE_LOCATION, record.filename)
    email = record.email
    # 上面的是python解释器的路径 利用which python可以获取
    # 下面是脚本的绝对路径位置以及参数
    cmd = f"C:\\ProgramData\\Anaconda3\\envs\\neuropeptide2022-4-25\\python " \
          f"F:\\pythonproject\\neuropeptide2022-11-16\\validate.py --file_path={file_path}"
    subp = subprocess.Popen(cmd, encoding='utf-8', stdout=subprocess.PIPE)
    # 在脚本中通过print打印json格式字符的方式返回值在out.split("\n")[0]里
    out, err = subp.communicate()
    out = json.loads(out.split("\n")[0])
    if out['state']:
        result_file_path = os.path.join(settings.STORAGE_LOCATION, record.filename.split('.')[0]+".csv")
        sent_email(out['state'], record, result_file_path)
        record.state = 1
        record.save()
    else:
        sent_email(out['state'], record)
        record.state = 2
        record.save()
    return


def run_zsm(record):
    return 0


def run_task():
    while True:
        # 每多一个项目，就多一个模型，多一张表，同时允许跑一个项目的脚本
        # 将项目和任务名称对应地填写到tables和task_names
        tables = [NeuTask, ZsmTask]
        task_names = ["neuropeptide", "zsm"]
        latest_records = []
        for i in range(len(tables)):
            latest_records.append(tables[i].objects.filter(state=0).order_by('time').first())

        task_name = None
        run_record = None
        for i in range(len(latest_records)):
            if latest_records[i] is None:
                continue
            elif run_record is None:
                run_record = latest_records[i]
                task_name = task_names[i]
            else:
                a = time.mktime(run_record.time.timetuple())
                b = time.mktime(latest_records[i].time.timetuple())
                if b - a <= 0:
                    task_name = task_names[i]
                    run_record = latest_records[i]
        # 并且在这里增加对应的分支
        if task_name == "neuropeptide":
            run_neuropeptide(run_record)
        elif task_name == "zsm":
            run_zsm(run_record)
        elif task_name is None:
            time.sleep(settings.SLEEPTIME)
            print(f"No task, sleep {settings.SLEEPTIME} seconds")
            # 暂无任务


run_task()