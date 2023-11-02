from django.contrib import admin
from .models import Post,Category,Comment,Reply,Tag,EmailSignUp,Contact,Image,Author


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'post_status','created_on')
    list_filter = ("post_status",)
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}
    # prepopulated_fields = {'slug': ('name',)}

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}

admin.site.register(Post, PostAdmin)
admin.site.register(Category,CategoryAdmin)
admin.site.register(Author)
admin.site.register(Comment)
admin.site.register(Reply)
admin.site.register(Tag)
admin.site.register(EmailSignUp)
admin.site.register(Contact)
admin.site.register(Image)

