from django.core.management.base import BaseCommand, CommandError
import blog
import os
from pathlib import Path
import yaml
from blog.models import BlogPost
from django.utils import dateparse
from django.utils.text import slugify
from datetime import datetime
from django.utils import timezone

class Command(BaseCommand):
    help = 'Collects all posts within the post folder'

    def handle(self, *args, **options):
        app_dir = Path(os.path.dirname(blog.__file__))
        posts_dir = app_dir / "posts"
        os.makedirs(posts_dir, exist_ok=True)

        post_files = posts_dir.glob("*/post.yaml")

        BlogPost.objects.all().delete()

        for post_path in post_files:
            post_dir = post_path.parent

            with open(post_path, 'r') as post_file:
                post_dict = yaml.load(post_file)

            #check required fields
            for field in ["title", "format", "locale", "datetime"]:
                if type(post_dict.get(field, None)) != str:
                    raise Exception("not a string {} in {}".format(field, post_path))

            parsed_datetime = dateparse.parse_datetime(post_dict['datetime'])
            if parsed_datetime is None:
                raise Exception("invalid datetime in {}".format(post_path))
            if parsed_datetime.tzinfo is None:
                raise Exception("datetimes cannot be naiive in {}".format(post_path))
            post_dict['datetime'] = parsed_datetime

            content_file_path = (post_dir / f"post.{post_dict['format']}")
            with open(content_file_path, 'r') as content_file:
                content = content_file.read()
            
            post_obj = BlogPost.objects.create_post(**post_dict, content=content)

            correct_dirname = "{}__{}".format(str(post_obj.datetime.date()), post_obj.slug)
            correct_dir = posts_dir / correct_dirname

            if not post_dir == correct_dir and correct_dir.exists():
                raise Exception("duplicate post directory {}".format(correct_dirname))
            post_dir.rename(correct_dir)