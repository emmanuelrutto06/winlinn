from django.urls import reverse_lazy
from django.utils.safestring import mark_safe
from django.views import generic
from django.views.generic import CreateView, DetailView, UpdateView, ListView, DeleteView

from .models import Post
from django.core import paginator
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.db.models.fields import EmailField
from django.shortcuts import render, redirect,get_object_or_404
from django.views import View
from .models import Post, Category,Tag, EmailSignUp,Comment,Author, Image
from django.core.paginator import Paginator
from django.db.models import Count, F
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.db.models import Count, Sum
from authentication.models import User
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from analytics.mixins import ObjectViewedMixin
from .forms import ImageForm, AuthorForm


# class HomeView(generic.ListView):
#     # queryset = Post.objects.filter(status=1).order_by('-created_on')
#     model = Post
#     template_name = 'blog/index.html'

#     def get_context_data(self, *, object_list=None, **kwargs):
#         featured_obj = Post.objects.all().filter(status='active', visible=True, featured=True).order_by('categories',
#                                                                                                         '-created_on')[
#                        :5]
#         print(featured_obj)  # Add this line for debugging


    
#         # featured_obj = Post.objects.all().filter(status='active', visible=True, featured=True).order_by('categories', '-created_on')[:5]

#         popular_obj = Post.objects.all().filter(status='active', visible=True, popular=True).order_by('categories',
#                                                                                                         '-created_on')[
#                        :5]
#         post_obj = Post.objects.all().filter(status='active', visible=True).order_by('categories', '-created_on')

#         # As per Templates Views
#         first_post = featured_obj.first() if featured_obj else ''
#         s_post = featured_obj[0] if featured_obj else ''
#         last_post = featured_obj[2:] if featured_obj else ''

#         context =super().get_context_data(**kwargs)
#         context['post'] =post_obj
#         context['f_post'] =featured_obj
#         context['p_post'] =popular_obj
#         context['first'] =first_post
#         context['s_post'] =s_post
#         context['last_post'] =last_post
#         return context
    


class HomeView(generic.ListView):
    def get(self, request, *args, **kwargs):
        featured_obj = Post.objects.all().filter(post_status='active', visible=True, featured=True).order_by('categories','-created_on')[:5]
        post_obj = Post.objects.all().filter(post_status='active', visible=True).order_by('categories', '-created_on')

        image_path = 'blog/assets/img/winlinmac.jpg'

        # As per Templates Views
        first_post = featured_obj.first()
        s_post = featured_obj
        last_post = featured_obj
        context = {
            'post': post_obj,
            'f_post': featured_obj,
            'first': first_post,
            's_post': s_post,
            'last_post': last_post,
            'image_path': image_path,

        }

        return render(request, 'blog/index.html', context)

# ObjectViewedMixin
class PostDetailView(generic.DetailView):
    model = Post
    template_name = 'blog/single_blog.html'

    def get_context_data(self, **kwargs):
        context =super().get_context_data(**kwargs)
        post_ = Post.objects.filter(slug=self.kwargs['slug'])
        post_.update(visit_count=F('visit_count') + 1)


        post_obj = get_object_or_404(Post, slug=self.kwargs['slug'])
        post_obj.visit_count = post_obj.visit_count + 1
        post_obj.save()

        related_post = Post.objects.filter(author=post_obj.author).exclude(slug=self.kwargs['slug']).order_by('-id')[:2]
        # As per templates views
        first_post = related_post.first() if related_post else ''
        last_post = related_post[1:] if related_post else ''

        context['post'] =post_obj
        context['r_post']= related_post
        context['first'] =first_post
        context['last'] =last_post
        return context

# class PostDetailView(View):

#     def get(self, request, slug, *args, **kwargs):
#         post_obj = get_object_or_404(Post, slug=slug)
#         post_obj.visit_count = post_obj.visit_count + 1
#         post_obj.save()
#         related_post = Post.objects.filter(author=post_obj.author).exclude(slug=slug).order_by('-id')[:4]

#         # As per templates views
#         first_post = related_post.first()
#         last_post = related_post[1:]

#         context = {
#             'post': post_obj,
#             'r_post': related_post,
#             'first': first_post,
#             'last': last_post
#         }
#         print("aaaaaa", context)
#         return render(request, 'blog/single_blog.html', context)


# Category View
class CategoryView(View):
    def get(self, request, slug, *args, **kwargs):
        category_obj = get_object_or_404(Category, slug=slug)
        # post = catagory_obj.blog_set.all().order_by('-id')
        post = Post.objects.filter(categories=category_obj, \
                                   post_status='active', visible=True) \
            .order_by('-created_on')
        popular = Post.objects.filter(categories=category_obj, \
                                      post_status='active', visible=True) \
            .annotate(post_count=Count('visit_count')) \
            .order_by('-visit_count')
        # as Per templates views
        featured_post = popular.first()
        popular_post = popular[1:6]
        # Pagination
        paginator = Paginator(post, 3)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context = {
            'post': page_obj,
            'pop': popular_post,
            'f_post': featured_post,
        }
        return render(request, 'blog/category.html', context)


