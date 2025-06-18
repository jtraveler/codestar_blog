from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.views import generic
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Post, CollaborationRequest, About, Comment 
from .forms import CommentForm, CollaborationForm


class PostList(generic.ListView):
    queryset = Post.objects.filter(status=1)
    template_name = "blog/index.html"
    paginate_by = 6


def post_detail(request, slug):
    """
    Display an individual :model:`blog.Post`.

    **Context**

    ``post``
        An instance of :model:`blog.Post`.
    ``comments``
        All comments related to the post (both approved and unapproved).

    **Template:**

    :template:`blog/post_detail.html`
    """
    queryset = Post.objects.filter(status=1)
    post = get_object_or_404(queryset, slug=slug)
    
    # Get ALL comments for this post (template will handle conditional display)
    comments = post.comments.all().order_by('created_on')
    comment_count = post.comments.filter(approved=True).count()
    
    comment_form = CommentForm()
    
    if request.method == "POST":
        print("Comment form submitted!")  # Debug line
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            print("Comment form is valid!")  # Debug line
            comment = comment_form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.approved = False  # Explicitly set to False
            comment.save()
            print(f"Comment saved with ID: {comment.id}")  # Debug line
            messages.add_message(
                request, messages.SUCCESS,
                'Comment submitted and awaiting approval'
            )
            comment_form = CommentForm()
        else:
            print("Comment form errors:", comment_form.errors)  # Debug line

    return render(
        request,
        "blog/post_detail.html",
        {
            "post": post,
            "comments": comments,
            "comment_count": comment_count,
            "comment_form": comment_form,
        },
    )


def about_me(request):
    """
    Renders the About page with collaboration form
    """
    about = About.objects.all().order_by('-updated_on').first()
    
    if request.method == "POST":
        print("POST request received!")  # Debug line
        print("POST data:", request.POST)  # Debug line
        collaborate_form = CollaborationForm(data=request.POST)
        if collaborate_form.is_valid():
            print("Form is valid!")  # Debug line
            collaborate_form.save()
            print("Form saved!")  # Debug line
            messages.add_message(
                request, messages.SUCCESS,
                "Collaboration request received! I endeavour to respond within 2 working days."
            )
            collaborate_form = CollaborationForm()
        else:
            print("Form is NOT valid!")  # Debug line
            print("Form errors:", collaborate_form.errors)  # Debug line
    else:
        collaborate_form = CollaborationForm()

    return render(
        request,
        "about/about.html",
        {
            "about": about,
            "collaborate_form": collaborate_form,
        },
    )


def profile_page(request):
    """
    Display a user's profile page with all their comments.
    
    **Context**
    
    ``user``
        The current user object.
    ``comments``
        All comments made by the user.
        
    **Template:**
    
    :template:`blog/profile.html`
    """
    user = get_object_or_404(User, username=request.user.username)
    comments = user.commenter.all()
    
    return render(
        request,
        "blog/profile.html",
        {
            "user": user,
            "comments": comments,
        },
    )


def collaboration_request(request):
    """
    Renders the Collaboration Request page and handles form submission.
    
    **Context**
    
    ``collaboration_form``
        An instance of :form:`blog.CollaborationForm`.
        
    **Template:**
    
    :template:`blog/collaboration.html`
    """
    collaboration_form = CollaborationForm()
    
    if request.method == "POST":
        collaboration_form = CollaborationForm(data=request.POST)
        if collaboration_form.is_valid():
            collaboration_form.save()
            messages.add_message(
                request, messages.SUCCESS,
                "Collaboration request received! I endeavour to respond within 2 working days."
            )
            # Reset form after successful submission
            collaboration_form = CollaborationForm()

    return render(
        request,
        "blog/collaboration.html",
        {
            "collaboration_form": collaboration_form,
        },
    )


def comment_edit(request, slug, comment_id):
    """
    view to edit comments
    """
    if request.method == "POST":
        print(f"Comment edit submitted for comment ID: {comment_id}")  # Debug line
        
        queryset = Post.objects.filter(status=1)
        post = get_object_or_404(queryset, slug=slug)
        comment = get_object_or_404(Comment, pk=comment_id)
        comment_form = CommentForm(data=request.POST, instance=comment)

        if comment_form.is_valid() and comment.author == request.user:
            print("Comment edit form is valid!")  # Debug line
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.approved = False
            comment.save()
            print(f"Comment {comment_id} updated successfully!")  # Debug line
            messages.add_message(request, messages.SUCCESS, 'Comment Updated!')
        else:
            print("Comment edit form errors:", comment_form.errors)  # Debug line
            print(f"User check: comment.author={comment.author}, request.user={request.user}")  # Debug line
            messages.add_message(request, messages.ERROR, 'Error updating comment!')

    return HttpResponseRedirect(reverse('post_detail', args=[slug]))


@login_required
def post_edit(request, slug):
    """
    Edit a blog post
    """
    post = get_object_or_404(Post, slug=slug)
    
    # Check if user is the author
    if request.user != post.author:
        messages.error(request, "You can only edit your own posts.")
        return redirect('post_detail', slug=slug)
    
    if request.method == 'POST':
        # Update post with form data
        post.title = request.POST.get('title')
        post.excerpt = request.POST.get('excerpt')
        post.content = request.POST.get('content')
        post.status = int(request.POST.get('status'))
        post.save()
        
        messages.success(request, f'Post "{post.title}" has been updated!')
        return redirect('post_detail', slug=post.slug)
    
    return render(request, 'blog/edit_post.html', {'post': post})


@login_required  
def post_delete(request, slug):
    """
    Delete a blog post
    """
    post = get_object_or_404(Post, slug=slug)
    
    # Check if user is the author
    if request.user != post.author:
        messages.error(request, "You can only delete your own posts.")
        return redirect('post_detail', slug=slug)
    
    if request.method == 'POST':
        post.delete()
        messages.success(request, f'Post "{post.title}" has been deleted.')
        return redirect('home')
    
    return render(request, 'blog/delete_post.html', {'post': post})