import json
import re

from django.http import HttpResponse
from django.shortcuts import render, redirect

from .models import User, Question, Doctor, Reply, Feedback

import sys
sys.path.append('F:/MedicalQA-KG')

from Neo4j import disease, symptom, drug, department, population
from QA import question_classify


# Create your views here.
def index(request):
    user_role = request.COOKIES.get('user_role', '')
    username = request.COOKIES.get('username', '')
    print(user_role, username, 'aaaaaaaaaaaaa')
    return render(request, 'wenda/index.html')


def search(request):
    if request.method == 'POST':
        data = dict()
        data['search_text'] = request.POST['search_text']
        return render(request, 'wenda/search.html', {'data': data})
    else:
        return render(request, 'wenda/404.html')


def info_brief_ajax(request):
    if request.is_ajax():
        more_text = request.GET['more_type']
        search_text = request.GET['search_text']
        page = int(request.GET['page'])
        page_size = int(request.GET['page_size'])
        print(more_text, search_text, page, page_size)
        if more_text == 'disease':
            handler = disease.Disease()
            diseases_name = handler.fuzzy_search(search_text)
            data = []
            for disease_name in diseases_name[(page*page_size):min(((page+1)*page_size), len(diseases_name))]:
                print(disease_name)
                data.append(handler.disease_info_brief(disease_name))
            json_data = json.dumps({'disease_list': data}, ensure_ascii=False)
            return HttpResponse(json_data, content_type='application/json')
        elif more_text == 'symptom':
            handler = symptom.Symptom()
            symptoms_name = handler.fuzzy_search(search_text)
            print(len(symptoms_name))
            data = []
            for symptom_name in symptoms_name[(page*page_size):min(((page+1)*page_size), len(symptoms_name))]:
                print(symptom_name)
                data.append(handler.symptom_info_brief(symptom_name))
            json_data = json.dumps({'symptom_list': data}, ensure_ascii=False)
            return HttpResponse(json_data, content_type='application/json')
        elif more_text == 'drug':
            handler = drug.Drug()
            drugs_name = handler.fuzzy_search(search_text)
            print(len(drugs_name))
            data = []
            for drug_name in drugs_name[(page*page_size):min(((page+1)*page_size), len(drugs_name))]:
                print(drug_name)
                data.append(handler.drug_info_brief(drug_name))
            json_data = json.dumps({'drug_list': data}, ensure_ascii=False)
            return HttpResponse(json_data, content_type='application/json')
    else:
        return render(request, 'wenda/404.html')


def search_more(request, search_type):
    data = dict()
    if request.method == 'POST':
        data['search_text'] = request.POST['search_text']
    else:
        data['search_text'] = ''
    data['search_type'] = search_type
    if search_type == 'disease':
        data['search_type_zh'] = '疾病'
    elif search_type == 'symptom':
        data['search_type_zh'] = '症状'
    elif search_type == 'drug':
        data['search_type_zh'] = '药物'
    else:
        return render(request, 'wenda/404.html')
    return render(request, 'wenda/search_more.html', {'data': data})


def wenda(request):
    return render(request, 'wenda/wenda.html')


def wenda_ajax(request):
    if request.is_ajax():
        handler = question_classify.QuestionClassify()
        data = request.GET['question']
        print(data)
        answer = handler.classify(data)
        a = {'answer': answer}
        jsonDate = json.dumps(a, ensure_ascii=False)
        return HttpResponse(jsonDate, content_type='application/json')
    else:
        return render(request, 'wenda/404.html')


def department_html(request, keshi):
    data = dict()
    dept_first = ['全部科室', '内科', '外科', '妇产科', '传染科', '生殖健康',
                  '男科', '皮肤性病科', '中医科', '五官科', '精神科', '心理科',
                  '儿科', '营养科', '肿瘤科', '其他科室', '急诊科', '肝病']
    if keshi in dept_first:
        data['department'] = keshi
        return render(request, 'wenda/department.html', {'data': data})
    else:
        return render(request, 'wenda/404.html')


