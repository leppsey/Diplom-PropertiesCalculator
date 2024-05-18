from django.shortcuts import render
from PropertiesCalculator.forms import FirstEnterForm, CalculatedDataForm, SecondEnterForm


def home(request):
    form = FirstEnterForm()
    return render(request, 'PropertiesCalculator/home.html',
                  {'form': form, })


def enter_page(request):
    fluid = request.GET.get('fluid_field')
    choice1 = request.GET.get('choice_field1')

    # num2 = float(request.GET.get('value_field2'))
    form = SecondEnterForm(choice1, fluid)

    return render(request, 'PropertiesCalculator/enter_page.html',
                  {'form': form, "fluid": fluid})


def result_page(request):
    fluid = request.GET.get('fluid_field')
    choice1 = request.GET.get('choice_field1')

    # num2 = float(request.GET.get('value_field2'))
    form = SecondEnterForm(choice1, fluid)

    return render(request, 'PropertiesCalculator/result_page.html',
                  {'form': form, "fluid": fluid})
