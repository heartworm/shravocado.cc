from django.shortcuts import render
from django.views.generic.base import TemplateView

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
