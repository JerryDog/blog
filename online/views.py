#coding:utf8
from django.shortcuts import render,render_to_response
from django.http import HttpResponse,HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from django.contrib.auth.models import User
from django import forms
from models import Blogs
from models import Comments, IndexViews, PhotoViews
import os
from django.views.decorators.csrf import csrf_exempt
import datetime
import re
#表单
class UserForm(forms.Form): 
    username = forms.CharField(label='用户名',max_length=100)
    password = forms.CharField(label='密码',widget=forms.PasswordInput())
    password1 = forms.CharField(label='密码',widget=forms.PasswordInput())


#注册
def regist(req):
    if req.method == 'POST':
        uf = UserForm(req.POST)
        if uf.is_valid():
            #获得表单数据
            username = uf.cleaned_data['username']
            password = uf.cleaned_data['password']
	    password1 = uf.cleaned_data['password1']
            #添加到数据库
            #User.objects.create(username= username,password=password)
	    if User.objects.filter(username=username):
		 exist = '用户已存在'
		 return render_to_response('regist.html',{'exist':exist}, context_instance=RequestContext(req))
            if password != password1:
		 passwrong = '两次输入的密码不一致'
                 return render_to_response('regist.html',{'pass':passwrong}, context_instance=RequestContext(req))
            if not User.objects.filter(username=username) and password == password1:
		 User.objects.create_user(username,'test@test.com',password)
                 return HttpResponse('<h1>注册成功!!</h1>')
    else:
        uf = UserForm()
    return render_to_response('regist.html',{'uf':uf}, context_instance=RequestContext(req))

#登陆
def login(req):
    exist = 0
    if re.search('photo',req.get_full_path()):
	exist = 1
    if req.method == 'POST':
	username = req.POST.get('username', '')
    	password = req.POST.get('password', '')
	user = auth.authenticate(username=username, password=password)
        if user is not None:
 	    if exist == 1:
	    	auth.login(req, user)
		response = HttpResponseRedirect('/online/photo/')
	    else:
	    	auth.login(req, user)
            	response = HttpResponseRedirect('/online/index/')
            #将username写入浏览器cookie,失效时间为3600
            response.set_cookie('username',username,120)
            return response
        else:
            #比较失败，还在login
            error = '用户名密码错误'
            return render_to_response('login.html',{'error':error},context_instance=RequestContext(req))
    #else:
       # uf = UserForm()
    return render_to_response('login.html',context_instance=RequestContext(req))

#登陆成功
#@login_required
def index(req):
    linux_count = len(Blogs.objects.filter(item='linux'))
    django_count = len(Blogs.objects.filter(item='django'))
    aws_count = len(Blogs.objects.filter(item='aws'))
    python_count = len(Blogs.objects.filter(item='python'))
    others_count = len(Blogs.objects.filter(item='others'))
    username = req.COOKIES.get('username','')
    view_date = datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S')

    if req.META.has_key('HTTP_X_FORWARDED_FOR'):  
    	view_ip =  req.META['HTTP_X_FORWARDED_FOR']  
    else:  
    	view_ip = req.META['REMOTE_ADDR']

    view_sum = int(IndexViews.objects.latest('id').view_sum) + 1
    add = IndexViews(view_date=view_date,view_ip=view_ip,view_sum=view_sum)
    add.save()

    if username:
    	logout = '注销'
	loginTag = ''
	registTag = ''
    else: 
	logout = ''
        loginTag = '登陆'
        registTag = '注册'
    viewsum = int(int(IndexViews.objects.latest('id').view_sum)-1)
    return render_to_response('index.html' , locals())

#退出
def logout(req):
    auth.logout(req)
    response = HttpResponse('logout !!')
    #清理cookie里保存username
    response.delete_cookie('username')
    return response

