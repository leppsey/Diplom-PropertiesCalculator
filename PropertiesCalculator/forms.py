import base64
from io import BytesIO

from django import forms
import CoolProp.CoolProp as CP
import CoolProp.Plots as CPP

# from django_matplotlib import MatplotlibFigureField
# CHOICES = (("Q", "Quality [-]"), ("T", "Temperature [K]"), ("P", "Pressure [kPa]"), ("D", "Density [kg/m3]"),
#     ("C0", "Ideal-gas specific heat at constant pressure [kJ/kg/K]"),
#     ("C", "Specific heat at constant pressure [kJ/kg/K]"), ("O", "Specific heat at constant volume [kJ/kg/K]"),
#     ("U", "Internal energy [kJ/kg]"), ("H", "Enthalpy [kJ/kg]"), ("S", "Entropy [kJ/kg/K]"),
#     ("A", "Speed of sound [m/s]"), ("G", "Gibbs function [kJ/kg]"), ("V", "Dynamic viscosity [Pa-s]"),
#     ("L", "Thermal conductivity [kW/m/K]"), ("I", "Surface Tension [N/m]"), ("w", "Accentric Factor [-]"))
CHOICES1 = (("P", "Давление [кПa]"), ("T", "Температура [K]"),)
CHOICES2 = (("T", "Temperature [K]"), ("Q", "Quality [-]"), ("P", "Pressure [kPa]"), ("D", "Density [kg/m3]"),
            ("H", "Enthalpy [kJ/kg]"), ("S", "Entropy [kJ/kg/K]"),)


def calculate(name, input_name1, input_prop1, input_name2, input_prop2, fluid_name):
    try:
        return CP.PropsSI(name, input_name1, input_prop1, input_name2, input_prop2, fluid_name)
    except Exception as error:
        error = str(error)
        return error[:error.find(': Pro')]


def render_img(fluid, graph_type):
    buffer = BytesIO()
    plt = CPP.Plots.PropertyPlot(fluid, graph_type)
    plt.calc_isolines()

    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    graphic = base64.b64encode(image_png)
    return graphic.decode('utf-8')


class CalculatedDataForm(forms.Form):
    def __init__(self, input_name1, input_prop1, input_name2, input_prop2, fluid_name):
        super().__init__()
        self.Q = calculate("Q", input_name1, input_prop1, input_name2, input_prop2, fluid_name)

        self.graphPT = render_img(fluid_name, 'PT')


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

class FirstEnterForm(forms.Form):
    temp = ()
    for fluid,fluidRU in zip(sorted(CP.FluidsList()),fluidsRU):
        temp = temp + ((fluid, fluidRU),)

    fluid_field = forms.ChoiceField(label='Fluids', choices=temp)
    choice_field1 = forms.ChoiceField(label='Parameter 1', choices=CHOICES1)

class SecondEnterForm(forms.Form):
    value_field1 = forms.FloatField(label='Value 1', min_value=0)