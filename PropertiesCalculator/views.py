from django.shortcuts import render
import CoolProp.Plots as CPP
from PropertiesCalculator.forms import FullForm, CalculatedDataForm


def home(request):
    form = FullForm()
    return render(request, 'PropertiesCalculator/home.html',
                  {'form': form, })


def result(request):
    fluid = request.GET.get('fluid_field')
    choice1 = request.GET.get('choice_field1')
    choice2 = request.GET.get('choice_field2')
    num1 = float(request.GET.get('value_field1'))
    num2 = float(request.GET.get('value_field2'))
    form = CalculatedDataForm(choice1, num1, choice2, num2, fluid)

    return render(request, 'PropertiesCalculator/result.html',
                  {'form': form, "fluid": fluid})
