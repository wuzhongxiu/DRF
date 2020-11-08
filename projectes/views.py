from django.shortcuts import render
from django.http.response import JsonResponse
from django.views import View
# Create your views here.
import json
from .models import ProBi
class Projectes(View):
    # get 获取资源，得到项目的列表
    def get(self,request):
        #1.去数据库查询所以的数据
        db_data_all = ProBi.objects.all()
        db_data={
            "data":[],
        }
        count = 0
        for data in db_data_all:
            db_dic={
                "p_id":data.p_id,
                "p_name":data.p_name,
                "p_tester":data.p_tester,
                "p_rd":data.p_rd,
                "p_desc":data.p_desc,
                "create_time":data.create_time,
            }
            count += 1
            db_data["data"].append(db_dic)
        #2，返回一个json对象给前端
        ret = db_data.update({"msg":"sucess","code":1,"total":count})
        return JsonResponse(db_data)
    # post 创建资源，创建一个项目
    def post(self,request):
        # 1. 接收前端发来的数据，进行转换成python的数据格式字典
        get_data = request.body
        try:
            get_json_data = json.loads(get_data)
        except Exception as  e:
            return  JsonResponse({
            "msg":"json解析错误",
            'code':0
        })
        # 2. 对解析的数据进行校验
        if "p_name" not in get_json_data or "p_tester" not in get_json_data:
            return JsonResponse({
                "msg": "参数错误",
                'code': 0
            })
        # 对p_name字段重复性进行校验
        try:
            qs = ProBi.objects.get(p_name__contains=get_json_data["p_name"])
            if qs.p_name == get_json_data["p_name"]:
                return JsonResponse({
                    "msg": "p_name重复",
                    'code': 1
                })
        except Exception as  e:
            # 当没有这个 项目名称时，我就向数据增加前端传来的数据
            # 3. 合格数据进行数据库的creta()
            db_data = ProBi.objects.create(**get_json_data)
            db_dic = {
                "p_name":db_data.p_name,
                "p_tester":db_data.p_tester,
                "p_rd":db_data.p_rd,
                "p_create":db_data.create_time
            }
            ret = db_dic.update({
                "msg":"创建成功",
                "code":1
            })
            # 4. 返回前端json数据
            return JsonResponse(db_dic)


class Projectes_pk(View):
    # 某一个项目的详情页
    def get(self,request,pk):
        # print(request.GET)
        # 1.获取到pk 这个id，去数据库查询id=pk的这条数据
        try:
            db_id = ProBi.objects.get(p_id__exact=pk)
            db_dic = {
                "p_id": db_id.p_id,
                "p_name": db_id.p_name,
                "p_tester": db_id.p_tester,
                "p_rd": db_id.p_rd,
                "p_desc": db_id.p_desc,
                "create_time": db_id.create_time,
            }
            return JsonResponse(db_dic)
        except Exception as e:
            return JsonResponse({"msg":"id不存在","code":0})
    # 更新put
    def put(self,request,pk):
        #1.先获取前端要修改的数据
        upate_data = request.body
        upate_data_dic = json.loads(upate_data)
        # 校验参数
        #2.根据pk查询数据库的数据，前端数据与数据库数据进行修改（更新）
        try:
            db_data = ProBi.objects.get(p_id__exact=pk)
            # 3.返回更新的json
        except Exception as e:
            return JsonResponse({
                "msg": "参数错误"
            })
        # 更新操作
        db_data.p_name = upate_data_dic.get("p_name")
        db_data.p_tester = upate_data_dic.get("p_tester")
        db_data.p_rd = upate_data_dic.get("p_rd")
        db_data.p_desc = upate_data_dic.get("p_desc")
        db_data.save()
        print(db_data)
        # 向前端返回数据
        db_dic = {
            "p_id": db_data.p_id,
            "p_name": db_data.p_name,
            "p_tester": db_data.p_tester,
            "p_rd": db_data.p_rd,
            "p_desc": db_data.p_desc,
            "create_time": db_data.create_time,
        }
        return JsonResponse(db_dic)

    # 删除delete
    def delete(self,request,pk):
        # 1.先去查询要删除的pk
        ProBi.objects.filter(pk=pk).delete()
        return JsonResponse(
           {"msg": "删除成功", "code": 1},status=204
        )









