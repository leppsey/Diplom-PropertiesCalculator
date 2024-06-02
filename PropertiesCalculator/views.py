from django.shortcuts import render
from PropertiesCalculator.forms import AFirstEnterForm, ACalculatedDataForm, ASecondEnterForm, fluidsRU, fluids, \
    BFirstEnterForm, BSecondEnterForm,BCalculatedDataForm
import CoolProp.CoolProp as CP

def RUname(param):
    match param:
        case 'T':
            return 'Температура, K'
        case 'P':
            return 'Давление, кПа'
        case 'D':
            return 'Плотность, кг/м³'
        case 'H':
            return 'Энтальпия, Дж/кг'
        case 'S':
            return 'Энтропия, Дж/кг/К'
        case _:
            return ''


def home(request):
    return render(request, 'PropertiesCalculator/home.html',
                  {})


def Afirst_page(request):
    form = AFirstEnterForm()
    return render(request, 'PropertiesCalculator/Afirst_page.html',
                  {'form': form, })


def Aenter_page(request):
    fluidRU = fluidsRU[fluids.index(request.GET.get('fluid_field'))]
    fluid = request.GET.get('fluid_field')
    param = request.GET.get('param_field')
    form = ASecondEnterForm(fluid, param)
    Tmin = str(round(CP.PropsSI('Ttriple', fluid), 2))+' K'
    Tmax =  str(round(CP.PropsSI('Tcrit', fluid), 2))+' K'
    Pmin =  str(round(CP.PropsSI('ptriple', fluid) / pow(10, 3), 2))+' кПа'
    Pmax =  str(round(CP.PropsSI('pcrit', fluid) / pow(10, 3), 2))+' кПа'
    param = RUname(param)
    return render(request, 'PropertiesCalculator/Aenter_page.html',
                  {'form': form, "fluid": fluidRU, "param": param,"Tmin":Tmin,"Tmax":Tmax,"Pmin":Pmin,"Pmax":Pmax})


def Aresult_page(request):
    fluidRU = fluidsRU[fluids.index(request.GET.get('fluid'))]
    fluid = request.GET.get('fluid')
    param = request.GET.get('param')
    start = request.GET.get('start')
    finish = request.GET.get('finish')
    step = request.GET.get('step')
    form = ACalculatedDataForm(fluid, param, start, finish, step)

    return render(request, 'PropertiesCalculator/Aresult_page.html',
                  {'form': form, "fluid": fluidRU})


def Bfirst_page(request):
    form = BFirstEnterForm()
    return render(request, 'PropertiesCalculator/Bfirst_page.html',
                  {'form': form, })


def Benter_page(request):
    fluidRU = fluidsRU[fluids.index(request.GET.get('fluid_field'))]
    fluid = request.GET.get('fluid_field')
    param = request.GET.get('param_field')
    const_param = request.GET.get('const_param_field')
    form = BSecondEnterForm(fluid, param,const_param)
    param = RUname(param)
    const_param=RUname(const_param)
    return render(request, 'PropertiesCalculator/Benter_page.html',
                  {'form': form, "fluid": fluidRU, "param": param,"const_param": const_param})


def Bresult_page(request):
    fluidRU = fluidsRU[fluids.index(request.GET.get('fluid'))]
    fluid = request.GET.get('fluid')
    param = request.GET.get('param')
    const_param = request.GET.get('const_param')
    const_param_value = request.GET.get('const_param_value')
    start = request.GET.get('start')
    finish = request.GET.get('finish')
    step = request.GET.get('step')
    form = BCalculatedDataForm(fluid, param, start, finish, step, const_param_value, const_param)

    return render(request, 'PropertiesCalculator/Bresult_page.html',
                  {'form': form, "fluid": fluidRU})
