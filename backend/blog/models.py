from django.db import models
import uuid
import markdown
# Create your models here.

class BlogPost(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    locale = models.CharField(max_length=8)
    title = models.CharField(max_length=128)
    slug = models.CharField(max_length=128)
    format = models.CharField(max_length=4)
    datetime = models.DateTimeField()
    content = models.TextField()

    @property
    def html(self):
        if self.format == "md":
            return markdown.markdown(self.content)
        elif self.format == "html":
            return self.content
        else:
            return "<pre>{}</pre>".format(self.content)
