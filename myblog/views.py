from django.shortcuts import render
from django.http import HttpResponse
from myblog.models import Article,Comment,Message
import json
import pdb
import time

# Create your views here.

def timeFormat(timeStamp):
	timeArray = time.localtime(int(timeStamp))
	otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
	return otherStyleTime

def index(request):
	return render(request, 'index.html')

def getHomeMessage(request):
	res = Message.objects.filter(message_id = 1)
	data = {
		'success': True,
		'message': '',
		'status': 4,
		'data':{
			'slogan': res[0].slogan,
			'bannerurl': res[0].banner_url
		}
		
	}
	return HttpResponse(json.dumps(data),content_type="application/json")

def getTechnologyMessage(request):
	res = Message.objects.filter(message_id = 2)
	data = {
		'success': True,
		'message': '',
		'status': 4,
		'data':{
			'slogan': res[0].slogan,
			'bannerurl': res[0].banner_url
		}
		
	}
	return HttpResponse(json.dumps(data),content_type="application/json")

def getAboutMessage(request):
	res = Message.objects.filter(message_id = 3)
	pic = res[0].other_url.split(',')
	data = {
		'success': True,
		'message': '',
		'status': 4,
		'data':{
			'slogan': res[0].slogan,
			'bannerurl': res[0].banner_url,
			'pic1url': pic[0],
			'pic2url': pic[1],
			'pic3url': pic[2],
		}
		
	}
	return HttpResponse(json.dumps(data),content_type="application/json")

def getArticle(request):
	articleType = request.GET['type']
	ip = request.META['REMOTE_ADDR']
	lists = []
	try:
		subtype = request.GET['subtype']

		res = Article.objects.filter(article_subtype = subtype).order_by('-time')
		if(len(res) == 0):
			data = {
				'success':False,
				'message':'未找到相关文章',
				'status': 4,
				'data': {}
			}
			return HttpResponse(json.dumps(data),content_type="application/json")
	except Exception as e:
		if(articleType == 'all'):
			res = Article.objects.filter().order_by('-time')
		else: 
			res = Article.objects.filter(article_type = articleType).order_by('-time')
	for re in res:
		like_ip = re.user_like.split(',')
		like = 1 if (ip in like_ip) else 0 
		collect_ip = re.user_collect.split(',')
		collect = 1 if (ip in collect_ip) else 0
		if(re.article_type == 'technology'):
			article_type = "技术小栈"
		else:
			article_type = "其他"
		lists.append({
			'id': re.id,
			'title': re.title,
			'time': timeFormat(re.time),
			'type': article_type,
			'abstract': re.abstract,
			'subtype':re.article_subtype,
			'read': re.read,
			'comment': re.comment,
			'like': re.like,
			'isLike': like,
			'isCollect': collect
		})
	data = {
		'success': True,
		'message': '',
		'status': 4,
		'data': {
			'list': lists
		}
	}
	return HttpResponse(json.dumps(data),content_type="application/json")
		
def like(request):
	article_id = json.loads(request.body.decode('utf-8'))['id']
	like_type = json.loads(request.body.decode('utf-8'))['type']
	ip = request.META['REMOTE_ADDR']
	count = 0
	if(like_type == 1):
		res = Article.objects.get(id = article_id)
		res.user_like += (','+ip)
		res.like += 1
		count = res.like
		res.save()
	else:
		res = Article.objects.get(id = article_id)
		likes = res.user_like.split(',')
		likes.remove(ip)
		res.user_like = ','.join(likes)
		res.like -= 1
		count = res.like
		res.save()
	data = {
		'success': True,
		'message': '',
		'status': 4,
		'data': {
			'likeCount': count
		}
	}
	return HttpResponse(json.dumps(data),content_type="application/json")

def collect(request):
	article_id = json.loads(request.body.decode('utf-8'))['id']
	collect_type = json.loads(request.body.decode('utf-8'))['type']
	ip = request.META['REMOTE_ADDR']
	count = 0
	if(collect_type == 1):
		res = Article.objects.get(id = article_id)
		res.user_collect += (','+ip)
		res.collect += 1
		count = res.collect
		res.save()
	else:
		res = Article.objects.get(id = article_id)
		collects = res.user_collect.split(',')
		collects.remove(ip)
		res.user_collect = ','.join(collects)
		res.collect -= 1
		count = res.collect
		res.save()
	data = {
		'success': True,
		'message': '',
		'status': 4,
		'data': {
			'collectCount': count
		}
	}
	return HttpResponse(json.dumps(data),content_type="application/json")