def blog(req):
    linux_count = len(Blogs.objects.filter(item='linux'))
    django_count = len(Blogs.objects.filter(item='django'))
    aws_count = len(Blogs.objects.filter(item='aws'))
    python_count = len(Blogs.objects.filter(item='python'))
    others_count = len(Blogs.objects.filter(item='others'))
    username = req.COOKIES.get('username','')
    if username:
        logout = '注销'
        loginTag = ''
        registTag = ''
	blogs_list= Blogs.objects.order_by('id').reverse()                           
        return render_to_response('blogmeau.html', locals(), context_instance=RequestContext(req))
    else:
        logout = ''
        loginTag = '登陆'
        registTag = '注册'
	blogs_list= Blogs.objects.order_by('id').reverse()
        return render_to_response('blogmeau.html', locals(), context_instance=RequestContext(req))


def singleblog(req,blogid=''):
	linux_count = len(Blogs.objects.filter(item='linux'))
    	django_count = len(Blogs.objects.filter(item='django'))
   	aws_count = len(Blogs.objects.filter(item='aws'))
    	python_count = len(Blogs.objects.filter(item='python'))
        others_count = len(Blogs.objects.filter(item='others'))
	username = req.COOKIES.get('username','')
    	if username:
        	logout = '注销'
        	loginTag = ''
        	registTag = ''
   	else:
        	logout = ''
        	loginTag = '登陆'
        	registTag = '注册'
	single_blog = Blogs.objects.get(id=blogid)
	single_blog_comments = Comments.objects.filter(blogid=blogid).order_by('id')
	previous_id = int(blogid)
	while 1:
		previous_id = previous_id - 1
		try:
			previous_title = Blogs.objects.get(id=previous_id).title 
			previous_blog = '<a href="/online/singleblog/%s">%s</a>' % (previous_id, previous_title)
			break
		except Exception,e:
			if previous_id > 0:
				continue
			else:
				previous_title = ''
				previous_blog = '没有了'
				break

	next_id = int(blogid)
	while 1:
		next_id = next_id + 1
		try:
			next_title = Blogs.objects.get(id=next_id).title
                	next_blog = '<a href="/online/singleblog/%s">%s</a>' % (next_id, next_title)
			break
		except Exception,e:
			if next_id < int(Blogs.objects.latest('id').id):
				continue
			else:
				next_title = ''
                		next_blog = '没有了'
				break
	return render_to_response('blogsingle.html', locals())

@csrf_exempt
def comments(req):
	name = req.REQUEST.get('name')
	content = req.REQUEST.get('content')
	blogid = req.REQUEST.get('blogid')
	if content == '':
		return render_to_response('returnBlog.html',{'blogid': blogid}, context_instance=RequestContext(req)) 		
	else:
		blogtitle = Blogs.objects.get(id=blogid).title
		pub_date = datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S')
		if req.META.has_key('HTTP_X_FORWARDED_FOR'):  
    			ipaddress =  req.META['HTTP_X_FORWARDED_FOR']  
		else:  
    			ipaddress = req.META['REMOTE_ADDR'] 
		add = Comments(blogid=blogid,blogtitle=blogtitle,pub_date=pub_date,username=name,ipaddress=ipaddress,content=content)
		add.save()
		return render_to_response('returnBlog.html',{'blogid': blogid}, context_instance=RequestContext(req)) 		


#@login_required
def photo(req):
	username = req.COOKIES.get('username','')
    	if username:
		linux_count = len(Blogs.objects.filter(item='linux'))
    		django_count = len(Blogs.objects.filter(item='django'))
    		aws_count = len(Blogs.objects.filter(item='aws'))
    		python_count = len(Blogs.objects.filter(item='python'))
		others_count = len(Blogs.objects.filter(item='others'))
        	logout = '注销'
        	loginTag = ''
        	registTag = ''
		a = os.popen("find /var/www/blog/online/static/images/photos -type f")
		photos_list = []
		for i in a.readlines():
                	b = i.split('/')
                	photos_list.append(''.join(b[-1:]).replace('\n',''))

    		view_date = datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S')

    		if req.META.has_key('HTTP_X_FORWARDED_FOR'):  
    			view_ip =  req.META['HTTP_X_FORWARDED_FOR']  
    		else:  
    			view_ip = req.META['REMOTE_ADDR']

    		view_sum = int(PhotoViews.objects.latest('id').view_sum) + 1
    		add = PhotoViews(view_date=view_date,view_ip=view_ip,view_sum=view_sum,view_user=username)
    		add.save()
		viewsum = int(int(PhotoViews.objects.latest('id').view_sum)-1)

		return render_to_response('photomeau.html', locals(), context_instance=RequestContext(req))
    	else:
		return render_to_response('needlogin.html')

