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
CHOICES_CONST = (("P", "Давление [кПa]"), ("T", "Температура [K]"),)
# CHOICES_CONST = (("T", "Температура [K]"), ("P", "Давление [кПa]"),)


CHOICES_B = (("T", "Температура [K]"), ("P", "Давление [кПa]"), ("D", "Плотность [кг/м3]"),
                 ("H", "Энтальпия [Дж/кг]"), ("S", "Энтропия [Дж/кг/K]"),)


# CHOICES2 = (("T", "Temperature [K]"), ("Q", "Quality [-]"), ("P", "Pressure [kPa]"), ("D", "Density [kg/m3]"),
#             ("H", "Enthalpy [kJ/kg]"), ("S", "Entropy [kJ/kg/K]"),)


def calculate(name, input_name1, input_prop1, input_name2, input_prop2, fluid_name, delimiter=1.0,flag=0):
    try:
        if flag==0:
            return CP.PropsSI(name, input_name1, input_prop1, input_name2, input_prop2, fluid_name) / delimiter
        else:
            return flag/(CP.PropsSI(name, input_name1, input_prop1, input_name2, input_prop2, fluid_name) / delimiter)
    except Exception as error:
        # return error
        return '-'


def digits(value, numb=2):
    if not value == '-':
        i = 0
        temp = 1
        while temp > value:
            temp = temp / 10.0
            i += 1
        if i > numb:
            numb = i + 1
        return round(value, numb)
    else:
        return value


def render_img(fluid, graph_type):
    buffer = BytesIO()
    plt = CPP.Plots.PropertyPlot(fluid, graph_type)

    plt.calc_isolines()
    plt.ylabel('Давление, Па')
    plt.xlabel('Энтальпия, Дж/кг')
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    graphic = base64.b64encode(image_png)
    return graphic.decode('utf-8')


class ACalculatedDataForm(forms.Form):
    def __init__(self, fluid, param, start, finish, step):
        super().__init__()

        self.T_title = 'T, К'
        self.P_title = 'P, кПа'
        self.D_title = "ʋ', м³/кг*10⁻³"
        self.H_title = "h', кДж/кг"
        self.S_title = "s', кДж/кг/К"
        self.Dp_title = "ʋ'', м³/кг"
        self.Hp_title = "h'', кДж/кг"
        self.Sp_title = "s'', кДж/кг/К"
        self.C_title = "Cv', Дж/кг/К"
        self.PRANDTL_title = "Pr'"
        self.V_title = "Ƞ', Па-с*10⁻⁵"
        self.L_title = "λ', Вт/м/К"
        self.Cp_title = "Cv'', Дж/кг/К"
        self.PRANDTLp_title = "Pr''"
        self.Vp_title = "Ƞ'', Па-с*10⁻⁵"
        self.Lp_title = "λ'', Вт/м/К"

        self.T =[]
        self.P =[]
        self.D =[]
        self.H =[]
        self.S =[]
        self.Dp =[]
        self.Hp =[]
        self.Sp =[]
        self.C =[]
        self.PRANDTL=[]
        self.V =[]
        self.L =[]
        self.Cp =[]
        self.PRANDTLp=[]
        self.Vp =[]
        self.Lp =[]
        i = 1
        multi = 1
        if param == 'P':
            multi = pow(10, 3)
        start = float(start) * multi
        finish = float(finish) * multi
        step = float(step) * multi

        while start <= finish:
            self.T.append(digits(calculate("T", param, start, 'Q', 0, fluid)))
            self.P.append(digits(calculate("P", param, start, 'Q', 0, fluid,1000) , 1))
            self.D.append(digits(calculate("D", param, start, 'Q', 0, fluid,flag=1000),4))
            self.H.append(digits(calculate("H", param, start, 'Q', 0, fluid, 1000)))
            self.S.append(digits(calculate("S", param, start, 'Q', 0, fluid, 1000), 4))
            self.Dp.append(digits(calculate("D", param, start, 'Q', 1, fluid,flag=1), 4))
            self.Hp.append(digits(calculate("H", param, start, 'Q', 1, fluid, 1000)))
            self.Sp.append(digits(calculate("S", param, start, 'Q', 1, fluid, 1000), 4))
            self.C.append(digits(calculate("CVMASS", param, start, 'Q', 0, fluid), 4))
            self.PRANDTL.append(digits(calculate("PRANDTL", param, start, 'Q', 0, fluid)))
            self.V.append(digits(calculate("V", param, start, 'Q', 0, fluid,0.00001), 4))
            self.L.append(digits(calculate("L", param, start, 'Q', 0, fluid), 4))
            self.Cp.append(digits(calculate("CVMASS", param, start, 'Q', 1, fluid), 4))
            self.PRANDTLp.append(digits(calculate("PRANDTL", param, start, 'Q', 1, fluid)))
            self.Vp.append(digits(calculate("V", param, start, 'Q', 1, fluid,0.00001), 4))
            self.Lp.append(digits(calculate("L", param, start, 'Q', 1, fluid), 4))
            i += 1
            start += step
        #     для расчета перегретых паров calculate("P", param, start, const_param, const_param_value, fluid)
        self.graphPT = render_img(fluid, 'PH')