def department_ajax(request):
    if request.is_ajax():
        department_name = request.GET['department_name']
        page = int(request.GET['page'])
        page_size = int(request.GET['page_size'])
        print(department_name, page, page_size)
        handler = department.Department()
        data = handler.fuzzy_search(department_name, page=page, page_size=page_size)
        json_data = json.dumps({'disease_list': data}, ensure_ascii=False)
        return HttpResponse(json_data, content_type='application/json')
    else:
        return render(request, 'wenda/404.html')


def population_html(request, renqun):
    renqun_list = ['全部', '男性', '女性', '老年', '儿童']
    if renqun in renqun_list:
        data = dict()
        data['population'] = renqun
        return render(request, 'wenda/people.html', {'data': data})
    else:
        return render(request, 'wenda/404.html')


def population_ajax(request):
    if request.is_ajax():
        population_name = request.GET['population_name']
        page = int(request.GET['page'])
        page_size = int(request.GET['page_size'])
        print(population_name, page, page_size)
        handler = population.Population()
        data = handler.fuzzy_search(population_name, page=page, page_size=page_size)
        json_data = json.dumps({'disease_list': data}, ensure_ascii=False)
        return HttpResponse(json_data, content_type='application/json')
    else:
        return render(request, 'wenda/404.html')


def disease_info(request, name):
    handler = disease.Disease()
    data = handler.disease_info(name)
    if data is None:
        return render(request, 'wenda/404.html')
    else:
        return render(request, 'wenda/disease.html', {'disease_info': data})


def symptom_info(request, name):
    handler = symptom.Symptom()
    data = handler.symptom_info(name)
    if data is None:
        return render(request, 'wenda/404.html')
    else:
        return render(request, 'wenda/symptom.html', {'symptom_info': data})


def drug_info(request, name):
    handler = drug.Drug()
    data = handler.drug_info(name)
    if data is None:
        return render(request, 'wenda/404.html')
    else:
        return render(request, 'wenda/drug.html', {'drug_info': data})


def login(request):
    user_role = request.COOKIES.get('user_role', '')
    username = request.COOKIES.get('username', '')
    if user_role and username:
        if user_role == 'normal':
            return redirect('wenda:user_info', username)
        else:
            return redirect('wenda:doctor_info', username)

    else:
        # 当前端点击登录按钮时，提交数据到后端，进入该POST方法
        if request.method == "POST":
            # 获取用户名和密码
            user_role = request.POST.get("user_role")
            username = request.POST.get("username")
            password = request.POST.get("password")
            # 在前端传回时也将跳转链接传回来
            next_url = request.POST.get("next_url")
            # print(next_url)
            if user_role == 'normal':
                user = User.objects.filter(user_name=username)
            else:
                user = Doctor.objects.filter(user_name=username)
            # print(user_role, user)
            if len(user) == 1:
                if password == user[0].password:
                    response = redirect('wenda:index')
                    response.set_cookie('user_role', user_role, 36000)
                    response.set_cookie('username', username, 36000)
                    return response
                else:
                    error_msg = "输入密码错误"
                    return render(request, "wenda/login.html", {
                        'login_error_msg': error_msg,
                        'next_url': next_url,
                    })
            else:
                error_msg = "用户不存在"
                return render(request, "wenda/login.html", {
                    'login_error_msg': error_msg,
                    'next_url': next_url,
                })
        # 若没有进入post方法，则说明是用户刚进入到登录页面。用户访问链接形如下面这样：
        # http://host:port/login/?next=/next_url/
        # 拿到跳转链接
        # next_url = request.GET.get("next", "")
        # print(next_url)
        next_url = ''
        # 直接将跳转链接也传递到后端
        return render(request, "wenda/login.html", {'next_url': next_url})


def logout(request):
    username = request.COOKIES.get('username', '')
    response = redirect('wenda:index')
    print('asdfasdfasdfaf')
    if username:
        response.delete_cookie('username')
    return response


