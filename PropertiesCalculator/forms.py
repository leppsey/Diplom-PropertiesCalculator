import base64
from io import BytesIO

from django import forms
import CoolProp.CoolProp as CP
import CoolProp.Plots as CPP
from django.core.exceptions import ValidationError

# CHOICES = (("Q", "Quality [-]"), ("T", "Temperature [K]"), ("P", "Pressure [kPa]"), ("D", "Density [kg/m3]"),
#     ("C0", "Ideal-gas specific heat at constant pressure [kJ/kg/K]"),
#     ("C", "Specific heat at constant pressure [kJ/kg/K]"), ("O", "Specific heat at constant volume [kJ/kg/K]"),
#     ("U", "Internal energy [kJ/kg]"), ("H", "Enthalpy [kJ/kg]"), ("S", "Entropy [kJ/kg/K]"),
#     ("A", "Speed of sound [m/s]"), ("G", "Gibbs function [kJ/kg]"), ("V", "Dynamic viscosity [Pa-s]"),
#     ("L", "Thermal conductivity [kW/m/K]"), ("I", "Surface Tension [N/m]"), ("w", "Accentric Factor [-]"))
CHOICES_A = (("P", "Давление [кПa]"), ("T", "Температура [K]"),)
CHOICES_B = (("P", "Давление [кПa]"), ("T", "Температура [K]"), ("D", "Плотность [кг/м3]"),)
CHOICES_CONST = (("T", "Температура [K]"), ("P", "Давление [кПa]"), ("D", "Плотность [кг/м3]"),
                 ("H", "Энтальпия [кДж/кг]"), ("S", "Энтропия [кДж/кг/K]"),)

# CHOICES2 = (("T", "Temperature [K]"), ("Q", "Quality [-]"), ("P", "Pressure [kPa]"), ("D", "Density [kg/m3]"),
#             ("H", "Enthalpy [kJ/kg]"), ("S", "Entropy [kJ/kg/K]"),)


def calculate(name, input_name1, input_prop1, input_name2, input_prop2, fluid_name, dig=2):
    try:
        return round(CP.PropsSI(name, input_name1, input_prop1, input_name2, input_prop2, fluid_name), dig)
    except Exception as error:
        # return error
        return '-'


def render_img(fluid, graph_type):
    buffer = BytesIO()
    plt = CPP.Plots.PropertyPlot(fluid, graph_type)
    plt.calc_isolines()
    plt.ylabel('Давление, кПа')
    plt.xlabel('Температура, К')
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    graphic = base64.b64encode(image_png)
    return graphic.decode('utf-8')


class ACalculatedDataForm(forms.Form):
    def __init__(self, fluid, param, start, finish, step):
        super().__init__()

        self.T = ['Температура, К']
        self.P = ['Давление, кПа']
        self.D = ['Плотность, кг/м3']
        self.H = ['Энтальпия, Дж/кг']
        self.S = ['Энтропия, Дж/кг/К']
        self.C = ['Теплоемкость при постоянном объеме, Дж/кг/К']
        self.PRANDTL = ['Число Прандтля']
        self.V = ['Динамическая вязкость, Па-с']
        self.L = ['Теплопроводность, кВт/м/К']
        i = 1
        start = float(start)
        finish = float(finish)
        step = float(step)

        while start <= finish:
            self.T.append(calculate("T", param, start, 'Q', 0, fluid))
            self.P.append(calculate("P", param, start, 'Q', 0, fluid))
            self.D.append(calculate("D", param, start, 'Q', 0, fluid))
            self.H.append(calculate("H", param, start, 'Q', 0, fluid))
            self.S.append(calculate("S", param, start, 'Q', 0, fluid, 4))
            self.C.append(calculate("CVMASS", param, start, 'Q', 0, fluid, 4))
            self.PRANDTL.append(calculate("PRANDTL", param, start, 'Q', 0, fluid))
            self.V.append(calculate("V", param, start, 'Q', 0, fluid))
            self.L.append(calculate("L", param, start, 'Q', 0, fluid))
            i += 1
            start += step
        #     для расчета перегретых паров calculate("P", param, start, const_param, const_param_value, fluid)
        self.graphPT = render_img(fluid, 'PT')

