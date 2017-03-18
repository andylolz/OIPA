from django_filters import FilterSet
from django_filters import NumberFilter

from api.generics.filters import CommaSeparatedCharFilter

from traceability.models import Chain, ChainLink, ChainError



class ChainFilter(FilterSet):
    root_activity = CommaSeparatedCharFilter(name='root_activity__iati_identifier', lookup_type='in')

    class Meta:
        model = Chain
        fields = ['root_activity']


class ChainLinkFilter(FilterSet):

    chain = NumberFilter(name='chain__id')
    root_activity = CommaSeparatedCharFilter(name='chain__root_activity__iati_identifier', lookup_type='in')

    class Meta:
        model = ChainLink
        fields = ['chain', 'root_activity']


class ChainErrorFilter(FilterSet):
    chain = NumberFilter(name='chain__id')
    root_activity = CommaSeparatedCharFilter(name='chain__root_activity__iati_identifier', lookup_type='in')

    class Meta:
        model = ChainError
        fields = ['chain', 'root_activity']