def getClassify(request):
	res = Article.objects.filter(article_type = 'technology')
	classify = []
	classify_count = []
	for re in res:
		if(re.article_subtype in classify):
			classify_count[classify.index(re.article_subtype)] += 1
		else:
			classify.append(re.article_subtype)
			classify_count.append(1)
	lists = []
	for i,val in enumerate(classify):
		lists.append({
			'type': val,
			'count': classify_count[i]
		})
	data = {
		'success': True,
		'message': '',
		'status': 4,
		'data': {'list': lists}
	}
	return HttpResponse(json.dumps(data),content_type="application/json")


def getArticleDetail(request):
	article_id = request.GET['id']
	ip = request.META['REMOTE_ADDR']
	try:
		res = Article.objects.get(id = article_id)
		like_ip = res.user_like.split(',')
		like = 1 if (ip in like_ip) else 0
		collect_ip = res.user_collect.split(',')
		collect = 1 if (ip in collect_ip) else 0
		res.read += 1
		data = {
			'success': True,
			'message': '',
			'status': 4,
			'data': {
				'id': res.id,
				'title': res.title,
				'type':res.article_type,
				'subtype':res.article_subtype,
				'time': timeFormat(res.time),
				'content':res.content,
				'func': {
					'read': res.read,
					'comment': res.comment,
					'like': res.like,
					'isCollect': like,
					'isLike': collect,
					'id': res.id
				}
			}
		}
		res.save()
	except Exception as e:
		data={
			'success': False,
			'message': '未找到相关文章',
			'status': 4,
			'data':{}
		}
	return HttpResponse(json.dumps(data),content_type="application/json")

def commentLike(request):
	#pdb.set_trace()
	comment_id = json.loads(request.body.decode('utf-8'))['id']
	like_type = json.loads(request.body.decode('utf-8'))['type']
	ip = request.META['REMOTE_ADDR']
	count = 0
	if(like_type == 1):
		res = Comment.objects.get(id = comment_id)
		res.user_like += (','+ip)
		res.like += 1
		count = res.like
		res.save()
	else:
		res = Comment.objects.get(id = comment_id)
		likes = res.user_like.split(',')
		likes.remove(ip)
		res.user_like = ','.join(likes)
		res.like -= 1
		count = res.like
		res.save()
	data = {
		'success': True,
		'message': '',
		'status': 4,
		'data': {
			'likeCount': count
		}
	}
	return HttpResponse(json.dumps(data),content_type="application/json")


def getComment(request):
	article_id = request.GET['id']
	ip = request.META['REMOTE_ADDR']
	res = Comment.objects.filter(article_id = article_id).order_by('-time')
	lists = []
	for re in res:
		like_ip = re.user_like.split(',')
		like = 1 if (ip in like_ip) else 0
		lists.append({
			'articleId': re.article_id,
			'id': re.id,
			'isLike':like,
			'headUrl': re.headUrl,
			'name': re.name,
			'time': timeFormat(re.time),
			'liken': re.like,
			'text': re.content
		})
	data = {
		'success': True,
		'message': '',
		'status': 4,
		'data': {
			'list': lists
		}
	}
	return HttpResponse(json.dumps(data),content_type="application/json")

def comment(request):
	article_id = json.loads(request.body.decode('utf-8'))['id']
	ip = request.META['REMOTE_ADDR']
	value = json.loads(request.body.decode('utf-8'))['comment']
	try:
		res = Comment.objects.create(
								article_id = article_id,
								like = 0,
								content =  value,
								time = int(time.time()),
								name = "游客",
								user_like = '',
								headUrl = ''
							  )
		data = {
			'success': True,
			'message': '',
			'status': 4,
			'data': {}
		}
		return HttpResponse(json.dumps(data),content_type="application/json")
	except Exception as e:
		data = {
			'success': False,
			'message': '评论失败了',
			'status': 4,
			'data': {}
		}
		return HttpResponse(json.dumps(data),content_type="application/json")
		raise e

def publish(request):
	title = json.loads(request.body.decode('utf-8'))['title']
	abstract = json.loads(request.body.decode('utf-8'))['abstract']
	article_subtype = json.loads(request.body.decode('utf-8'))['type']
	text = json.loads(request.body.decode('utf-8'))['text']
	nowtime = int(time.time())
	# title = request.POST['title']
	# abstract = request.POST['abstract']
	# article_subtype = request.POST['type']
	# text = request.POST['text']
	# nowtime = int(time.time())
	Article.objects.create(title = title,
		                   time = nowtime,
		                   article_type = "technology",
		                   article_subtype = article_subtype,
		                   abstract = abstract,
		                   read = 0,
		                   comment = 0,
		                   like = 0,
		                   collect = 0,
		                   content = text)
	data = {
			'success': True,
			'message': '',
			'status': 4,
			'data': {}
	}
	return HttpResponse(json.dumps(data),content_type="application/json")