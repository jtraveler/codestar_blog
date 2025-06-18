from django.contrib import admin
from .models import Post, Comment, CollaborationRequest, About
from django_summernote.admin import SummernoteModelAdmin

@admin.register(About)
class AboutAdmin(SummernoteModelAdmin):
    summernote_fields = ('content',)
    list_display = ('title', 'updated_on')

@admin.register(Post)
class PostAdmin(SummernoteModelAdmin):
    summernote_fields = ('content',)  # Replace 'content' with your actual field name
    list_display = ('title', 'slug', 'status', 'created_on')
    list_filter = ('status', 'created_on')
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'body', 'post', 'created_on', 'approved')
    list_filter = ('approved', 'created_on')
    search_fields = ('author__username', 'body')
    actions = ['approve_comments']

    def approve_comments(self, request, queryset):
        queryset.update(approved=True)
        
    approve_comments.short_description = "Approve selected comments"


@admin.register(CollaborationRequest)
class CollaborationRequestAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'message', 'read', 'created_on')
    list_filter = ('read', 'created_on')
    search_fields = ('name', 'email')