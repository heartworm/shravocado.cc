from django.urls import path
from . import views

urlpatterns = [
    path('cv', views.CVView.as_view()),
    path('projects', views.ProjectsView.as_view()),
    path('links', views.LinksView.as_view()),
    path('blog', views.BlogView.as_view()),
    path('blog/post/<slug:slug>', views.BlogPostView.as_view(), name='post'),
    path('', views.IndexView.as_view()),
]
