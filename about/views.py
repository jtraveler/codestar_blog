from django.shortcuts import render
from django.contrib import messages
from .models import About
from blog.models import CollaborationRequest
from blog.forms import CollaborationForm

# Create your views here.

def about_me(request):
    """
    Renders the About page with collaboration form
    """
    about = About.objects.all().order_by('-updated_on').first()
    
    if request.method == "POST":
        print("POST request received in about app!")  # Debug line
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
            # Create a fresh form after successful submission
            collaborate_form = CollaborationForm()
        else:
            print("Form is NOT valid!")  # Debug line
            print("Form errors:", collaborate_form.errors)  # Debug line
    else:
        # Create a fresh form for GET requests
        collaborate_form = CollaborationForm()

    return render(
        request,
        "about/about.html",
        {
            "about": about,
            "collaborate_form": collaborate_form,
        },
    )