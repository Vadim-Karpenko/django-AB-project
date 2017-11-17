from django.db import models

class TrafficDivider(models.Model):
    page_title = models.CharField(max_length=100)
    divider = models.BooleanField(default=True)

    def __str__(self):
        return self.page_title

class Experiment(models.Model):
    divider = models.ForeignKey(TrafficDivider, null=True, related_name='traffic_divider')
    page_title = models.CharField(max_length=100)
    entered = models.PositiveIntegerField(default=0, help_text='How much users was entered to this page')
    success = models.PositiveIntegerField(default=0, help_text='How much users was successfully go to the next page')
    сonversion = models.FloatField('Conversion(%)', default=0)
    alternative_entered = models.PositiveIntegerField('Entered', default=0, help_text='How much users was entered to this page')
    alternative_success = models.PositiveIntegerField('Success', default=0, help_text='How much users was successfully go to the next page')
    alternative_сonversion = models.FloatField('Conversion(%)', default=0)
    is_editable = models.BooleanField(default=False, help_text='If you want edit this experiment, just enable this checkbox and save. Only if necessary!')
    is_active = models.BooleanField(default=True, help_text='Do you want to run this experiment?')

    def __str__(self):
        return self.page_title

    def save(self, *args, **kwargs):
        # if 'entered' and 'succes' not equal zero
        if self.entered != 0 and self.success != 0:
            # get conversion by formula (succes / entered)*100, than round number to more readable
            self.сonversion = round(((self.success / self.entered) * 100), 2)
        # if antered and succes == 0, set conversion to zero
        else:
            self.сonversion = 0

        # if 'entered' and 'succes' not equal zero
        if self.alternative_entered != 0 and self.alternative_success != 0:
            # get conversion by formula (succes / entered)*100, than round number to more readable
            self.alternative_сonversion = round(((self.alternative_success / self.alternative_entered) * 100), 2)
        # if antered and succes == 0, set conversion to zero
        else:
            self.alternative_сonversion = 0
        super(Experiment, self).save(*args, **kwargs)