def signup(request):
    # 当前端点击登录按钮时，提交数据到后端，进入该POST方法
    if request.method == "POST":
        # 获取用户名和密码
        user_role = request.POST.get("user_role")
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        # 在前端传回时也将跳转链接传回来
        next_url = request.POST.get("next_url")
        if re.match("^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$", email) == None:
            error_msg = "邮箱格式不正确"
            return render(request, "wenda/signup.html", {
                'login_error_msg': error_msg,
                'next_url': next_url,
            })
        # print(next_url)
        if user_role == 'normal':
            user = User.objects.filter(user_name=username)
            mail = User.objects.filter(mail=email)
        else:
            user = Doctor.objects.filter(user_name=username)
            mail = Doctor.objects.filter(mail=email)
        print(user_role, user)
        if len(user) == 0 and len(mail) == 0:
            if user_role == 'normal':
                User.objects.create(user_name=username, mail=email, password=password)
            else:
                Doctor.objects.create(user_name=username, mail=email, password=password)
            response = redirect('wenda:index')
            response.set_cookie('user_role', user_role, 3600)
            response.set_cookie('username', username, 3600)
            return response
        elif len(user) == 1 and len(mail) == 0:
            error_msg = "用户名已被注册"
        elif len(user) == 0 and len(mail) == 1:
            error_msg = "邮箱已被注册"
        elif len(user) == 1 and len(mail) == 1:
            error_msg = "用户名、邮箱已被注册"
        return render(request, "wenda/signup.html", {
            'login_error_msg': error_msg,
            'next_url': next_url,
        })
    next_url = ''
    return render(request, "wenda/signup.html", {'next_url': next_url})


# 手机正则phone_re = re.compile(r'^(13[0-9]|15[012356789]|17[0678]|18[0-9]|14[57])[0-9]{8}$')
def user_info(request, username):
    if username == request.COOKIES.get('username', '') and request.COOKIES.get('user_role', '') == 'normal':
        user = User.objects.get(user_name=username)
        # 个人信息
        data = dict()
        data['name'] = username
        data['mail'] = user.mail
        data['birth'] = user.birth
        data['tel'] = user.tel
        print(user.mail, user.user_name, user.birth, user.tel)
        return render(request, 'wenda/user_info.html', {'data': data})
    else:
        return render(request, 'wenda/404.html')


def user_info_ajax(request):
    if request.is_ajax():
        user_role = request.COOKIES.get('user_role', '')
        username = request.COOKIES.get('username', '')
        if user_role and username and user_role == 'normal':
            username = request.GET['username']
            user = User.objects.get(user_name=username)
            page = int(request.GET['page'])
            page_size = int(request.GET['page_size'])
            print(username, page, page_size)
            # 问题
            questions = user.question_set.all()
            data = []
            for question in questions[(page * page_size):min(((page + 1) * page_size), len(questions))]:
                question_info = dict()
                question_info['id'] = question.id
                question_info['title'] = question.title
                question_info['content'] = question.content
                question_info['date'] = question.date.strftime('%Y-%m-%d')
                question_info['num_reply'] = len(question.reply_set.all())
                print(question_info)
                data.append(question_info)
            json_data = json.dumps({'question_list': data}, ensure_ascii=False)
            return HttpResponse(json_data, content_type='application/json')
        else:
            json_data = json.dumps({'question_list': []}, ensure_ascii=False)
            return HttpResponse(json_data, content_type='application/json')
    else:
        return render(request, 'wenda/404.html')


def doctor_info(request, username):
    if request.COOKIES.get('user_role', '') == 'doctor' and \
            username == request.COOKIES.get('username', ''):
        doctor = Doctor.objects.get(user_name=username)
        # 个人信息
        data = dict()
        data['username'] = username
        data['mail'] = doctor.mail
        data['birth'] = doctor.birth
        data['tel'] = doctor.tel
        data['confirmed'] = doctor.confirmed
        data['name'] = doctor.name
        data['hospital'] = doctor.hospital
        data['department'] = doctor.department
        # print(data)
        return render(request, 'wenda/doctor_info.html', {'data': data})
    else:
        return render(request, 'wenda/404.html')


