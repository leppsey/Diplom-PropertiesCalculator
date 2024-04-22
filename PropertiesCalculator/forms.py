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
CHOICES1 = (("P", "Pressure [kPa]"), ("Q", "Quality [-]"), ("T", "Temperature [K]"), ("D", "Density [kg/m3]"),
            ("H", "Enthalpy [kJ/kg]"), ("S", "Entropy [kJ/kg/K]"),)
CHOICES2 = (("T", "Temperature [K]"), ("Q", "Quality [-]"), ("P", "Pressure [kPa]"), ("D", "Density [kg/m3]"),
            ("H", "Enthalpy [kJ/kg]"), ("S", "Entropy [kJ/kg/K]"),)


def calculate(name, input_name1, input_prop1, input_name2, input_prop2, fluid_name):
    try:
        return CP.PropsSI(name, input_name1, input_prop1, input_name2, input_prop2, fluid_name)
    except Exception as error:
        error = str(error)
        return error[:error.find(': Pro')]


def render_img(fluid,graph_type):
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
        self.T = calculate("T", input_name1, input_prop1, input_name2, input_prop2, fluid_name)
        self.P = calculate("P", input_name1, input_prop1, input_name2, input_prop2, fluid_name)
        self.D = calculate("D", input_name1, input_prop1, input_name2, input_prop2, fluid_name)
        # self.C0 = calculate("C0", input_name1, input_prop1, input_name2, input_prop2, fluid_name)
        self.C = calculate("C", input_name1, input_prop1, input_name2, input_prop2, fluid_name)
        self.O = calculate("O", input_name1, input_prop1, input_name2, input_prop2, fluid_name)
        self.U = calculate("U", input_name1, input_prop1, input_name2, input_prop2, fluid_name)
        self.H = calculate("H", input_name1, input_prop1, input_name2, input_prop2, fluid_name)
        self.S = calculate("S", input_name1, input_prop1, input_name2, input_prop2, fluid_name)
        self.A = calculate("A", input_name1, input_prop1, input_name2, input_prop2, fluid_name)
        self.G = calculate("G", input_name1, input_prop1, input_name2, input_prop2, fluid_name)
        self.V = calculate("V", input_name1, input_prop1, input_name2, input_prop2, fluid_name)
        self.L = calculate("L", input_name1, input_prop1, input_name2, input_prop2, fluid_name)
        self.I = calculate("I", input_name1, input_prop1, input_name2, input_prop2, fluid_name)
        # self.w = calculate("w", input_name1, input_prop1, input_name2, input_prop2, fluid_name)
        self.graphTS = render_img(fluid_name,'TS')
        self.graphPH = render_img(fluid_name, 'PH')
        self.graphHS = render_img(fluid_name, 'HS')
        self.graphPS = render_img(fluid_name, 'PS')
        self.graphPD = render_img(fluid_name, 'PD')
        self.graphTD = render_img(fluid_name, 'TD')
        self.graphPT = render_img(fluid_name, 'PT')


        # self.graph=MatplotlibFigureField(figure='figure')
        # print()


#         тут надо покумекать


class FullForm(forms.Form):
    temp = ()
    for fluid in sorted(CP.FluidsList()):
        temp = temp + ((fluid, fluid),)
    fluid_field = forms.ChoiceField(label='Fluids', choices=temp)
    choice_field1 = forms.ChoiceField(label='Parameter 1', choices=CHOICES1)
    value_field1 = forms.FloatField(label='Value 1', min_value=0)
    choice_field2 = forms.ChoiceField(label='Parameter 2', choices=CHOICES2)
    value_field2 = forms.FloatField(label='Value 2', min_value=0)