def linux(req):
	linux_count = len(Blogs.objects.filter(item='linux'))
    	django_count = len(Blogs.objects.filter(item='django'))
    	aws_count = len(Blogs.objects.filter(item='aws'))
    	python_count = len(Blogs.objects.filter(item='python'))
    	others_count = len(Blogs.objects.filter(item='others'))
    	username = req.COOKIES.get('username','')
	blogs_list= Blogs.objects.filter(item='linux').order_by('-id')
    	if username:
        	logout = '注销'
        	loginTag = ''
        	registTag = ''
    	else:
        	logout = ''
        	loginTag = '登陆'
        	registTag = '注册'
        return render_to_response('linuxmeau.html', locals(), context_instance=RequestContext(req))

def singlelinux(req,blogid=''):
	linux_count = len(Blogs.objects.filter(item='linux'))
    	django_count = len(Blogs.objects.filter(item='django'))
   	aws_count = len(Blogs.objects.filter(item='aws'))
    	python_count = len(Blogs.objects.filter(item='python'))
        others_count = len(Blogs.objects.filter(item='others'))
	username = req.COOKIES.get('username','')
    	if username:
        	logout = '注销'
        	loginTag = ''
        	registTag = ''
   	else:
        	logout = ''
        	loginTag = '登陆'
        	registTag = '注册'
	single_blog = Blogs.objects.get(id=blogid)
	single_blog_comments = Comments.objects.filter(blogid=blogid).order_by('id')

	blogs_list= Blogs.objects.filter(item='linux').reverse()
	id_list = []
	
	for i in blogs_list:
		id_list.append(str(i.id))
	print id_list
	current_id_index = id_list.index(blogid) 
	
	
	previous_id_index = current_id_index -1
	next_id_index = current_id_index + 1

	if previous_id_index in range(len(id_list)):
		previous_id = id_list[previous_id_index]
		previous_title = Blogs.objects.get(id=previous_id).title
		previous_blog = '<a href="/online/linux/%s">%s</a>' % (previous_id, previous_title)
	else:
		previous_title = ''
		previous_blog = '没有了'

	if next_id_index in range(len(id_list)):
		next_id = id_list[next_id_index]
		next_title = Blogs.objects.get(id=next_id).title
		next_blog = '<a href="/online/linux/%s">%s</a>' % (next_id, next_title)
	else:
		next_title = ''
		next_blog = '没有了'
	return render_to_response('blogsingle.html', locals())


def python(req):
	linux_count = len(Blogs.objects.filter(item='linux'))
    	django_count = len(Blogs.objects.filter(item='django'))
    	aws_count = len(Blogs.objects.filter(item='aws'))
    	python_count = len(Blogs.objects.filter(item='python'))
    	others_count = len(Blogs.objects.filter(item='others'))
    	username = req.COOKIES.get('username','')
	blogs_list= Blogs.objects.filter(item='python').order_by('-id')
    	if username:
        	logout = '注销'
        	loginTag = ''
        	registTag = ''
    	else:
        	logout = ''
        	loginTag = '登陆'
        	registTag = '注册'
        return render_to_response('pythonmeau.html', locals(), context_instance=RequestContext(req))