def doctor_info_ajax(request):
    if request.is_ajax():
        user_role = request.COOKIES.get('user_role', '')
        username = request.COOKIES.get('username', '')
        if user_role and username and user_role == 'doctor':
            doctor = Doctor.objects.get(user_name=username)
            page = int(request.GET['page'])
            page_size = int(request.GET['page_size'])
            print(username, page, page_size)
            # question
            replies = doctor.reply_set.all()
            data = dict()
            reply_list = []
            for reply in replies[(page * page_size):min(((page + 1) * page_size), len(replies))]:
                reply_info = dict()
                reply_info['id'] = reply.id
                reply_info['content'] = reply.content
                reply_info['date'] = reply.date.strftime('%Y-%m-%d')
                reply_info['question_id'] = reply.question.id
                reply_info['question_title'] = reply.question.title
                reply_list.append(reply_info)
            data['reply_list'] = reply_list
            json_data = json.dumps(data, ensure_ascii=False)
            return HttpResponse(json_data, content_type='application/json')
        else:
            json_data = json.dumps({'reply_list': []}, ensure_ascii=False)
            return HttpResponse(json_data, content_type='application/json')
    else:
        return render(request, 'wenda/404.html')


def wenyi(request):
    user_role = request.COOKIES.get('user_role', '')
    username = request.COOKIES.get('username', '')
    if username and user_role:
        if user_role == 'normal':
            # 当前端点击登录按钮时，提交数据到后端，进入该POST方法
            if request.method == "POST":
                # 获取用户名和密码
                title = request.POST.get("title")
                content = request.POST.get("content")
                # 在前端传回时也将跳转链接传回来
                next_url = request.POST.get("next_url")
                # print(next_url)
                user = User.objects.get(user_name=username)
                if title and content:
                    new_question = Question.objects.create(title=title, content=content, user=user)
                    response = redirect('wenda:question', new_question.id)
                    return response
                else:
                    error_msg = "问题标题或问题详情为空"
                    return render(request, "wenda/login.html", {
                        'login_error_msg': error_msg,
                        'next_url': next_url,
                    })
            next_url = ''
            # 直接将跳转链接也传递到后端
            return render(request, 'wenda/wenyi.html', {'next_url': next_url})
        else:
            return render(request, 'wenda/wenyi_reply.html')
    else:
        return render(request, 'wenda/not_login.html')


def wenyi_reply_ajax(request):
    if request.is_ajax():
        user_role = request.COOKIES.get('user_role', '')
        username = request.COOKIES.get('username', '')
        if user_role and username and user_role == 'doctor':
            page = int(request.GET['page'])
            page_size = int(request.GET['page_size'])
            print(page, page_size)
            # question
            data = dict()
            questions = Question.objects.all()
            question_list = []
            for question in questions[(page * page_size):min(((page + 1) * page_size), len(questions))]:
                question_info = dict()
                question_info['id'] = question.id
                question_info['title'] = question.title
                question_info['content'] = question.content
                question_info['date'] = question.date.strftime('%Y-%m-%d')
                question_info['num_reply'] = len(question.reply_set.all())
                print(question_info)
                question_list.append(question_info)
            data['question_list'] = question_list
            json_data = json.dumps(data, ensure_ascii=False)
            return HttpResponse(json_data, content_type='application/json')
        else:
            json_data = json.dumps({'reply_list': []}, ensure_ascii=False)
            return HttpResponse(json_data, content_type='application/json')
    else:
        return render(request, 'wenda/404.html')


def reply(request):
    user_role = request.COOKIES.get('user_role', '')
    username = request.COOKIES.get('username', '')
    if username and user_role:
        if user_role == 'normal':
            return render(request, 'wenda/wenyi.html')
        else:
            return render(request, 'wenda/wenyi_reply.html')
    else:
        return render(request, 'wenda/not_login.html')


