from __future__ import unicode_literals

from django.db import models

from .extras import TimeStampedModel


class DocumentTemplate(TimeStampedModel):

    STUDENT_REF = 'student'
    ENROLLMENT_REF = 'enrollment'

    REFERENCE_TYPES = (
        (STUDENT_REF, 'student'),
        (ENROLLMENT_REF, 'Enrollment')
    )

    # TODO add presets as needed here

    COMPANY_NAME = 'company_name'
    INSUREE_NAME = 'insuree_name'
    POLICY_NAME = 'policy_name'

    PRESET_FIELDS = (
        (COMPANY_NAME, 'Company Name'),
        (INSUREE_NAME, 'Insuree Name'),
        (POLICY_NAME, 'Policy Name')
    )

    company = models.ForeignKey(
        'Company', on_delete=models.CASCADE, related_name='templates',
        null=True, blank=True)
    name = models.CharField(max_length=64, null=True, blank=True, unique=True)
    reference = models.CharField(
        max_length=10, choices=REFERENCE_TYPES, default=ENROLLMENT_REF)
    _preset_fields = models.TextField(
        null=True, blank=True, verbose_name='Preset Fields')
    template_id = models.CharField(max_length=32, null=True, blank=True)

    @property
    def preset_fields(self):
        return self._preset_fields.split('|')

    @preset_fields.setter
    def preset_fields(self, data):
        self._preset_fields = '|'.join(data)

    def save(self, *args, **kwargs):
        new = self.pk is None
        create_template = False
        # Call create template API if template is new
        super().save(*args, **kwargs)
        if new:
            self.create_template()
            self.save()