class CategoryFunction(View):
    # @method_decorator(login_required(login_url='login'))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        catagory_obj = Category.objects.all().order_by('-id')
        context = {
            'category': catagory_obj
        }
        return render(request, 'blog/dashboard/category.html', context)

# tag View
class TagView(View):
    def get(self, request, id, *args, **kwargs):
        tag_obj = get_object_or_404(Tag, id=id)
        post = tag_obj.blog_set.all().order_by('-id')
        tag_count = post.count()
        context = {
            'tag': tag_obj,
            'post': post,
            'tag_count': tag_count
        }
        return render(request, 'home/tag.html', context)


# Subscribe Views
class SubscriptionView(View):
    def post(self, request, *args, **kwargs):

        sub_obj = request.POST.get('email')
        email = EmailSignUp.objects.filter(email=sub_obj)
        if email:
            messages.success(request, 'You are already Subscribed , Thanks!')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            subscribe = EmailSignUp.objects.create(email=sub_obj)
            subscribe.save()
            messages.success(request, 'Thanks for Subscribing')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


# search Views
class SearchView(View):
    def get(self, request, *args, **kwargs):
        search = request.GET['q']
        post = Post.objects.filter(post_status='active', visible=True)
        if len(search) > 100:
            posts = post.none()
        else:
            posts = post.filter(
                Q(title__icontains=search) |
                Q(categories__name__icontains=search) |
                Q(content__icontains=search)

            )
        context = {
            'post': posts,
            'search': search
        }
        return render(request, 'blog/search.html', context)


# Comments View
class CommentView(View):
    def post(self, request, id, *args, **kwargs):
        post = get_object_or_404(Post, id=id)
        name = request.POST.get('name')
        body = request.POST.get('body')
        comment_obj = Comment(post=post, name=name, body=body)
        comment_obj.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def test(request):
    catagory_obj = Category.objects.all()
    cat = Category.objects.all().count()
    lent = len(catagory_obj)
    # post = Catagory.blog_set.count()
    # post = Blog.objects.filter(categories__icontains = catagory_obj).count()

    # src = https://able.bio/rhett/how-to-order-by-count-of-a-foreignkey-field-in-django--26y1ug1

    post = Category.objects.all() \
        .annotate(post_count=Count('blog')) \
        .order_by('-post_count')
    context = {
        'catagory': catagory_obj,
        'cat': cat,
        'lent': lent,
        'post': post

    }
    return render(request, 'test.html', context)


"""
Author Views

"""


# user dashboard views
class Dashboard(View):
    # @method_decorator(login_required(login_url='login'))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        user = request.user
        post = user.author.blog_set.all()
        post_count = post.count()
        post_active = user.author.blog_set.filter(status='active')
        post_active_count = post_active.count()
        post_pending = user.author.blog_set.filter(status='pending')
        post_pending_count = post_pending.count()
        # showing the sum of visit count of spacific users
        post_visit_count = post.aggregate(Sum('visit_count'))['visit_count__sum']
        context = {
            'user': user,
            'post': post,
            'post_count': post_count,
            'post_active': post_active,
            'post_pending': post_pending,
            'post_active_count': post_active_count,
            'post_pending_count': post_pending_count,
            'count': post_visit_count

        }
        return render(request, 'dashboard/dash/dashboard.html', context)