def question(request, question_id):
    user_role = request.COOKIES.get('user_role', '')
    username = request.COOKIES.get('username', '')
    if user_role:
        questions = Question.objects.filter(id=question_id)
        if len(questions) == 1:
            data = dict()
            # 角色
            data['user_role'] = user_role
            data['username'] = username
            if user_role == 'doctor':
                doctor = Doctor.objects.get(user_name=username)
                data['confirmed'] = doctor.confirmed
            # 问题
            question_info = dict()
            question_info['id'] = questions[0].id
            question_info['title'] = questions[0].title
            question_info['content'] = questions[0].content
            question_info['date'] = questions[0].date.strftime('%Y-%m-%d')
            question_info['time'] = questions[0].time.strftime('%H:%M')
            data['question'] = question_info
            # 回复
            replies = questions[0].reply_set.all()
            reply_list = []
            for reply in replies:
                reply_info = dict()
                reply_info['content'] = reply.content
                reply_info['date'] = reply.date.strftime('%Y-%m-%d')
                reply_info['time'] = reply.time.strftime('%H:%M')
                # 医师
                reply_doctor = dict()
                reply_doctor['name'] = reply.doctor.name
                reply_doctor['hospital'] = reply.doctor.hospital
                reply_doctor['department'] = reply.doctor.department
                reply_info['doctor'] = reply_doctor
                reply_list.append(reply_info)
            data['reply_list'] = reply_list
            # print(data)
            return render(request, 'wenda/question.html', data)
        return render(request, 'wenda/404.html')
    else:
        return render(request, 'wenda/not_login.html')


def question_reply_ajax(request):
    if request.is_ajax():
        user_role = request.COOKIES.get('user_role', '')
        username = request.COOKIES.get('username', '')
        if user_role and username and user_role == 'doctor':
            content = request.GET["content"]
            question_id = request.GET["question"]
            if question and content:
                doctor = Doctor.objects.get(user_name=username)
                question_o = Question.objects.get(id=question_id)
                print(content, username, question_id)
                new_reply = Reply.objects.create(content=content, doctor=doctor, question=question_o)
                data = dict()
                if new_reply:
                    reply_info = dict()
                    reply_info['content'] = new_reply.content
                    reply_info['date'] = new_reply.date.strftime('%Y-%m-%d')
                    reply_info['time'] = new_reply.time.strftime('%H:%M')
                    # 医师
                    reply_doctor = dict()
                    reply_doctor['name'] = new_reply.doctor.name
                    reply_doctor['hospital'] = new_reply.doctor.hospital
                    reply_doctor['department'] = new_reply.doctor.department
                    data['reply'] = reply_info
                    data['doctor'] = reply_doctor
                    data['success'] = True
                else:
                    data['success'] = False
                json_data = json.dumps(data, ensure_ascii=False)
                return HttpResponse(json_data, content_type='application/json')
        else:
            json_data = json.dumps({'reply_list': []}, ensure_ascii=False)
            return HttpResponse(json_data, content_type='application/json')
    else:
        return render(request, 'wenda/404.html')


def feedback(request, feedback_type):
    feedback_type_list = ['disease', 'symptom', 'drug', 'wenda']
    if feedback_type in feedback_type_list:
        # 当前端点击登录按钮时，提交数据到后端，进入该POST方法
        if request.method == "POST":
            # 获取用户名和密码
            user_role = request.COOKIES.get('user_role', '')
            username = request.COOKIES.get('username', '')
            if user_role == 'normal':
                user_id = User.objects.get(user_name=username).id
            else:
                user_id = Doctor.objects.get(user_name=username).id
            content = request.POST.get("content")
            contact = request.POST.get("contact")
            # 在前端传回时也将跳转链接传回来
            next_url = request.POST.get("next_url")
            Feedback.objects.create(feedback_type=feedback_type, user_role=user_role, user_id=user_id, content=content, contact=contact)
            response = redirect('wenda:index')
            return response
        next_url = ''
        # 直接将跳转链接也传递到后端
        return render(request, "wenda/feedback.html", {'next_url': next_url, 'feedback_type': feedback_type})
    else:
        return render(request, 'wenda/404.html')


