from django.db import models
import uuid
import markdown
import re
from django.utils.text import slugify
# Create your models here.

class BlogPostManager(models.Manager):
    def create_post(self, **kwargs):
        tags = kwargs.pop('tags', [])
        
        if "slug" not in kwargs:
            kwargs["slug"] = slugify(kwargs['title'], allow_unicode=True)

        post = self.create(**kwargs)

        for tag in tags:
            if not re.match("^[A-Za-z0-9-]$", str(tag)):
                raise Exception("tag invalid format")
            BlogTag.objects.create(post=post, name=tag)
        return post

class BlogPost(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    locale = models.CharField(max_length=8)
    title = models.CharField(max_length=128)
    slug = models.CharField(max_length=128)
    format = models.CharField(max_length=4)
    datetime = models.DateTimeField()
    content = models.TextField()

    objects = BlogPostManager()

    @property
    def html(self):
        if self.format == "md":
            return markdown.markdown(self.content)
        elif self.format == "html":
            return self.content
        else:
            return "<pre>{}</pre>".format(self.content)

    @property
    def iso_date(self):
        return str(self.datetime.date())

    @property
    def tag_list(self):
        return [tag.name for tag in self.tags.all().order_by('name')]

class BlogTag(models.Model):
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE, related_name='tags')
    name = models.CharField(max_length=64)

    class Meta:
        unique_together = ('post', 'name')