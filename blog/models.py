from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
# Create your models here.

class PublishedManager(models.Manager):
	def get_queryset(self):
		return super().get_queryset()\
			.filter(status=Post.Status.PUBLISHED)

class Post(models.Model):

	# Adding a status field : A common functionality
	# for blogs is to save posts as a draft
	# until ready for publication.
	class Status(models.TextChoices):
		DRAFT = 'DF', 'Draft'
		PUBLISHED = 'PB', 'Published'


	title = models.CharField(max_length=250)
	slug = models.SlugField(max_length=250,
							unique_for_date='publish')
	# many-to-one relationship
	author = models.ForeignKey(User,
						on_delete=models.CASCADE,
						related_name='blog_posts')
	body = models.TextField()
	publish = models.DateTimeField(default=timezone.now)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	status = models.CharField(max_length=2,
			choices=Status.choices,
			default=Status.DRAFT)
	objects = models.Manager() # The default Manager
	published = PublishedManager() # Our Custom Managers


	# Defining a default sort order (from newest to oldest)
	class Meta:
		# We indicate descending order by using a
		# hyphen before the field name, -publish.
		ordering = ['-publish']
		indexes = [
			models.Index(fields=['-publish']),
		]

	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse('blog:post_detail',
						args=[self.publish.year,
						      self.publish.month,
						      self.publish.day,
						      self.slug])

