from django.shortcuts import render, redirect, reverse,  get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from .forms import BugForm
from .models import Bug, Attachment


@login_required
def homepage(request):
    """
      View to display the bugs reporting homepage
      :param request: 
      :return: returns all bugs and a link to submit a new bug report
    """
    bugs = Bug.objects.filter(user=request.user)  # Get all bugs from the database
    return render(request, 'bugs/bug_list.html', {'bugs': bugs})


@login_required()
def bug_form(request):
    """
    View to submit a new bug report
    :param request:
    :return: returns all bugs including the new bug report
    """
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

            messages.success(request, 'Bug submitted successfully!')
            return redirect(reverse('bugs:homepage'))
    else:
        form = BugForm()

    return render(request, 'bugs/register_bug.html', {'form': form})


@login_required()
def bug_list(request):
    """
     View to display all the bugs created by the authenticated user
    :param request:
    :return: list of all bugs created by the authenticated user
    """
    if request.user.is_superuser:
        bugs = Bug.objects.all()  # Retrieves all bugs for superuser
    else:
        bugs = Bug.objects.filter(user=request.user)  # Get all bugs from the database
    return render(request, 'bugs/bug_list.html', {'bugs': bugs})


@login_required()
def bug_detail(request, bug_id):
    """
    View to display the details of a bug by id
    :param request:bug i
    :param bug_id:
    :return: details about the bug
    """
    bug = get_object_or_404(Bug, pk=bug_id)  # Fetch the bug or return a 404
    attachments = bug.attachments.all()  # Retrieve all related attachments
    return render(request, 'bugs/bug_detail.html', {'bug': bug, 'attachments': attachments})


@login_required()
def update_bug(request, bug_id):
    """
    View to update a bug by id and its attachments
    :param request:
    :param bug_id: id of the bug to be updated
    :return: details about the updated bug
    """
    bug = get_object_or_404(Bug, pk=bug_id)

    if not (request.user == bug.user or request.user.is_superuser):
        messages.error(request, 'You are not allowed to edit this bug!')
        return redirect("bugs:homepage")

    if request.method == 'POST':
        form = BugForm(request.POST)
        if form.is_valid():
            # Manually update the bug instance with the form's cleaned data
            bug.title = form.cleaned_data['title']
            bug.description = form.cleaned_data['description']
            # Save the updated bug
            bug.save()
            messages.success(request, 'Bug updated successfully!')
            return redirect('bugs:bug_detail', bug_id=bug.id)  # Redirect as appropriate
    else:
        # Prepopulate the form with the instance's current data
        initial_data = {
            'title': bug.title,
            'description': bug.description,
            'status': bug.status,
        }
        form = BugForm(initial=initial_data)

    return render(request, 'bugs/update_bug.html', {'form': form, 'bug_id': bug_id})


@login_required()
@permission_required('bugs.delete_bug')
def delete_bug(request, bug_id):
    """
    Delete an existing bug by id
    :param request:
    :param bug_id:
    :return: returns the list of all bugs after deleting the specified bug
    """
    bug = get_object_or_404(Bug, pk=bug_id)
    bug.delete()
    messages.success(request, 'Bug deleted successfully!')
    return redirect('bugs:homepage')
