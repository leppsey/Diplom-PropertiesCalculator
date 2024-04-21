from django import forms
import CoolProp.CoolProp as CP


class FluidForm(forms.Form):
    fluids = CP.FluidsList()
    CHOICES = ()
    for t in fluids:
        CHOICES = CHOICES + ((t, t),)
    field = forms.ChoiceField(label='Fluids', choices=CHOICES)


# тут я даун не понимаю почему я не могу вытянуть после иницавлизации поля
# class FluidForm(forms.Form):
#     def __init__(self, fluids=None):
#         super().__init__()
#         if fluids is None:
#             fluids = []
#         self.CHOICES = ()
#         for t in range(len(fluids)):
#             self.CHOICES = self.CHOICES + ((t, fluids[t]),)
#         self.field = forms.ChoiceField(choices=self.CHOICES)
# CHOICES = (("Q", "Quality [-]"), ("T", "Temperature [K]"), ("P", "Pressure [kPa]"), ("D", "Density [kg/m3]"),
#     ("C0", "Ideal-gas specific heat at constant pressure [kJ/kg/K]"),
#     ("C", "Specific heat at constant pressure [kJ/kg/K]"), ("O", "Specific heat at constant volume [kJ/kg/K]"),
#     ("U", "Internal energy [kJ/kg]"), ("H", "Enthalpy [kJ/kg]"), ("S", "Entropy [kJ/kg/K]"),
#     ("A", "Speed of sound [m/s]"), ("G", "Gibbs function [kJ/kg]"), ("V", "Dynamic viscosity [Pa-s]"),
#     ("L", "Thermal conductivity [kW/m/K]"), ("I", "Surface Tension [N/m]"), ("w", "Accentric Factor [-]"))
CHOICES = (("Q", "Quality [-]"), ("T", "Temperature [K]"), ("P", "Pressure [kPa]"), ("D", "Density [kg/m3]"),
    ("H", "Enthalpy [kJ/kg]"), ("S", "Entropy [kJ/kg/K]"),)

class Parameter1Form(forms.Form):

    field1 = forms.ChoiceField(label='Parameter', choices=CHOICES)

class Parameter2Form(forms.Form):

    field2 = forms.ChoiceField(label='Parameter', choices=CHOICES)
