from django.db import models

# Create your models here.k
# 创建一个模型类
class ProBi(models.Model):
    p_id = models.AutoField(primary_key=True)
    p_name = models.CharField(max_length=20, unique=True,verbose_name="项目名字", help_text="项目名字")
    p_tester=models.CharField(max_length=5)
    p_rd=models.CharField(max_length=5) # 项目开发人员
    p_desc=models.TextField(verbose_name="项目简介",blank=True)
    create_time = models.DateTimeField(auto_now_add=True,verbose_name="创建记录时间")
    update_time = models.DateTimeField(auto_now=True,verbose_name="更新记录时间")
    class Meta:
        db_table='project_biao'
        verbose_name="项目表"