def renz(request):
    user_role = request.COOKIES.get('user_role', '')
    username = request.COOKIES.get('username', '')
    if username and user_role == 'doctor':
        if request.method == "POST":
            # 获取用户名和密码
            user_role = request.COOKIES.get('user_role', '')
            username = request.COOKIES.get('username', '')
            doctor = Doctor.objects.get(user_name=username)
            doctor.name = request.POST.get("name")
            doctor.certificate = request.POST.get("certificate")
            doctor.hospital_region = request.POST.get("hospital_region")
            doctor.hospital = request.POST.get("hospital")
            doctor.department = request.POST.get("department")
            doctor.confirmed = -1
            doctor.save()
            response = redirect('wenda:doctor_info', username)
            return response
        return render(request, 'wenda/renz.html')
    else:
        return render(request, 'wenda/404.html')


def alter_info(request):
    user_role = request.COOKIES.get('user_role', '')
    username = request.COOKIES.get('username', '')
    if username and user_role:
        if request.method == "POST":
            # 获取用户名和密码
            # change_username = request.POST.get("username")
            email = request.POST.get("email")
            birth = request.POST.get("birth")
            tel = request.POST.get("tel")
            # 在前端传回时也将跳转链接传回来
            next_url = request.POST.get("next_url")
            if re.match("^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$", email) == None:
                error_msg = "邮箱格式不正确"
                return render(request, "wenda/alter_info.html", {
                    'login_error_msg': error_msg,
                    'next_url': next_url,
                })
            # if re.match("r'^(13[0-9]|15[012356789]|17[0678]|18[0-9]|14[57])[0-9]{8}$'", tel) == None:
            #     error_msg = "手机格式不正确"
            #     return render(request, "wenda/alter_info.html", {
            #         'login_error_msg': error_msg,
            #         'next_url': next_url,
            #     })
            if user_role == 'normal':
                user = User.objects.get(user_name=username)
                # user.user_name = change_username
                user.mail = email
                user.birth = birth
                user.tel = tel
                user.save()
            else:
                doctor = Doctor.objects.get(user_name=username)
                # doctor.user_name = change_username
                doctor.mail = email
                doctor.birth = birth
                doctor.tel = tel
                doctor.save()
            response = redirect('wenda:login')
            return response
        data = dict()
        if user_role == 'normal':
            user = User.objects.get(user_name=username)
            data['mail'] = user.mail
            data['birth'] = user.birth.strftime('%Y-%m-%d')
            data['tel'] = user.tel
        else:
            doctor = Doctor.objects.get(user_name=username)
            data['mail'] = doctor.mail
            data['birth'] = doctor.birth.strftime('%Y-%m-%d')
            data['tel'] = doctor.tel
        return render(request, 'wenda/alter_info.html', {'data': data})
    else:
        return render(request, 'wenda/not_login.html')


def delete_question(request, question_id):
    user_role = request.COOKIES.get('user_role', '')
    username = request.COOKIES.get('username', '')
    if user_role and user_role == 'normal':
        question = Question.objects.filter(id=question_id)
        if len(question) == 1 and question[0].user.user_name == username:
            question.delete()
            response = redirect('wenda:user_info', username)
            return response
        else:
            return render(request, 'wenda/404.html')
    else:
        return render(request, 'wenda/404.html')


def delete_reply(request, reply_id):
    user_role = request.COOKIES.get('user_role', '')
    username = request.COOKIES.get('username', '')
    if user_role and user_role == 'doctor':
        reply = Reply.objects.filter(id=reply_id)
        if len(reply) == 1 and reply[0].doctor.user_name == username:
            reply.delete()
            response = redirect('wenda:doctor_info', username)
            return response
        else:
            return render(request, 'wenda/404.html')
    else:
        return render(request, 'wenda/404.html')
