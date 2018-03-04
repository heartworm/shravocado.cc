from django.core.management.base import BaseCommand, CommandError
import blog
import os
from pathlib import Path
import yaml
from blog.models import BlogPost
from django.utils import dateparse

class Command(BaseCommand):
    help = 'Collects all posts within the post folder'

    def handle(self, *args, **options):
        app_dir = Path(os.path.dirname(blog.__file__))
        posts_dir = app_dir / "posts"
        os.makedirs(posts_dir, exist_ok=True)

        post_files = posts_dir.glob("*/post.yaml")

        BlogPost.objects.all().delete()

        for post_path in post_files:
            with open(post_path, 'r') as post_file:
                post_dict = yaml.load(post_file)

            post_dict['datetime'] = dateparse.parse_datetime(post_dict['datetime'])
            post_obj = BlogPost.objects.create(**post_dict)

            current_dir = Path(os.path.dirname(post_path))
            correct_dirname = "{}__{}".format(str(post_obj.datetime.date()), post_obj.slug)
            correct_dir = posts_dir / correct_dirname

            if correct_dir.exists() and not current_dir == correct_dir:
                raise Exception("duplicate post directory {}".format(correct_dirname))
            os.rename(current_dir, correct_dir)
