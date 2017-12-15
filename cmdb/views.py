from django.shortcuts import render,HttpResponse,redirect
from django.core import serializers
from cmdb import models
import json
# Create your views here.
def hosts(request):
    if request.method == 'GET':
        v1 = models.Hosts.objects.all() #对象
        # print(v1)
        v2 = models.Business.objects.all().values() #字典
        #print(v2)
        v3 = models.Business.objects.all().values_list() #元组
        #print(v3)
        business_info = models.Business.objects.all()

        ####测试跨表查询
        v4 = models.Hosts.objects.all().values('hostname','business__caption')
        ####


        return render(request,'hosts.html',{'v1':v1,'v2':v2,'v3':v3,'business_info':business_info,'v4':v4})
    elif request.method == 'POST':
        h = request.POST.get('hostname')
        ip = request.POST.get('ip')
        port = request.POST.get('port')
        b_id = request.POST.get('bus')
        print(h,ip,port,b_id)
        models.Hosts.objects.create(hostname=h,ip=ip,port=port,business_id=b_id)
        return redirect('/cmdb/hosts')

def ajax_test(request):
    ret = {'status':True,'error':None,'data':None}
    try:
        if request.method == 'POST':
            hid = request.POST.get('hid')
            h = request.POST.get('hostname')
            ip = request.POST.get('ip')
            port = request.POST.get('port')
            bus = request.POST.get('bus')
            print(hid,h,ip,port,bus)
            if h and len(h) > 2:
                print(1)
                models.Hosts.objects.filter(id=hid).update(hostname=h,ip=ip,port=port,business_id=bus)
                print(2)
            else:
                print('else执行了 ')
                ret['status'] = False
                print(ret['status'])
                ret['error'] = '机器名太短了'

    except:
        ret['status'] = False
        ret['error'] = '出错了'
    print(ret)
    return HttpResponse(json.dumps(ret))

def ajax_del(request):
    ret = {'status':True,'error':None,'data':None}
    try:
        if request.method == 'POST':
            delhid = request.POST.get('delhid')
            models.Hosts.objects.filter(id=delhid).delete()
    except:
        ret['status'] = False
        ret['error'] = '出错了'
    return HttpResponse(json.dumps(ret))


def apps(request):
    if request.method =='GET':
        apps = models.Application.objects.all()
        return render(request,'apps.html',{'apps':apps})

def apphosts(request):
    ret = {'status':True, 'error':None, 'data':None}
    try:
        if request.method == 'GET':
            info = models.Application.objects.all()
            v1 = models.Hosts.objects.all()
            return render(request,'apphosts.html',{'info':info,'v1':v1})
            # return HttpResponse('ok')
        elif request.method == 'POST':
            name = request.POST.get('app')
            hostid = request.POST.getlist('host')
            app_ididid = request.POST.get('ididid')
            app11 = request.POST.get('app11')
            host11 = request.POST.getlist('host11')
            delid = request.POST.get('appid')
            if name and len(name) > 2:
                obj = models.Application.objects.create(name=name)
                obj.r.add(*hostid)
            elif app11 and len(app11) >2 and host11:
                obj = models.Application.objects.get(id=app_ididid)
                obj.name = app11
                obj.save()
                obj.r.set(host11)
            elif delid:
                models.Application.objects.filter(id=delid).delete()
            else:
                ret['status'] = False
                ret['error'] = '业务名太短'

    except:
        ret['status'] = False
        ret['error'] = '出错了'
    print(ret)
    return HttpResponse(json.dumps(ret))











