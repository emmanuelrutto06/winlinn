import os

from django.http import HttpRequest
from urllib import request
# from urllib3 import request

from django.conf import settings
from django.contrib.sites.requests import RequestSite
from django.db import models
from authentication.models import User
from django.utils.text import slugify
from django.dispatch import receiver
from django.db.models.signals import pre_save
from ckeditor.fields import RichTextField
from django.utils.safestring import mark_safe
from PIL import Image as Im # new
STATUS = (
    (0,"Draft"),
    (1,"Publish")
)

# Catagory model
class Category(models.Model):
    name = models.CharField(max_length=200, null=True)
    slug = models.SlugField(max_length=200, unique=True)
    image = models.CharField(max_length=300, null=True, blank=True )
    description = models.CharField(max_length=500, null=True,blank=True, verbose_name='Description')

    class Meta:
        verbose_name_plural = 'Category'

    def __str__(self):
        return str(self.name)

# @receiver(pre_save, sender=Category)
# def store_pre_save(sender, instance, *args, **kwargs):
#     if not instance.slug:
#         instance.slug = slugify(instance.name)

# tags model
class Tag(models.Model):

    name  = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.name

# Author model
class Author(models.Model):
    status = (
        ('active', 'active'),
        ('pending', 'pending')
    )
    DESIGNATION = (
        ('writer', 'writer'),
        ('editor', 'editor'),
        ('senior-editor', 'senior-editor')
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    designation = models.CharField(max_length=20, choices=DESIGNATION, default='writer')
    # author_image = models.ImageField(upload_to='author/', verbose_name='Author Profile Image', blank=True, null=True)
    author_image = models.ImageField(upload_to='author/')
    title = models.TextField(blank=True, null=True)
    profile = models.TextField(blank=True, null=True)
    auth_status = models.CharField(max_length=20, choices=status, default='active')

    # class Meta:
    #     verbose_name_plural = 'Author'

    def save(self, *args, **kwargs):
        # delete old file when replacing by updating the file
        try:
            this = Author.objects.get(id=self.id)
            if this.author_image != self.author_image:
                this.author_image.delete(save=False)
        except:
            pass  # when new photo then we do nothing, normal case
        super(Author, self).save(*args, **kwargs)

    def delete(self):
        # deletes files from folder
        try:
            this = Author.objects.get(id=self.id)
            if this.author_image == self.author_image:
                this.author_image.delete(save=False)
        except:
            pass
        super().delete()
    # def __str__(self):
    #     ht =HostInfo()
    #     value =ht.return_host_name()
    #
    #     return str(value)+"media/"+str(self.author_image)
    def __str__(self):
        return f'{self.id} -- {self.user.first_name} {self.user.last_name}'
    
    from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User  # Assuming you're using the default User model

# class Post(models.Model):
#     status_choices = (
#         ('active', 'Active'),
#         ('pending', 'Pending')
#     )

#     title = models.CharField(max_length=200, unique=True)
#     slug = models.SlugField(max_length=200, unique=True, blank=True)  # Allow it to be blank initially
#     author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='blog_posts')
#     # author = models.ForeignKey(Author, on_delete= models.CASCADE,related_name='blog_posts')
#     categories = models.ForeignKey(Category, on_delete=models.DO_NOTHING, null=True)  # Make sure Category is defined
#     updated_on = models.DateTimeField(auto_now=True)
#     content = models.TextField(blank=True, null=True)  # Changed to TextField for longer content
#     image = models.ImageField(upload_to='images/media', null=True, blank=True)
#     visit_count = models.IntegerField(default=0)
#     featured = models.BooleanField(default=False)
#     popular = models.BooleanField(default=False)
#     visible = models.BooleanField(default=True)
#     created_on = models.DateTimeField(auto_now_add=True)
#     status = models.CharField(max_length=20, choices=status_choices, default='pending')
    
class Post(models.Model):
    status = (
        ('active', 'active'),
        ('pending', 'pending')
        )
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    author = models.ForeignKey(Author, on_delete= models.CASCADE,related_name='blog_posts')
    categories = models.ForeignKey(Category, on_delete=models.DO_NOTHING, null=True)
    updated_on = models.DateTimeField(auto_now= True)
    content = RichTextField(blank=True, null=True)
    image = models.ImageField(upload_to='images/media', null=True, blank=True)
    visit_count = models.IntegerField(default=0)
    featured = models.BooleanField(default=False)
    popular = models.BooleanField(default=False)
    visible = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now_add=True)
    post_status = models.CharField(max_length=20, choices=status, default='pending')


    class Meta:
        verbose_name_plural = 'Posts'
        ordering = ['-created_on']
        
    def save(self, *args, **kwargs):
        if self.slug:
            self.slug = slugify(self.title)  # Generate a slug based on the title
            super().save(*args, **kwargs)



    def image_url(self):
        if self.image and hasattr(self.image, 'url'):
            return self.image.url

    def __str__(self):
        return f"{self.title} | {self.categories} | {self.status}"

