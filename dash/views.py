from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from dash.models import Employer
from .forms import EmpForm

@login_required(login_url='sign-in')
def index(request):
    return render(request, 'pages/index.html')


@login_required(login_url='sign-in')
def emp(request):
    roots = Employer.objects.all()
    ctx = {
        'roots':roots
    }
    return render(request, 'pages/ishchi/list.html', ctx)


@login_required(login_url='sign-in')
def about(request, pk):
    root = Employer.objects.filter(pk=pk).first()
    ctx = {
        'roots':root
    }
    return render(request, 'pages/ishchi/about.html', ctx)


@login_required(login_url='sign-in')
def create(request):
    if request.POST:
        form = EmpForm(request.POST, request.FILES or None)
        if form.is_valid():
            form.save()
            return redirect('emp')
        else:
            print(form.error)
    form = EmpForm()
    ctx = {
        "form" : form
    }
    return render(request, 'pages/ishchi/create.html', ctx)



@login_required(login_url='sign-in')
def edit(request, pk):
    root = Employer.objects.filter(pk=pk).first()
    if not root:
        return redirect('emp')
    if request.POST:
        form = EmpForm(request.POST, request.FILES or None, instance=root)
        if form.is_valid():
            form.save()
            return redirect('emp')
        else:
            print(form.error)
    form = EmpForm(instance=root)
    ctx = {
        'roots':root,
        "form" : form
    }
    return render(request, 'pages/ishchi/create.html', ctx)



@login_required(login_url='sign-in')
def delete(request, pk, conf=False):
    if conf:
        try:
            Employer.objects.get(pk=pk).delete()
        except:
            pass
    return redirect('emp')



