from django.urls import path, re_path, include
from . import views

urlpatterns = [
    path('cv', views.CVView.as_view()),
    path('projects', views.ProjectsView.as_view()),
    path('links', views.LinksView.as_view()),
    path('blog/', include([
        path('tag/<tag>', views.BlogByTagView.as_view(), name='blog-tag-list'),
        path('', views.BlogView.as_view(), name='blog-list')
    ])),
    re_path(r'blog/post/(?P<date>\d{4}-\d{2}-\d{2})/(?P<slug>[^/\s]+)/', include([
        path('static/<path>', views.BlogPostStaticRedirectView.as_view(), name='post-static'),
        path('', views.BlogPostView.as_view(), name='post'),
    ])),
    path('', views.IndexView.as_view()),
]
