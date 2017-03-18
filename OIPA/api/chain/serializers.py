from rest_framework import serializers
from traceability import models as chain_models
from api.generics.serializers import DynamicFieldsModelSerializer
from iati.models import Activity


class SimpleActivitySerializer(serializers.ModelSerializer):

    class Meta:
        model = Activity
        fields = (
            'id',
            'iati_identifier',
        )


class ChainSerializer(DynamicFieldsModelSerializer):

    root_activity = SimpleActivitySerializer()
    links = serializers.HyperlinkedIdentityField(
        read_only=True,
        view_name='chains:chain-link-list',
        )
    errors = serializers.HyperlinkedIdentityField(
        read_only=True,
        view_name='chains:chain-error-list',
        )
    activities = serializers.HyperlinkedIdentityField(
        read_only=True,
        view_name='chains:chain-activity-list',
        )


    class Meta:
        model = chain_models.Chain
        fields = (
            'id',
            'root_activity',
            'links',
            'errors',
            'activities'
        )


class ChainLinkSerializer(DynamicFieldsModelSerializer):
    # chain = ChainSerializer()
    activity = SimpleActivitySerializer()
    parent_activity = SimpleActivitySerializer()

    class Meta:
        model = chain_models.ChainLink
        fields = (
            'id',
            'chain',
            'activity',
            'parent_activity',
            'direction'
        )


class ChainErrorSerializer(DynamicFieldsModelSerializer):
    # chain = ChainSerializer()

    class Meta:
        model = chain_models.ChainError
        fields = (
            'chain',
            'error_location',
            'iati_element',
            'message',
            'level'
        )