class BCalculatedDataForm(forms.Form):
    def __init__(self, fluid, param, start, finish, step,const_param_value,const_param):
        super().__init__()

        self.T = ['Температура, К']
        self.P = ['Давление, кПа']
        self.D = ['Плотность, кг/м3']
        self.H = ['Энтальпия, кДж/кг']
        self.S = ['Энтропия, кДж/кг/К']
        self.C = ['Теплоемкость при постоянном объеме, Дж/кг/К']
        self.PRANDTL = ['Число Прандтля']
        self.V = ['Динамическая вязкость, Па-с']
        self.L = ['Теплопроводность, кВт/м/К']
        i = 1
        start = float(start)
        finish = float(finish)
        step = float(step)
        const_param_value=float(const_param_value)
        while start <= finish:
            self.T.append(calculate("T", param, start, const_param, const_param_value, fluid))
            self.P.append(calculate("P", param, start, const_param, const_param_value, fluid))
            self.D.append(calculate("D", param, start, const_param, const_param_value, fluid))
            self.H.append(calculate("H", param, start, const_param, const_param_value, fluid))
            self.S.append(calculate("S", param, start, const_param, const_param_value, fluid, 4))
            self.C.append(calculate("CVMASS", param, start, const_param, const_param_value, fluid, 4))
            self.PRANDTL.append(calculate("PRANDTL", param, start, const_param, const_param_value, fluid))
            self.V.append(calculate("V", param, start, const_param, const_param_value, fluid))
            self.L.append(calculate("L", param, start, const_param, const_param_value, fluid))
            i += 1
            start += step
        self.graphPT = render_img(fluid, 'PT')


fluidsRU = ['1-Бутен', 'Ацетон', 'Воздух', 'Аммиак', 'Аргон', 'Бензол', 'Диоксид углерода', 'Монооксид углерода',
            'Карбонилсульфид', 'цис-2-Бутен', 'Циклогексан', 'Циклопентан', 'Циклопропан', 'D4', 'D5', 'D6', 'Дейтерий',
            'Дихлорэтан', 'Диэтиловый эфир', 'Диметилкарбонат', 'Диметиловый эфир', 'Этан', 'Этанол', 'Этилбензол',
            'Этилен', 'Оксид этилена', 'Фтор', 'Тяжёлая вода', 'Гелий', 'HFE143m', 'Водород', 'Хлороводород',
            'Сероводород', 'Изобутан', 'Изобутен', 'Изогексан', 'Изопентан', 'Криптон', 'м-Ксилол', 'MD2M', 'MD3M',
            'MD4M', 'MDM', 'Метан', 'Метанол', 'Метиллинолеат', 'Метиллиноленат', 'Метилоолеат', 'Метилпальмитат',
            'Метилстеарат', 'MM', 'н-Бутан', 'н-Декан', 'н-Додекан', 'н-Гептан', 'н-Гексан', 'н-Нонан', 'н-Октан',
            'н-Пентан', 'н-Пропан', 'н-Ундекан', 'Неон', 'Неопентан', 'Азот', 'Закись азота', 'Novec649', 'о-Ксилол',
            'Орто-Дейтерий', 'Орто-Водород', 'Кислород', 'п-Ксилол', 'Пара-Дейтерий', 'Пара-Водород', 'Пропилен',
            'Пропин', 'R11', 'R113', 'R114', 'R115', 'R116', 'R12', 'R123', 'R1233zd(E)', 'R1234yf', 'R1234ze(E)',
            'R1234ze(Z)', 'R124', 'R1243zf', 'R125', 'R13', 'R134a', 'R13I1', 'R14', 'R141b', 'R142b', 'R143a', 'R152A',
            'R161', 'R21', 'R218', 'R22', 'R227EA', 'R23', 'R236EA', 'R236FA', 'R245ca', 'R245fa', 'R32', 'R365MFC',
            'R40', 'R404A', 'R407C', 'R41', 'R410A', 'R507A', 'RC318', 'SES36', 'Диоксид серы', 'Гексафторид серы',
            'Толуол', 'транс-2-Бутен', 'Вода', 'Ксенон']
