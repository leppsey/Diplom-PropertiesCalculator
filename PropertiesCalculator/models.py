from django.db import models

# Create your models here
class ParamModel(models.Model):
    def __init__(self,param,fluid):
        self.start_value = models.FloatField()
        self.end_value = models.FloatField()
        self.step_value = models.FloatField(help_text="Шаг")
        if param == 'T':
            self.start_value.default_validators