from django.shortcuts import render
from PropertiesCalculator.forms import FirstEnterForm, CalculatedDataForm, SecondEnterForm,fluidsRU,fluids,StylesForm


def home(request):
    form = FirstEnterForm()
    return render(request, 'PropertiesCalculator/home.html',
                  {'form': form, })


def enter_page(request):
    fluidRU = fluidsRU[fluids.index(request.GET.get('fluid_field'))]
    fluid=request.GET.get('fluid_field')
    param = request.GET.get('param_field')
    # form = SecondEnterForm(param,fluid)
    form=StylesForm(site_id=fluid)
    return render(request, 'PropertiesCalculator/enter_page.html',
                  {'form': form, "fluid": fluidRU, "param": param})


def result_page(request):
    # fluid = request.GET.get('fluid_field')
    # choice1 = request.GET.get('choice_field1')

    # num2 = float(request.GET.get('value_field2'))
    # form = SecondEnterForm(choice1, fluid)

    return render(request, 'PropertiesCalculator/result_page.html',
                  {'form': form, "fluid": fluid})