# Create Author
class CreateAuthor(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('dashboard')
        return render(request, 'dashboard/user/create_user.html')

    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            username = request.POST.get('username')
            email = request.POST.get('email')
            first_name = request.POST.get('fname')
            last_name = request.POST.get('lname')
            password1 = request.POST.get('password1')
            password2 = request.POST.get('password2')
            user = User.objects.filter(username=username)
            email_obj = Author.objects.filter(email=email)
            if user:
                messages.warning(request, 'Username Already Exits!')
                return redirect('create_user')
            elif password1 != password2:
                messages.warning(request, 'Password Didn`t match')
                return redirect('create_user')
            else:
                auth_info = {
                    'username': username,
                    'password': make_password(password1)
                }
                user = User(**auth_info)
                user.save()
            if email_obj:
                messages.warning(request, 'Email Already Exits!')
                return redirect('create_user')
            else:
                user_other_obj = Author(author=user, email=email, first_name=first_name, last_name=last_name)
                user_other_obj.save(Author)
                messages.success(request, 'Thanks for Joining Please Log in')
                return redirect('login')


# Author Profile
class AuthorProfile(DetailView):
    model = Author
    template_name = 'blog/author_profile.html'
    context_object_name = 'author'

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #
    #     post_obj = get_object_or_404(Post, slug=self.kwargs['slug'])
    #     post_obj.visit_count = post_obj.visit_count + 1
    #     post_obj.save()
    #     related_post = Post.objects.filter(author=post_obj.author).exclude(slug=self.kwargs['slug']).order_by('-id')[:4]
    #
    #     # As per templates views
    #     first_post = related_post.first()
    #     last_post = related_post[1:]
    #
    #     context['post'] = post_obj
    #     context['r_post'] = related_post
    #     context['first'] = first_post
    #     context['last'] = last_post
    #
    #     return context

# class AuthorProfile(View):
#     # @method_decorator(login_required(login_url='login'))
#     def dispatch(self, request, *args, **kwargs):
#         return super().dispatch(request, *args, **kwargs)
#
#     def get(self, request):
#         print("hhhhhhhhhhhhhh", request.user)
#         author = request.user
#         context = {
#             'author': author
#         }
#
#         return render(request, 'blog/author_profile.html', context)

class AuthorUpdateView(UpdateView):
    model = Author
    form_class = AuthorForm
    template_name = 'blog/edit_profile.html'

    def get_success_url(self):
        return reverse_lazy('blog:author-profile', args=(self.object.id,))

# Edit Author
# class EditAuthor(View):
#     # @method_decorator(login_required(login_url='login'))
#     def dispatch(self, request, *args, **kwargs):
#         return super().dispatch(request, *args, **kwargs)
#
#     def get(self, request):
#         return render(request, 'blog/edit_profile.html')
#
#     def post(self, request):
#         obj = request.user.author
#         obj.author_image = request.POST.get('image')
#         obj.first_name = request.POST.get('fname')
#         obj.last_name = request.POST.get('lname')
#         obj.email = request.POST.get('email')
#         # mail_obj = Author.objects.filter(email=obj.email)
#         # if mail_obj == obj.email:
#         #     messages.success(request,'Your profile has been updated Successfully')
#         #     return redirect('profile')
#         # elif mail_obj:
#         #     messages.warning(request,'sorry Mail already used')
#         #     return redirect ('edit')
#         # else:
#         obj.save()
#         # obj = Author.objects.update(first_name=first_name, last_name=last_name)
#         messages.success(request, 'Your profile has been updated Successfully')
#         return redirect('profile')


# post listing View Active
class PostListingActive(View):
    @method_decorator(login_required(login_url='login'))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        user = request.user
        post_active = user.author.blog_set.filter(status='active').order_by('-id')
        context = {
            'post_active': post_active
        }
        return render(request, 'dashboard/post/post_listing_active.html', context)


# post listing View Pending
class PostListingPending(View):
    @method_decorator(login_required(login_url='login'))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        user = request.user
        post_pending = user.author.blog_set.filter(status='Pending').order_by('-id')
        context = {
            'post_pending': post_pending
        }
        return render(request, 'dashboard/post/post_listing_pending.html', context)

    # Category Views


class CatagoryFunction(View):
    # @method_decorator(login_required(login_url='login'))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        catagory_obj = Category.objects.all().order_by('-id')
        context = {
            'category': catagory_obj
        }
        return render(request, 'blog/dashboard/category.html', context)


# add category
class AddCatagory(View):
    # @method_decorator(login_required(login_url='login'))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        return render(request, 'blog/dashboard/category.html')

    def post(self, request):
        if request.method == 'POST':
            category = request.POST.get('category')
            cat_obj = Category.objects.filter(name=category)
            if cat_obj:
                messages.warning(request, 'Sorry This category already in Databse')
                return redirect('category')
            else:
                obj = Category.objects.create(name=category)
                obj.save()
                messages.success(request, 'Category successfully Added')
                return redirect('category')


# Edit Category
class UpdateCategory(View):
    @method_decorator(login_required(login_url='login'))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, id):
        obj = get_object_or_404(Category, id=id)
        obj.name = request.POST.get('category')
        obj.save()
        return redirect('category')


# Delete Category
class DeleteCategory(View):
    @method_decorator(login_required(login_url='login'))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, id):
        obj = get_object_or_404(Category, id=id)
        obj.delete()
        return redirect('category')

    # Tag functions


class TagFunction(View):
    @method_decorator(login_required(login_url='login'))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        tag_obj = Tag.objects.all().order_by('-id')
        context = {
            'tag': tag_obj
        }
        return render(request, 'dashboard/tag/tag.html', context)


# add Tags
class AddTag(View):
    @method_decorator(login_required(login_url='login'))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        return render(request, 'dashboard/tag/tag.html')

    def post(self, request):
        if request.method == 'POST':
            tag = request.POST.get('tag')
            obj = Tag.objects.create(name=tag)
            obj.save()
            return redirect('tag')


