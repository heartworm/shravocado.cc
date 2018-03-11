from django.shortcuts import render, redirect
from django.views.generic.base import TemplateView
from django.views import View
from .models import BlogPost, BlogTag
from django.http import Http404
from django.conf import settings

class LanguageMixin:
    @property
    def locale(self):
        return self.kwargs.get('locale', 'en-AU')

    def get_template(self):
        base_dir = self.locale
        return f"{base_dir}/{self.template_name}"

    def get_template_names(self):
        return [self.get_template()]

    def get_context_data(self, **kwargs):
        return {
            **super().get_context_data(**kwargs),
            'clean': "clean" in self.request.GET
        }


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

    def get_blog_posts(self):
        return BlogPost.objects.filter(locale=self.locale)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        posts = self.get_blog_posts().order_by("-datetime")
        return {
            **context,
            "posts": posts
        }

class BlogByTagView(BlogView):
    def get_blog_posts(self):
        return super().get_blog_posts().filter(tags__name=self.kwargs['tag'])

class BlogPostMixin:
    def get_blog_post(self):
        try:
            return BlogPost.objects.get(locale=self.locale, 
                                        slug=self.kwargs['slug'],
                                        datetime__date = self.kwargs['date'])
        except BlogPost.DoesNotExist:
            raise Http404()



class BlogPostView(LanguageMixin, BlogPostMixin, TemplateView):
    template_name = "pages/post.html"

    def get_context_data(self, *, date, slug, **kwargs):
        context = super().get_context_data(**kwargs)
        return {
            **context,
            "post": self.get_blog_post()
        }

class BlogPostStaticRedirectView(LanguageMixin, BlogPostMixin, View):
    def get(self, request, *, date, slug, path, **kwargs):
        return redirect(
            settings.BLOG_STATIC_URL_BASE.format(
                id=self.get_blog_post().id,
                path=path
            )
        )