import datetime

from django.db import models
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator
from osler.core.models import Patient, Encounter

from django.utils.translation import gettext_lazy as _


class LabType(models.Model):
    """
    type of lab panels
    e.g. BMP, A1c, CBC, etc.
    """
    name = models.CharField(max_length=30)
    order_index = models.PositiveIntegerField(
        default=0, blank=False, null=False, verbose_name=_("order index"))

    class Meta:
        ordering = ['order_index']

    def __str__(self):
        return self.name


class Lab(models.Model):
    """Model for a group of lab measurments.

    Stores a patient, timestamp, type, and encounter. Is pointed to by
    ForeignKey relationships from the Measurement object.
    """

    class Meta:
        ordering = ['-lab_time']

    encounter = models.ForeignKey(Encounter, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-lab_time']

    patient = models.ForeignKey(
        Patient, on_delete=models.CASCADE, verbose_name=_("patient"))

    lab_time = models.DateTimeField(
        default=timezone.now, verbose_name=_("lab time"))

    lab_type = models.ForeignKey(
        LabType, on_delete=models.PROTECT, verbose_name=_("lab type"))

    encounter = models.ForeignKey(Encounter, on_delete=models.CASCADE)

    def __str__(self):
        to_tz = timezone.get_default_timezone()
        str_time = self.lab_time.astimezone(to_tz).strftime("%B-%d-%Y, %H:%M")
        return '%s | %s | %s ' % (str(self.patient), str(self.lab_type), str_time)

    def get_day(self):
        to_tz = timezone.get_default_timezone()
        day = self.lab_time.astimezone(to_tz).date()
        return day


class MeasurementType(models.Model):
    """
    Abstract class: type of measurements with in a lab panel
    e.g. Na+, K+ in BMP, A1c in A1c, WBC in CBC, HIV, etc.
    """
    class Meta:
        ordering = ['order_index']
        abstract = True

    long_name = models.CharField(max_length=30, primary_key=True,
                                 help_text=_("A unique name of the measurement"))
    short_name = models.CharField(max_length=30)

    lab_type = models.ForeignKey(LabType, on_delete=models.PROTECT, verbose_name=_("lab type"))

    order_index = models.PositiveIntegerField(default=0, blank=False, null=False,
                                              verbose_name=_("order index"), help_text=_("Order at which this measurement will display"))

    def __lt__(self, other):
        return ((self.order_index) < (other.order_index))

    def __str__(self):
        return self.long_name


class ContinuousMeasurementType(MeasurementType):
    """
    type of measurements with a continuous value in a lab panel
    e.g. Na+, K+ in BMP, A1c in A1c, WBC in CBC, etc.
    """
    unit = models.CharField(max_length=15, blank=True, null=True)
    panic_upper = models.DecimalField(max_digits=7, decimal_places=3, blank=True, null=True,
                                      help_text=_("All labs above this value will display as red with a warning sign. Will also be used as the upper bound of reference."))
    panic_lower = models.DecimalField(max_digits=7, decimal_places=3, blank=True, null=True,
                                      help_text=_("All labs below this value will display as blue with a warning sign. Will also be used as the lower bound of reference."))
    display_decimals = models.SmallIntegerField(default=1, validators=[MinValueValidator(0), MaxValueValidator(3)])

    def get_ref(self):
        if (self.panic_lower == None and self.panic_upper == None):
            return ''
        else:
            lower_str = '' if (self.panic_lower is None) else (
                '{:7.{deci}f}'.format(self.panic_lower, deci=self.display_decimals))
            upper_str = '' if (self.panic_upper is None) else (
                '{:7.{deci}f}'.format(self.panic_upper, deci=self.display_decimals))
            unit_str = '' if (self.unit is None) else str(self.unit)
            return '[%s - %s %s]' % (lower_str, upper_str, unit_str)

    def get_unit(self):
        if self.unit:
            return self.unit
        else:
            return ''

    def get_value_type(self):
        return 'Continuous'


class DiscreteMeasurementType(MeasurementType):
    """
    type of measurements with a discrete value in a lab panel
    e.g. HIV, etc.
    """

    def get_ref(self):
        return ''

    def get_unit(self):
        return ''

    def get_value_type(self):
        return 'Discrete'


class Measurement(models.Model):
    """
    Abstract class: parent class of measurements
    """
    class Meta:
        abstract = True

    lab = models.ForeignKey(Lab, on_delete=models.CASCADE)


class ContinuousMeasurement(Measurement):
    """
    object of a continuous measurement
    """
    measurement_type = models.ForeignKey(ContinuousMeasurementType, on_delete=models.PROTECT)
    value = models.DecimalField(max_digits=7, decimal_places=3)

    def __str__(self):
        return '%s: %2g' % (self.measurement_type, self.value)

    def panic(self):
        """Returns True if the value is outside the reference range. Returns False if reference range doesn't exist"""
        panic_lower = self.measurement_type.panic_lower
        panic_upper = self.measurement_type.panic_upper
        if ((panic_lower != None) and (self.value < panic_lower)):
            return True
        elif((panic_upper != None) and (self.value > panic_upper)):
            return True
        return False

    def panic_low(self):
        """Returns true if the value is lower than the reference range. To display in a different color than normal panic."""
        panic_lower = self.measurement_type.panic_lower
        if ((panic_lower != None) and (self.value < panic_lower)):
            return True
        return False

    def get_value(self):
        """Returns the value of the measurement"""
        decimal = self.measurement_type.display_decimals
        return '{:7.{deci}f}'.format(self.value, deci=decimal)


class DiscreteResultType(models.Model):
    """
    type of discrete results
    e.g. Positive, Negative, Trace, etc.
    """
    name = models.CharField(max_length=30, primary_key=True)
    measurement_type = models.ManyToManyField(DiscreteMeasurementType)
    PANIC_CHOICES = (
        ('T', 'Abnormal value'),
        ('F', 'Normal value')
    )
    is_panic = models.CharField(max_length=1, choices=PANIC_CHOICES,
                                default='T',
                                help_text=_("If abnormal, all labs with this value will display as red with a warning sign."))

    def __str__(self):
        return self.name


class DiscreteMeasurement(Measurement):
    """Model representing a discrete measurement.
    """
    measurement_type = models.ForeignKey(
        DiscreteMeasurementType, on_delete=models.PROTECT)
    value = models.ForeignKey(DiscreteResultType, on_delete=models.PROTECT)

    def __str__(self):
        value_name = DiscreteResultType.objects.get(pk=self.value)
        return '%s: %s' % (self.measurement_type, value_name.name)

    def panic(self):
        """Returns True if the value is not normal"""
        if self.value.is_panic == 'T':
            return True
        return False

    def panic_low(self):
        """Panic because the value is too low. 
        To display in a different color than normal panic."""
        return False

    def get_value(self):
        """Returns the value of the measurement"""
        return self.value
