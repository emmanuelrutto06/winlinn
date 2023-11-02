from . import views
from django.urls import path

app_name = 'blog'
urlpatterns = [


    # path('', views.HomeView.as_view(), name='home'),
    path('', views.HomeView.as_view(), name='home'),

    path('search/', views.SearchView.as_view(), name='search'),
    # path('<slug:slug>/', views.PostDetailView.as_view(), name='single-post' ),
    
    path('<slug:slug>/', views.PostDetailView.as_view(), name='single-post'),



    #
    path('category/<slug:slug>', views.CategoryView.as_view(), name='post-category'),
    path('tag/<int:id>', views.TagView.as_view(), name='tag'),
    path('member/subscription/', views.SubscriptionView.as_view(), name='member-subscription'),
    path('<int:id>/create-comment/', views.CommentView.as_view(), name='comment'),

    # Author
    path('author/<int:pk>/', views.AuthorProfile.as_view(), name='author-profile'),
    path('author/<int:pk>/edit/', views.AuthorUpdateView.as_view(), name="author-edit"),

    # Images
    path('images', views.ImageList.as_view(), name="image-list"),
    path("images/upload", views.CreateImagePostView.as_view(), name="image-upload"),
    path('images/<int:pk>/', views.ImageDetailView.as_view(),name='image-detail'),
    path('images/<int:pk>/edit/', views.ImageUpdateView.as_view(), name='image-update'),
    path('images/<int:pk>/delete/', views.ImageDeleteView.as_view(),  name='image-delete'),

    # Articles
    path('article/', views.ArticleOne, name='article-one'),

] 