def singlepython(req,blogid=''):
	linux_count = len(Blogs.objects.filter(item='linux'))
    	django_count = len(Blogs.objects.filter(item='django'))
   	aws_count = len(Blogs.objects.filter(item='aws'))
    	python_count = len(Blogs.objects.filter(item='python'))
        others_count = len(Blogs.objects.filter(item='others'))
	username = req.COOKIES.get('username','')
    	if username:
        	logout = '注销'
        	loginTag = ''
        	registTag = ''
   	else:
        	logout = ''
        	loginTag = '登陆'
        	registTag = '注册'
	single_blog = Blogs.objects.get(id=blogid)
	single_blog_comments = Comments.objects.filter(blogid=blogid).order_by('id')

	blogs_list= Blogs.objects.filter(item='python').reverse()
	id_list = []
	
	for i in blogs_list:
		id_list.append(str(i.id))
	print id_list
	current_id_index = id_list.index(blogid) 
	
	
	previous_id_index = current_id_index -1
	next_id_index = current_id_index + 1

	if previous_id_index in range(len(id_list)):
		previous_id = id_list[previous_id_index]
		previous_title = Blogs.objects.get(id=previous_id).title
		previous_blog = '<a href="/online/python/%s">%s</a>' % (previous_id, previous_title)
	else:
		previous_title = ''
		previous_blog = '没有了'

	if next_id_index in range(len(id_list)):
		next_id = id_list[next_id_index]
		next_title = Blogs.objects.get(id=next_id).title
		next_blog = '<a href="/online/python/%s">%s</a>' % (next_id, next_title)
	else:
		next_title = ''
		next_blog = '没有了'
	return render_to_response('blogsingle.html', locals())


def django(req):
	linux_count = len(Blogs.objects.filter(item='linux'))
    	django_count = len(Blogs.objects.filter(item='django'))
    	aws_count = len(Blogs.objects.filter(item='aws'))
    	python_count = len(Blogs.objects.filter(item='python'))
    	others_count = len(Blogs.objects.filter(item='others'))
    	username = req.COOKIES.get('username','')
	blogs_list= Blogs.objects.filter(item='django').order_by('-id')
    	if username:
        	logout = '注销'
        	loginTag = ''
        	registTag = ''
    	else:
        	logout = ''
        	loginTag = '登陆'
        	registTag = '注册'
        return render_to_response('djangomeau.html', locals(), context_instance=RequestContext(req))

def singledjango(req,blogid=''):
	linux_count = len(Blogs.objects.filter(item='linux'))
    	django_count = len(Blogs.objects.filter(item='django'))
   	aws_count = len(Blogs.objects.filter(item='aws'))
    	python_count = len(Blogs.objects.filter(item='python'))
        others_count = len(Blogs.objects.filter(item='others'))
	username = req.COOKIES.get('username','')
    	if username:
        	logout = '注销'
        	loginTag = ''
        	registTag = ''
   	else:
        	logout = ''
        	loginTag = '登陆'
        	registTag = '注册'
	single_blog = Blogs.objects.get(id=blogid)
	single_blog_comments = Comments.objects.filter(blogid=blogid).order_by('id')

	blogs_list= Blogs.objects.filter(item='django').reverse()
	id_list = []
	
	for i in blogs_list:
		id_list.append(str(i.id))
	current_id_index = id_list.index(blogid) 
	
	
	previous_id_index = current_id_index -1
	next_id_index = current_id_index + 1

	if previous_id_index in range(len(id_list)):
		previous_id = id_list[previous_id_index]
		previous_title = Blogs.objects.get(id=previous_id).title
		previous_blog = '<a href="/online/django/%s">%s</a>' % (previous_id, previous_title)
	else:
		previous_title = ''
		previous_blog = '没有了'

	if next_id_index in range(len(id_list)):
		next_id = id_list[next_id_index]
		next_title = Blogs.objects.get(id=next_id).title
		next_blog = '<a href="/online/django/%s">%s</a>' % (next_id, next_title)
	else:
		next_title = ''
		next_blog = '没有了'
	return render_to_response('blogsingle.html', locals())

def aws(req):
	linux_count = len(Blogs.objects.filter(item='linux'))
    	django_count = len(Blogs.objects.filter(item='django'))
    	aws_count = len(Blogs.objects.filter(item='aws'))
    	python_count = len(Blogs.objects.filter(item='python'))
    	others_count = len(Blogs.objects.filter(item='others'))
    	username = req.COOKIES.get('username','')
	blogs_list= Blogs.objects.filter(item='aws').order_by('-id')
    	if username:
        	logout = '注销'
        	loginTag = ''
        	registTag = ''
    	else:
        	logout = ''
        	loginTag = '登陆'
        	registTag = '注册'
        return render_to_response('awsmeau.html', locals(), context_instance=RequestContext(req))