# class Post(models.Model):
#     status = (
#         ('active', 'active'),
#         ('pending', 'pending')
#     )
#     title = models.CharField(max_length=200, unique=True)
#     slug = models.SlugField(max_length=200, unique=True)
#     author = models.ForeignKey(Author, on_delete= models.CASCADE,related_name='blog_posts')
#     categories = models.ForeignKey(Category, on_delete=models.DO_NOTHING, null=True)
#     updated_on = models.DateTimeField(auto_now= True)
#     content = RichTextField(blank=True, null=True)
#     image = models.ImageField(upload_to='images/media', null=True, blank=True)
#     visit_count = models.IntegerField(default=0)
#     featured = models.BooleanField(default=False)
#     popular = models.BooleanField(default=False)
#     visible = models.BooleanField(default=True)
#     created_on = models.DateTimeField(auto_now_add=True)
#     status = models.CharField(max_length=20, choices=status, default='pending')
#     class Meta:
#         verbose_name_plural = 'Post'
#         ordering = ['-created_on']

#     # def __str__(self):
#     #     return self.title

#     def overview(self):
#         short = self.detail[:30]
#         return short

#     @property
#     def image_url(self):
#         if self.image and hasattr(self.image, 'url'):
#             return self.image.url

#     def __str__(self):
#         return f"{self.title} | {self.categories} | {self.status}"
#         # return f"{self.title} | {self.author.author.username} | {self.categories} | {self.status}"

# Comment Class
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=100, null=True, blank=False)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.post.title} | {self.name } "

# Reply Class
class Reply(models.Model):
    comment = models.ForeignKey(Comment,on_delete=models.CASCADE, related_name='reply')
    name = models.CharField(max_length=200, null=True, blank=False)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.comment} | { self.name } |{ self.created_at }"


# email marketing system
class EmailSignUp(models.Model):
    status = (
        ('active', 'active'),
        ('pending', 'pending'),
        ('cancelled', 'cancelled')
    )
    email  = models.EmailField(blank=True)
    status = models.CharField(max_length=20, choices=status, default='active')

    class Meta:
        verbose_name_plural = " User Emails"

    def __str__(self):
        return self.email

class Contact(models.Model):
    name = models.CharField(max_length=100, null=True, verbose_name='Name')
    email = models.EmailField(null=True)
    messages = models.TextField()
    subject = models.CharField(max_length=200, null=True, verbose_name='Subjects' )

    def __str__(self):
        return f"{ self.name } | { self.subject}"

class Image(models.Model):
    name = models.TextField()
    image = models.ImageField(upload_to='uploads/')
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    # uploaded_by =models.ForeignKey(User, on_delete=models.CASCADE, related_name='images')
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # delete old file when replacing by updating the file
        try:
            this = Image.objects.get(id=self.id)
            if this.image != self.image:
                this.image.delete(save=False)
        except:
            pass  # when new photo then we do nothing, normal case
        super(Image, self).save(*args, **kwargs)

    def delete(self):
        # deletes files from folder
        try:
            this = Image.objects.get(id=self.id)
            if this.image == self.image:
                this.image.delete(save=False)
        except:
            pass
        super().delete()
    #

    def __str__(self):
        ht =HostInfo()
        value =ht.return_host_name()

        return str(value)+"media/"+str(self.image)


    # def save(self):  # new
    #     super().save()
    #     img = Im.open(self.image.path)
    #     # resize it
    #     if img.height > 300 or img.width > 300:
    #         output_size = (300, 300)
    #         img.thumbnail(output_size)
    #         img.save(self.image.path)


from django.contrib.sites.models import Site
class HostInfo:
    def return_host_name(self):
        from django.contrib.sites.shortcuts import get_current_site
        domain = get_current_site(request).domain
        return domain
        # return "http://"+str(os.environ.get("SYSTEM_HOST"))+":"+str(os.environ.get('SYSTEM_DEFAULT_PORT'))


