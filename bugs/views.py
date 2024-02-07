from django.shortcuts import render, redirect, reverse,  get_object_or_404
from .forms import  BugForm

from django.views.generic import ListView, CreateView  # new
from django.urls import reverse_lazy  # new

# from .forms import BugForm  # new
from .models import Bug, Attachment
# Create your views here.


# bugs homepage
def homepage(request):
    context = {}
    return render(request, "bugs/index.html", context)


def bug_form(request):
    if request.method == 'POST':
        form = BugForm(request.POST, request.FILES)
        if form.is_valid():
            # Manually create the Bug instance
            bug = Bug(
                user=request.user,  # Set the user
                title=form.cleaned_data['title'],
                description=form.cleaned_data['description'],
            )
            bug.save()

            # Check if a file was uploaded and then create an Attachment instance
            file = form.cleaned_data.get('file')
            if file:
                Attachment.objects.create(
                    bug=bug,
                    file=file
                )

            return redirect(reverse('homepage'))
    else:
        form = BugForm()

    return render(request, 'bugs/register_bug.html', {'form': form})


def bug_list(request):
    bugs = Bug.objects.all()  # Get all bugs from the database
    return render(request, 'bugs/bug_list.html', {'bugs': bugs})


def bug_detail(request, bug_id):
    bug = get_object_or_404(Bug, pk=bug_id)  # Fetch the bug or return a 404
    attachments = bug.attachments.all()  # Retrieve all related attachments
    return render(request, 'bugs/bug_detail.html', {'bug': bug, 'attachments': attachments})



