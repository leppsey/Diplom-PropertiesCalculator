from django import forms
from django.shortcuts import render
import CoolProp.CoolProp as CP
import CoolProp.Plots as CPP
from django.http import HttpResponse
from PropertiesCalculator.forms import FluidForm, Parameter1Form, Parameter2Form


# from PropertiesCalculator.forms import ApplicationForm


# Create your views here.
parameters1 = Parameter1Form()
parameters2 = Parameter2Form()
fluids = FluidForm()

def home(request):

    return render(request, 'PropertiesCalculator/home.html', {'fluids': fluids, 'parameters1': parameters1,'parameters2': parameters2, })


def result(request):
    choice1 = request.GET.get('field1')
    choice2 = request.GET.get('field2')
    num1 = request.GET.get('number1')
    num2 = request.GET.get('number2')
    if choice1 == choice2 or num1 =='' or num2 == '' or int(num1) < 0 or int(num2) < 0:
        return render(request, 'PropertiesCalculator/home.html', {'fluids': fluids, 'parameters1': parameters1,'parameters2': parameters2,'error':'Invalid Input!', })
    # if request.GET.get('submit') == "":
    #     ans = 'suck my dick'
    ans = [choice1, choice2, num1, num2]
    return render(request, 'PropertiesCalculator/result.html', {'ans': ans})