class BCalculatedDataForm(forms.Form):
    def __init__(self, fluid, param, start, finish, step, const_param_value, const_param):
        super().__init__()

        self.T_title = 'T, К'
        self.P_title = 'P, кПа'
        self.D_title = 'ʋ, м³/кг*10⁻³'
        self.H_title = 'h, кДж/кг'
        self.S_title = 's, кДж/кг/К'
        self.C_title = 'Cv, Дж/кг/К'
        self.PRANDTL_title= 'Pr'
        self.V_title = 'Ƞ, Па-с*10⁻⁵'
        self.L_title = 'λ, Вт/м/К'
        self.T=[]
        self.P =[]
        self.D =[]
        self.H =[]
        self.S =[]
        self.C =[]
        self.PRANDTL = []
        self.V =[]
        self.L =[]
        i = 1
        multi = 1
        if param == 'P':
            multi = pow(10, 3)
        start = float(start) * multi
        finish = float(finish) * multi
        step = float(step) * multi
        multi = 1
        if const_param == 'P':
            multi = pow(10, 3)
        const_param_value = float(const_param_value) * multi
        while start <= finish:
            self.T.append(digits(calculate("T", param, start, const_param, const_param_value, fluid)))
            self.P.append(digits(calculate("P", param, start, const_param, const_param_value, fluid,1000) , 1))
            self.D.append(digits(calculate("D", param, start, const_param, const_param_value, fluid,flag=1000), 4))
            self.H.append(digits(calculate("H", param, start, const_param, const_param_value, fluid, 1000)))
            self.S.append(digits(calculate("S", param, start, const_param, const_param_value, fluid, 1000), 4))
            self.C.append(digits(calculate("CVMASS", param, start, const_param, const_param_value, fluid), 4))
            self.PRANDTL.append(digits(calculate("PRANDTL", param, start, const_param, const_param_value, fluid)))
            self.V.append(digits(calculate("V", param, start, const_param, const_param_value, fluid,0.00001), 4))
            self.L.append(digits(calculate("L", param, start, const_param, const_param_value, fluid), 4))
            i += 1
            start += step
        # self.graphPT = render_img(fluid, 'PT')


