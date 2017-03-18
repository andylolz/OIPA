from django.db import models
from iati.models import Activity


# class Network(models.Model):

# class NetworkLink(models.Model):

# class NetworkError(models.Model):

# class NetworkOrganisation(models.Model):


class Chain(models.Model):
    # chains have no name, we'll make it 
    name = models.CharField(max_length=255, blank=False)
    root_activity = models.ForeignKey(Activity, null=False)


class ChainLink(models.Model):
    direction_choices = (
        ('up', u"Upwards"),
        ('down', u"Downwards"),
        ('both', u"Both directions")
    )

    chain = models.ForeignKey(Chain, null=False)
    activity = models.ForeignKey(Activity, null=False)
    parent_activity = models.ForeignKey(Activity, null=True, related_name='chain_parent')
    direction = models.CharField(choices=direction_choices, max_length=4)


class ChainError(models.Model):
    level_choices = (
        ('warning', u"Warning"),
        ('error', u"Error")
    )

    chain = models.ForeignKey(Chain, null=False)
    # = the activity or link where the error occurs
    error_location = models.CharField(max_length=255, null=False)
    iati_element = models.CharField(max_length=255, null=False)
    message = models.CharField(max_length=255, null=False)
    # = warning, error 
    level = models.CharField(choices=level_choices, max_length=255, null=False)