fluids = ['1-Butene', 'Acetone', 'Air', 'Ammonia', 'Argon', 'Benzene', 'CarbonDioxide', 'CarbonMonoxide',
          'CarbonylSulfide', 'cis-2-Butene', 'CycloHexane', 'Cyclopentane', 'CycloPropane', 'D4', 'D5', 'D6',
          'Deuterium', 'Dichloroethane', 'DiethylEther', 'DimethylCarbonate', 'DimethylEther', 'Ethane', 'Ethanol',
          'EthylBenzene', 'Ethylene', 'EthyleneOxide', 'Fluorine', 'HeavyWater', 'Helium', 'HFE143m', 'Hydrogen',
          'HydrogenChloride', 'HydrogenSulfide', 'IsoButane', 'IsoButene', 'Isohexane', 'Isopentane', 'Krypton',
          'm-Xylene', 'MD2M', 'MD3M', 'MD4M', 'MDM', 'Methane', 'Methanol', 'MethylLinoleate', 'MethylLinolenate',
          'MethylOleate', 'MethylPalmitate', 'MethylStearate', 'MM', 'n-Butane', 'n-Decane', 'n-Dodecane', 'n-Heptane',
          'n-Hexane', 'n-Nonane', 'n-Octane', 'n-Pentane', 'n-Propane', 'n-Undecane', 'Neon', 'Neopentane', 'Nitrogen',
          'NitrousOxide', 'Novec649', 'o-Xylene', 'OrthoDeuterium', 'OrthoHydrogen', 'Oxygen', 'p-Xylene',
          'ParaDeuterium', 'ParaHydrogen', 'Propylene', 'Propyne', 'R11', 'R113', 'R114', 'R115', 'R116', 'R12', 'R123',
          'R1233zd(E)', 'R1234yf', 'R1234ze(E)', 'R1234ze(Z)', 'R124', 'R1243zf', 'R125', 'R13', 'R134a', 'R13I1',
          'R14', 'R141b', 'R142b', 'R143a', 'R152A', 'R161', 'R21', 'R218', 'R22', 'R227EA', 'R23', 'R236EA', 'R236FA',
          'R245ca', 'R245fa', 'R32', 'R365MFC', 'R40', 'R404A', 'R407C', 'R41', 'R410A', 'R507A', 'RC318', 'SES36',
          'SulfurDioxide', 'SulfurHexafluoride', 'Toluene', 'trans-2-Butene', 'Water', 'Xenon']


class AFirstEnterForm(forms.Form):
    temp = ()
    for fluid, fluidRU in zip(fluids, fluidsRU):
        temp = temp + ((fluid, fluidRU),)

    fluid_field = forms.ChoiceField(label='Fluids', choices=temp)
    param_field = forms.ChoiceField(label='Parameter', choices=CHOICES_A)


class BFirstEnterForm(forms.Form):
    temp = ()
    for fluid, fluidRU in zip(fluids, fluidsRU):
        temp = temp + ((fluid, fluidRU),)

    fluid_field = forms.ChoiceField(label='Fluids', choices=temp)
    param_field = forms.ChoiceField(label='Parameter', choices=CHOICES_B)
    const_param_field = forms.ChoiceField(label='Parameter', choices=CHOICES_CONST)


class ASecondEnterForm(forms.Form):
    def __init__(self, fluid, param):
        super().__init__()
        self.fields['fluid'] = forms.CharField(widget=forms.HiddenInput(), initial=fluid)
        self.fields['param'] = forms.CharField(widget=forms.HiddenInput(), initial=param)
        if param == 'T':
            minimum = round(CP.PropsSI('Ttriple', fluid), 2)
            maximum = round(CP.PropsSI('Tcrit', fluid), 2)

        else:
            minimum = round(CP.PropsSI('ptriple', fluid), 2)
            maximum = round(CP.PropsSI('pcrit', fluid), 2)

        self.fields['start'] = forms.FloatField(label='start value', min_value=minimum, max_value=maximum)
        self.fields['finish'] = forms.FloatField(label='finish value', min_value=minimum, max_value=maximum)
        self.fields['step'] = forms.FloatField(label='step value', min_value=0.1,
                                               max_value=(maximum - minimum))
    def clean(self):
        cleaned_data = super().clean()
        start = cleaned_data.get("start")
        finish = cleaned_data.get("finish")
        if start > finish:
            raise ValidationError(
                "Начало не может быть больше конца"
            )

class BSecondEnterForm(forms.Form):
    def __init__(self, fluid, param,const_param):
        super().__init__()
        self.fields['fluid'] = forms.CharField(widget=forms.HiddenInput(), initial=fluid)
        self.fields['param'] = forms.CharField(widget=forms.HiddenInput(), initial=param)
        self.fields['const_param'] = forms.CharField(widget=forms.HiddenInput(), initial=const_param)
        self.fields['const_param_value'] = forms.FloatField(label='start value')
        self.fields['start'] = forms.FloatField(label='start value')
        self.fields['finish'] = forms.FloatField(label='finish value')
        self.fields['step'] = forms.FloatField(label='step value', min_value=0.1)
    def clean(self):
        cleaned_data = super().clean()
        start = cleaned_data.get("start")
        finish = cleaned_data.get("finish")
        if start > finish:
            raise ValidationError(
                "Начало не может быть больше конца"
            )