# update Tags
class UpdateTag(View):
    @method_decorator(login_required(login_url='login'))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, id):
        obj = get_object_or_404(Tag, id=id)
        obj.name = request.POST.get('tag')
        obj.save()
        return redirect('tag')


# Delete Tags
class DeleteTag(View):
    @method_decorator(login_required(login_url='login'))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, id):
        obj = get_object_or_404(Tag, id=id)
        obj.delete()
        return redirect('tag')

    # Post Lists


# Create Post
class CreatePost(View):
    @method_decorator(login_required(login_url='login'))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        category = Category.objects.all()
        context = {
            'category': category
        }
        return render(request, 'dashboard/post/create_post.html', context)

    def post(self, request):
        author = request.user.author
        title = request.POST.get('title')
        content = request.POST.get('content')
        image = request.FILES.get('image')
        # tag = request.POST.get('category')
        # tag_obj = Tag.objects.get(name=tag)
        category = request.POST.get('category')
        cat_obj = Category.objects.get(name=category)

        post_obj = Post(author=author, title=title, content=content, image=image, categories=cat_obj)
        post_obj.save(post_obj)
        messages.success(request, 'created Post Successfully')
        return redirect('all_post')


# All Post show
class AllPost(View):
    @method_decorator(login_required(login_url='login'))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        user = request.user.author
        post = user.blog_set.all().order_by('-id')
        context = {
            'post': post
        }
        return render(request, 'dashboard/post/all_post.html', context)


# Post detail
class PostView(View):
    # @method_decorator(login_required(login_url='login'))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, id):
        post_obj = get_object_or_404(Post, id=id)
        context = {
            'post': post_obj
        }
        return render(request, 'dashboard/post/post_view.html', context)


# Edit Post
class EditPost(View):
    # @method_decorator(login_required(login_url='login'))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, id):
        obj = get_object_or_404(Post, id=id)
        cat_obj = Category.objects.all()
        context = {
            'obj': obj,
            'cat': cat_obj
        }
        return render(request, 'dashboard/post/edit_post.html', context)

    def post(self, request, id):
        obj = get_object_or_404(Post, id=id)
        obj.title = request.POST.get('name')
        obj.title = request.POST.get('title')
        obj.content = request.POST.get('content')
        obj.image = request.FILES.get('image')
        category = request.POST.get('category')
        obj.cat_obj = Category.objects.get(name=category)
        obj.save()
        messages.success(request, 'Post has been Updated')
        return redirect('all_post')


# Make VIsible
class VisiblePost(View):
    # @method_decorator(login_required(login_url='login'))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, id):
        obj = Post.objects.get(id=id)
        obj.visible = True
        obj.save()
        messages.success(request, 'Post is Visible')
        # Redirect To the Same Page
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


# Make Hidden
class HidePost(View):
    # @method_decorator(login_required(login_url='login'))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, id):
        obj = Post.objects.get(id=id)
        obj.visible = False
        obj.save()
        messages.success(request, 'Post is Hidden')

        # Redirect To the Same Page
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


# Delete Posts
class DeletePost(View):
    # @method_decorator(login_required(login_url='login'))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, id):
        obj = get_object_or_404(Post, id=id)
        obj.delete()
        messages.success(request, 'Post Has Been Deleted')
        # Redirect To the Same Page
        return redirect('all_post')

# Popular posts
def ArticleOne(request):
    return render(request,'blog/article.html')


class CreateImagePostView(CreateView):  # new
    model = Image
    form_class = ImageForm
    template_name = "blog/images.html"
    # success_url = reverse_lazy("blog:image-detail")


    def form_valid(self, form):
        form.instance.uploaded_by = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('blog:image-detail', args=(self.object.id,))


class ImageList(ListView):
    model = Image


class ImageDetailView(DetailView):
        # specify the model to use
        model = Image

        def get_context_data(self, *args, **kwargs):
            context = super(ImageDetailView,
                            self).get_context_data(*args, **kwargs)
            # add extra field
            context["test"] = "test"
            return context

        # override data before displaying
        def get_object(self, queryset=None):
            obj = super(ImageDetailView, self).get_object(queryset=queryset)
            # if obj.user != obj.name.user:
            #     raise Http404()
            return obj


class ImageUpdateView(UpdateView):
    model = Image
    form_class = ImageForm
    template_name = 'blog/images.html'

    # success_url = "/"
    def get_success_url(self):
        return reverse_lazy('blog:image-detail', args=(self.object.id,))


class ImageDeleteView(DeleteView):
    # specify the model you want to use
    model = Image
    success_url = reverse_lazy("blog:image-list")


    # def delete(self, request, *args, **kwargs):
    #     object = self.get_object()
    #     if object.name:
    #         object.name.delete(save=False)
    #     return super().delete(request, *args, **kwargs)