from django.shortcuts import render, redirect
from .models import Project, Tag
from .form import ProjectForm

def projects(request):
    projects = Project.objects.all()
    context = {
        'projects': projects
    }
    return render(request, 'projects/projects.html', context)


def project(request, pk):
    project = Project.objects.get(id=pk)
    context = {
        'project': project,
    }
    return render(request, 'projects/single-project.html', context)

def createProject(request):
    form = ProjectForm()
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid:
            form.save()
            return redirect('projects')

    context = {'form': form}
    return render(request, 'projects/project-form.html', context)