def singleaws(req,blogid=''):
	linux_count = len(Blogs.objects.filter(item='linux'))
    	django_count = len(Blogs.objects.filter(item='django'))
   	aws_count = len(Blogs.objects.filter(item='aws'))
    	python_count = len(Blogs.objects.filter(item='python'))
        others_count = len(Blogs.objects.filter(item='others'))
	username = req.COOKIES.get('username','')
    	if username:
        	logout = '注销'
        	loginTag = ''
        	registTag = ''
   	else:
        	logout = ''
        	loginTag = '登陆'
        	registTag = '注册'
	single_blog = Blogs.objects.get(id=blogid)
	single_blog_comments = Comments.objects.filter(blogid=blogid).order_by('id')

	blogs_list= Blogs.objects.filter(item='aws').reverse()
	id_list = []
	
	for i in blogs_list:
		id_list.append(str(i.id))
	current_id_index = id_list.index(blogid) 
	
	
	previous_id_index = current_id_index -1
	next_id_index = current_id_index + 1

	if previous_id_index in range(len(id_list)):
		previous_id = id_list[previous_id_index]
		previous_title = Blogs.objects.get(id=previous_id).title
		previous_blog = '<a href="/online/aws/%s">%s</a>' % (previous_id, previous_title)
	else:
		previous_title = ''
		previous_blog = '没有了'

	if next_id_index in range(len(id_list)):
		next_id = id_list[next_id_index]
		next_title = Blogs.objects.get(id=next_id).title
		next_blog = '<a href="/online/aws/%s">%s</a>' % (next_id, next_title)
	else:
		next_title = ''
		next_blog = '没有了'
	return render_to_response('blogsingle.html', locals())

def others(req):
	linux_count = len(Blogs.objects.filter(item='linux'))
    	django_count = len(Blogs.objects.filter(item='django'))
    	aws_count = len(Blogs.objects.filter(item='aws'))
    	python_count = len(Blogs.objects.filter(item='python'))
    	others_count = len(Blogs.objects.filter(item='others'))
    	username = req.COOKIES.get('username','')
	blogs_list= Blogs.objects.filter(item='others').order_by('-id')
    	if username:
        	logout = '注销'
        	loginTag = ''
        	registTag = ''
    	else:
        	logout = ''
        	loginTag = '登陆'
        	registTag = '注册'
        return render_to_response('othersmeau.html', locals(), context_instance=RequestContext(req))

def singleothers(req,blogid=''):
	linux_count = len(Blogs.objects.filter(item='linux'))
    	django_count = len(Blogs.objects.filter(item='django'))
   	aws_count = len(Blogs.objects.filter(item='aws'))
    	python_count = len(Blogs.objects.filter(item='python'))
        others_count = len(Blogs.objects.filter(item='others'))
	username = req.COOKIES.get('username','')
    	if username:
        	logout = '注销'
        	loginTag = ''
        	registTag = ''
   	else:
        	logout = ''
        	loginTag = '登陆'
        	registTag = '注册'
	single_blog = Blogs.objects.get(id=blogid)
	single_blog_comments = Comments.objects.filter(blogid=blogid).order_by('id')

	blogs_list= Blogs.objects.filter(item='others').reverse()
	id_list = []
	
	for i in blogs_list:
		id_list.append(str(i.id))
	current_id_index = id_list.index(blogid) 
	
	
	previous_id_index = current_id_index -1
	next_id_index = current_id_index + 1

	if previous_id_index in range(len(id_list)):
		previous_id = id_list[previous_id_index]
		previous_title = Blogs.objects.get(id=previous_id).title
		previous_blog = '<a href="/online/others/%s">%s</a>' % (previous_id, previous_title)
	else:
		previous_title = ''
		previous_blog = '没有了'

	if next_id_index in range(len(id_list)):
		next_id = id_list[next_id_index]
		next_title = Blogs.objects.get(id=next_id).title
		next_blog = '<a href="/online/others/%s">%s</a>' % (next_id, next_title)
	else:
		next_title = ''
		next_blog = '没有了'
	return render_to_response('blogsingle.html', locals())
