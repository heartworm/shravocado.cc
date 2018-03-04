from django.shortcuts import render
from django.views.generic.base import TemplateView
from .models import BlogPost
from django.http import Http404

class LanguageMixin:
    @property
    def locale(self):
        return self.kwargs.get('locale', 'en-AU')

    def get_template(self):
        base_dir = self.locale
        return f"{base_dir}/{self.template_name}"

    def get_template_names(self):
        return [self.get_template()]


class IndexView(LanguageMixin, TemplateView):
    template_name = "pages/index.html"


class CVView(LanguageMixin, TemplateView):
    template_name = "pages/cv.html"


class ProjectsView(LanguageMixin, TemplateView):
    template_name = "pages/projects.html"


class LinksView(LanguageMixin, TemplateView):
    template_name = "pages/links.html"


class BlogView(LanguageMixin, TemplateView):
    template_name = "pages/blog.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        posts = BlogPost.objects.filter(locale=self.locale).order_by("-datetime")
        return {
            **context,
            "posts": posts
        }

class BlogPostView(LanguageMixin, TemplateView):
    template_name = "pages/post.html"

    def get_context_data(self, *, slug, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            post = BlogPost.objects.get(locale=self.locale, slug=slug)
        except BlogPost.DoesNotExist:
            raise Http404()



        return {
            **context,
            "post": post
        }

