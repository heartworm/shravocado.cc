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
import shutil
from django.conf import settings

class Command(BaseCommand):
    help = 'Collects all posts within the post folder'

    def handle(self, *args, **options):
        # app_dir is the base directory of the app. 
        # This finds or creates a subdirectory called "posts"
        app_dir = Path(os.path.dirname(blog.__file__))
        posts_dir = app_dir / "posts"
        posts_dir.mkdir(exist_ok=True)

        # Find all YAML files under a subdirectory, these mark valid posts
        post_files = posts_dir.glob("*/post.yaml")
        # The only source of truth for posts are the files, the DB is just a cache 
        # Clear it
        BlogPost.objects.all().delete()
        # Static files are stored in the same directory for convenience, but served using a
        # proper web server during production, so they have their own directory. 
        # It will be cleared out prior to being populated. 
        static_srv_dir = Path(settings.BLOG_STATIC_DIR)
        if not static_srv_dir.parent.is_dir():
            raise Exception("{} is not a directory".format(static_srv_dir.parent))
        shutil.rmtree(static_srv_dir)
        static_srv_dir.mkdir()

        # For all found files
        for post_path in post_files:
            # Since we only know about the .yaml file, the parent is the post directory
            post_dir = post_path.parent
            # Parse the YAML file
            with open(post_path, 'r') as post_file:
                post_dict = yaml.load(post_file)

            # Check the presence of required string fields
            for field in ["title", "format", "locale", "datetime"]:
                if type(post_dict.get(field, None)) != str:
                    raise Exception("not a string {} in {}".format(field, post_path))

            # Check that the datetime specified is valid, and specifies a timezone. 
            # Since this script can be run from anywhere, using local time will result in varying
            # dates for the one post. 
            parsed_datetime = dateparse.parse_datetime(post_dict['datetime'])
            if parsed_datetime is None:
                raise Exception("invalid datetime in {}".format(post_path))
            if parsed_datetime.tzinfo is None:
                raise Exception("datetimes cannot be naiive in {}".format(post_path))
            post_dict['datetime'] = parsed_datetime

            # Read the content file. Its filename is post, with a file extension that equals
            # the value of the format field. ({'format': 'md'}) >> "post.md"
            content_file_path = (post_dir / f"post.{post_dict['format']}")
            with open(content_file_path, 'r') as content_file:
                content = content_file.read()
            
            # The object is created within the database. 
            post_obj = BlogPost.objects.create_post(**post_dict, content=content)

            # For convenience the folder names are changed to resemble the blog URLs
            # The ISO format date is first to allow for alphabetization
            # There is no nesting because it's a chore
            correct_dirname = "{}__{}".format(str(post_obj.datetime.date()), post_obj.slug)
            correct_dir = posts_dir / correct_dirname
            if not post_dir == correct_dir:
                if correct_dir.exists():
                    raise Exception("duplicate post directory {}".format(correct_dirname))
                post_dir.rename(correct_dir)

            # The static files within the "static" folder are moved to 
            # static_dst_dir with a subdirectory equal to the post's generated UUID
            # There is a redirect from (post_url)/static/(filename), to this directory
            # So that the content-file can reference ./static/(filename) and is
            # not tightly coupled with this scheme
            static_dir = post_dir / "static"
            static_dst_dir = static_srv_dir / str(post_obj.id)
            if static_dir.is_dir():
                shutil.copytree(static_dir, static_dst_dir)
