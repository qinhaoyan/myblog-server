from django.db import models

# Create your models here.
class Article(models.Model):
	title = models.CharField(max_length = 200)
	time = models.CharField(max_length = 200)
	article_type = models.CharField(max_length = 200)
	article_subtype = models.CharField(max_length = 200)
	abstract = models.CharField(max_length = 500)
	read = models.IntegerField()
	comment = models.IntegerField()
	like = models.IntegerField()
	collect = models.IntegerField()
	content = models.TextField()
	user_like = models.TextField()
	user_collect = models.TextField()

class Comment(models.Model):
	article_id = models.CharField(max_length = 200)
	like = models.IntegerField()
	name = models.CharField(max_length = 200)
	time = models.CharField(max_length = 200)
	headUrl = models.CharField(max_length = 200)
	content = models.TextField()
	user_like = models.TextField()

# class Like(models.Model):
# 	article_id = models.CharField(max_length = 200)
# 	user_id = models.CharField(max_length = 200)

# class Collect(models.Model):
# 	article_id = models.CharField(max_length = 200)
# 	user_id = models.CharField(max_length = 200)

class Message(models.Model):
	message_id = models.CharField(max_length = 1)
	slogan = models.CharField(max_length = 200)
	banner_url = models.CharField(max_length = 1000)
	other_url = models.CharField(max_length = 1000)

