from django.shortcuts import render
from PropertiesCalculator.forms import FirstEnterForm, ACalculatedDataForm, SecondEnterForm,fluidsRU,fluids
from django import forms

def home(request):
    return render(request, 'PropertiesCalculator/home.html',
                  {})

def Afirst_page(request):
    form = FirstEnterForm()
    return render(request, 'PropertiesCalculator/Afirst_page.html',
                  {'form': form, })

def Aenter_page(request):
    fluidRU = fluidsRU[fluids.index(request.GET.get('fluid_field'))]
    fluid=request.GET.get('fluid_field')
    param = request.GET.get('param_field')
    form = SecondEnterForm(fluid,param)
    param = 'Температура' if param == 'T' else 'Давление'
    return render(request, 'PropertiesCalculator/Aenter_page.html',
                  {'form': form, "fluid": fluidRU, "param": param})


def Aresult_page(request):
    fluidRU = fluidsRU[fluids.index(request.GET.get('fluid'))]
    fluid = request.GET.get('fluid')
    param = request.GET.get('param')
    start = request.GET.get('start')
    finish = request.GET.get('finish')
    step = request.GET.get('step')
    form=ACalculatedDataForm(fluid, param, start, finish, step)

    return render(request, 'PropertiesCalculator/Aresult_page.html',
                  {'form': form, "fluid": fluidRU})

def Benter_page(request):
    fluidRU = fluidsRU[fluids.index(request.GET.get('fluid_field'))]
    fluid=request.GET.get('fluid_field')
    param = request.GET.get('param_field')
    form = SecondEnterForm(fluid,param)
    param = 'Температура' if param == 'T' else 'Давление'
    return render(request, 'PropertiesCalculator/Benter_page.html',
                  {'form': form, "fluid": fluidRU, "param": param})


def Bresult_page(request):
    fluidRU = fluidsRU[fluids.index(request.GET.get('fluid'))]
    fluid = request.GET.get('fluid')
    param = request.GET.get('param')
    start = request.GET.get('start')
    finish = request.GET.get('finish')
    step = request.GET.get('step')
    form=ACalculatedDataForm(fluid, param, start, finish, step)

    return render(request, 'PropertiesCalculator/Bresult_page.html',
                  {'form': form, "fluid": fluidRU})