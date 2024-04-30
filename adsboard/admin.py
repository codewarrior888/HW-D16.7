from django.contrib import admin
from .models import Post, Category, PostCategory, Comment, OTPCode
from modeltranslation.admin import TranslationAdmin


class CategoryInline(admin.TabularInline):
    model = PostCategory
    extra = 1


class PostAdmin(TranslationAdmin):
    model = Post
    inlines = (CategoryInline,)
    list_display = ('title', 'pk',)
    list_filter = ('category', 'author')
    search_fields = ('title', 'category__name')


class CategoryAdmin(TranslationAdmin):
    model = Category


class CommentAdmin(admin.ModelAdmin):
    list_display = ('content', 'author', 'post', 'status')
    list_filter = ('status', 'post')
    search_fields = ('author', 'post')
    actions = ['approve_comments', 'reject_comments']

    def approve_comments(self, request, queryset):
        queryset.update(status=True)



admin.site.register(Post, PostAdmin)
admin.site.register(Category)
admin.site.register(PostCategory)
admin.site.register(Comment, CommentAdmin)
admin.site.register(OTPCode)
