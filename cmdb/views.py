from django.shortcuts import render,HttpResponse,redirect
from django.core import serializers
from cmdb import models
import json
# Create your views here.
def hosts(request):
    for k,v in request.environ.items():
        print(k,v)
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

def block(request):
    return render(request,'block.html')

def testfunc(request):
    return render(request,'testfunc.html')


from django.utils.safestring import mark_safe

class Page():
    def __init__(self, current_page, data_count, per_page_count=10, pager_num=7):
        self.current_page = current_page
        self.data_count = data_count
        self.per_page_count = per_page_count
        self.pager_num = pager_num

    @property
    def start(self):
        return (self.current_page-1) * self.per_page_count

    @property
    def end(self):
        return self.current_page * self.per_page_count

    @property
    def all_count(self):
        count, y = divmod(self.data_count, self.per_page_count)
        if y != 0:
            count += 1
        return count

    def page_str(self, base_url):
        page_str = []
        if self.all_count <= self.pager_num:
            start_index = 1
            end_index = self.pager_num + 1
        else:
            if self.current_page < self.pager_num:
                start_index = 1
                end_index = self.pager_num + 1
            elif self.current_page + (self.pager_num - 1) / 2 > self.all_count:
                start_index = self.all_count - self.pager_num
                end_index = self.all_count
            else:
                start_index = self.current_page - (self.pager_num - 1) / 2
                end_index = self.current_page + (self.pager_num + 1) / 2
        if self.current_page == 1:
            prev = "<a class='base' href='javascript:void(0);'>上一页</a>"
        else:
            prev = "<a class='base' href='%s?p=%s'>上一页</a>" % (base_url,self.current_page - 1)
        page_str.append(prev)
        for i in range(int(start_index), int(end_index)):
            if i == self.current_page:
                str = "<a class='base active' href='%s?p=%s'>%s</a>" % (base_url,i, i)
            else:
                str = "<a class='base' href='%s?p=%s'>%s</a>" % (base_url,i, i)
            page_str.append(str)
        if self.current_page == self.all_count:
            next = "<a class='base' href='javascript:void(0);'>下一页</a>"
        else:
            next = "<a class='base' href='%s?p=%s'>下一页</a>" % (base_url, self.current_page + 1)
        page_str.append(next)
        jump = '''
                <input type="text"><a id='a1' onclick='jump(this);'>GO</a>
                <script>
                    function jump(ths) {
                        var inp = ths.previousSibling
                        var val = inp.value
                        location.href = '%s' + val
                    }
                </script>
            ''' % base_url
        page_str.append(jump)
        page_str = "".join(page_str)
        page_str = mark_safe(page_str)
        return page_str


LIST = [ i for i in range(501)]
def page_list(request):
    current_page = int(request.GET.get('p',1))
    page_obj = Page(current_page,len(LIST))
    data = LIST[page_obj.start:page_obj.end]
    page_str = page_obj.page_str('page_list')

    return render(request,'page_list.html',{'data':data,'page_str':page_str})







