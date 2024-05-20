from django.shortcuts import render
from PropertiesCalculator.forms import FirstEnterForm, CalculatedDataForm, SecondEnterForm,fluidsRU,fluids
from django import forms

def home(request):
    form = FirstEnterForm()
    return render(request, 'PropertiesCalculator/home.html',
                  {'form': form, })


def enter_page(request):
    fluidRU = fluidsRU[fluids.index(request.GET.get('fluid_field'))]
    fluid=request.GET.get('fluid_field')
    param = request.GET.get('param_field')
    form = SecondEnterForm(fluid,param)
    param = 'Температура' if param is 'T' else 'Давление'
    return render(request, 'PropertiesCalculator/enter_page.html',
                  {'form': form, "fluid": fluidRU, "param": param})


def result_page(request):
    fluidRU = fluidsRU[fluids.index(request.GET.get('fluid'))]
    fluid = request.GET.get('fluid')
    param = request.GET.get('param')
    start = request.GET.get('start')
    finish = request.GET.get('finish')
    step = request.GET.get('step')
    form=CalculatedDataForm(fluid,param,start,finish,step)

    return render(request, 'PropertiesCalculator/result_page.html',
                  {'form': form, "fluid": fluidRU})
