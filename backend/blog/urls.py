from django.urls import path, re_path
from . import views

urlpatterns = [
    path('cv', views.CVView.as_view()),
    path('projects', views.ProjectsView.as_view()),
    path('links', views.LinksView.as_view()),
    path('blog/', views.BlogView.as_view()),
    re_path(r'blog/post/(?P<date>\d{4}-\d{2}-\d{2})/(?P<slug>\S+)', views.BlogPostView.as_view(), name='post'),
    path('', views.IndexView.as_view()),
]