fluidsRU = ['Вода','Воздух', 'Аммиак', 'Аргон', 'Диоксид углерода', 'Монооксид углерода', 'Циклогексан', 'Циклопентан',
            'Циклопропан', 'Этан', 'Этанол', 'Этилен', 'Фтор', 'Гелий', 'HFE143m', 'Водород', 'Хлороводород',
            'Сероводород', 'Изобутан', 'Изобутен', 'Изогексан', 'Изопентан', 'Криптон', 'Метан', 'Метанол', 'н-Бутан',
            'н-Декан', 'н-Додекан', 'н-Гептан', 'н-Гексан', 'н-Нонан', 'н-Октан', 'н-Пентан', 'н-Пропан', 'н-Ундекан',
            'Неон', 'Неопентан', 'Азот', 'Закись азота', 'Кислород', 'Пара-Водород', 'Пропилен', 'Пропин', 'R11',
            'R113', 'R114', 'R115', 'R116', 'R12', 'R123', 'R1233zd(E)', 'R1234yf', 'R1234ze(E)', 'R1234ze(Z)', 'R124',
            'R1243zf', 'R125', 'R13', 'R134a', 'R13I1', 'R14', 'R141b', 'R142b', 'R143a', 'R152A', 'R161', 'R21',
            'R218', 'R22', 'R227EA', 'R23', 'R236EA', 'R236FA', 'R245ca', 'R245fa', 'R32', 'R365MFC', 'R40', 'R404A',
            'R407C', 'R41', 'R410A', 'R507A', 'RC318', 'SES36', 'Диоксид серы', 'Гексафторид серы', 'Толуол',
            'Ксенон']
fluids = ['Water','Air', 'Ammonia', 'Argon', 'CarbonDioxide', 'CarbonMonoxide', 'CycloHexane', 'Cyclopentane', 'CycloPropane',
          'Ethane', 'Ethanol', 'Ethylene', 'Fluorine', 'Helium', 'HFE143m', 'Hydrogen', 'HydrogenChloride',
          'HydrogenSulfide', 'IsoButane', 'IsoButene', 'Isohexane', 'Isopentane', 'Krypton', 'Methane', 'Methanol',
          'n-Butane', 'n-Decane', 'n-Dodecane', 'n-Heptane', 'n-Hexane', 'n-Nonane', 'n-Octane',
          'n-Pentane', 'n-Propane', 'n-Undecane', 'Neon', 'Neopentane', 'Nitrogen', 'NitrousOxide', 'Oxygen',
          'ParaHydrogen', 'Propylene', 'Propyne', 'R11', 'R113', 'R114', 'R115', 'R116', 'R12', 'R123', 'R1233zd(E)',
          'R1234yf', 'R1234ze(E)', 'R1234ze(Z)', 'R124', 'R1243zf', 'R125', 'R13', 'R134a', 'R13I1',
          'R14', 'R141b', 'R142b', 'R143a', 'R152A', 'R161', 'R21', 'R218', 'R22', 'R227EA', 'R23', 'R236EA', 'R236FA',
          'R245ca', 'R245fa', 'R32', 'R365MFC', 'R40', 'R404A', 'R407C', 'R41', 'R410A', 'R507A', 'RC318', 'SES36',
          'SulfurDioxide', 'SulfurHexafluoride', 'Toluene',  'Xenon']


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
            minimum = round(CP.PropsSI('ptriple', fluid) / pow(10, 3), 2)
            maximum = round(CP.PropsSI('pcrit', fluid) / pow(10, 3), 2)

        self.fields['start'] = forms.FloatField(label='start value', min_value=minimum, max_value=maximum)
        self.fields['finish'] = forms.FloatField(label='finish value', min_value=minimum, max_value=maximum)
        self.fields['step'] = forms.FloatField(label='step value', min_value=0.001,
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
    def __init__(self, fluid, param, const_param):
        super().__init__()
        self.fields['fluid'] = forms.CharField(widget=forms.HiddenInput(), initial=fluid)
        self.fields['param'] = forms.CharField(widget=forms.HiddenInput(), initial=param)
        self.fields['const_param'] = forms.CharField(widget=forms.HiddenInput(), initial=const_param)
        self.fields['const_param_value'] = forms.FloatField(label='start value')
        self.fields['start'] = forms.FloatField(label='start value')
        self.fields['finish'] = forms.FloatField(label='finish value')
        self.fields['step'] = forms.FloatField(label='step value', min_value=0.001)

    def clean(self):
        cleaned_data = super().clean()
        start = cleaned_data.get("start")
        finish = cleaned_data.get("finish")
        if start > finish:
            raise ValidationError(
                "Начало не может быть больше конца"
            )
