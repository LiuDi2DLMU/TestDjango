from django.db import models


class Task(models.Model):
    time = models.DateTimeField("添加时间", auto_now_add=True)
    name = models.CharField("用户姓名", max_length=255, null=True)
    email = models.EmailField("用户邮箱", max_length=255, null=False)
    state = models.IntegerField("任务状态", null=False)
    filename = models.CharField("文件名", max_length=255, null=False)
    tasktype = models.CharField("任务类型", max_length=255, null=False, default="neuropeptide")

    class Task:
        db_table = "neuropeptide"
