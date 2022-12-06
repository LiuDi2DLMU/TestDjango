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
from django.db.models import Q


def sent_email(state, record, result_file_path=None, content: str = None):
    """
    该函数是用于发送邮件的
    :param state: 表示任务的状态，1表示成功，0表示失败，用于调用函数中默认的邮件内容。
    :param record: 任务的具体信息，也就是对应的数据库记录。
    :param result_file_path: 任务如果过程，结果文件的路径，以附件的形式返回给用户。
    :param content: 自定义的邮件内容，为空则使用函数中默认的邮件内容。
    :return: 无返回值
    """
    mail_host = settings.MAIL_HOST
    mail_sender = settings.MAIL_SENDER
    mail_passwd = settings.MAIL_PASSWD
    # 主题设置
    msg = MIMEMultipart()
    msg["Subject"] = "带有附件的邮件"
    msg["From"] = mail_sender
    msg["To"] = record.email
    # 成功的邮件模板
    success_mail_content = f'''
        Dear {record.name},
        您在XXX提交的任务已完成，结果将随这本邮件，以附件的形式发送给您。
    '''
    #
    fail_mail_content = f'''
        Dear {record.name},
        出于未知原因，您的任务失败了，我们对此万分抱歉。
    '''

    if state:
        mail_content = success_mail_content
    else:
        mail_content = fail_mail_content

    if content is not None:
        mail_content = content

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
    """
    用于执行对应的神经肽任务
    :param record: 执行任务对应的数据库记录
    :return: 无返回
    """
    file_path = os.path.join(settings.STORAGE_LOCATION, "neuropeptide", record.filename)
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
        result_file_path = out["content"]
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
    clean_time = int(time.time())
    task_count = 0
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
            print("执行神经肽任务")
            task_count += 1
            run_neuropeptide(run_record)
        elif task_name == "zsm":
            print("执行师兄任务")
            task_count += 1
            run_zsm(run_record)
        elif task_name is None:
            # 暂无任务
            time.sleep(settings.SLEEP_TIME)
            print(f"No task, sleep {settings.SLEEP_TIME} seconds")

        if int(time.time()) - clean_time >= settings.CLEAN_TIME or task_count >= settings.CLEAN_COUNT:
            # 清理数据库，将所有非待执行的记录删除
            clean_time = time.time()
            task_count = 0
            file_path = settings.STORAGE_LOCATION
            for i in range(len(tables)):
                # task_name 用于表明到底是哪个任务的记录，删除文件的位置或许有影响
                task_name = task_names[i]
                records = tables[i].objects.filter(~Q(state=0))
                for temp in records:
                    # 优先清理保存文件
                    if task_name == "neuropeptide":
                        result_filename = temp.filename.split(".")[0] + ".csv"
                        if os.path.exists(os.path.join(file_path, task_name, result_filename)):
                            os.remove(os.path.join(file_path, task_name, result_filename))
                        if os.path.exists(os.path.join(file_path, task_name, temp.filename)):
                            os.remove(os.path.join(file_path, task_name, temp.filename))
                    print(task_name, "delete record")
                    temp.delete()


run_task()
