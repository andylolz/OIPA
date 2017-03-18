from rest_framework.filters import DjangoFilterBackend

from api.generics.views import DynamicListView, DynamicDetailView
from api.aggregation.views import AggregationView, Aggregation, GroupBy
from django.db.models import Sum

from api.chain.filters import ChainFilter, ChainLinkFilter, ChainErrorFilter
from api.chain.serializers import ChainSerializer, ChainLinkSerializer, ChainErrorSerializer
from traceability.models import Chain, ChainLink, ChainError


from rest_framework import filters

from api.activity.views import ActivityList
from iati.models import Activity

# class ChainAggregations(AggregationView):
#     """
#     Returns aggregations based on the item grouped by, and the selected aggregation.

#     ## Group by options

#     API request has to include `group_by` parameter.
    
#     This parameter controls result aggregations and
#     can be one or more (comma separated values) of:

#     - `chain`
#     - `tier`
#     - `reporting_org`

#     ## Aggregation options

#     API request has to include `aggregations` parameter.
    
#     This parameter controls result aggregations and
#     can be one or more (comma separated values) of:

#     - `activity_count`
#     - `link_count`

#     ## Request parameters

#     All filters available on the Indicator List, can be used on aggregations.

#     """

#     queryset = IndicatorData.objects.all()
#     filter_backends = (DjangoFilterBackend, )
#     filter_class = IndicatorDataFilter

#     allowed_aggregations = (
#         Aggregation(
#             query_param='value',
#             field='value',
#             annotate=Sum('value'),
#         ),
#     )

#     allowed_groupings = (
        
#         GroupBy(
#             query_param="name",
#             fields=("name",)
#         ),
#         # GroupBy(
#         #     query_param="country",
#         #     fields="country",
#         #     queryset=Country.objects.all(),
#         #     serializer=CountrySerializer,
#         #     serializer_main_field='id',
#         #     serializer_fields=('id', 'name'),
#         # ),
#     )






# class ChainError(models.Model):

class ChainList(DynamicListView):
    """
    Returns a list of chains.

    ## Aggregations

    The /chains/aggregations endpoint can be used for chain based aggregations.

    ## Result details

    Each item contains all information on the chain link being shown.

    """

    queryset = Chain.objects.all()
    filter_backends = (DjangoFilterBackend, )
    filter_class = ChainFilter
    serializer_class = ChainSerializer

    fields = (
        'id',
        'root_activity'
    )


class ChainDetail(DynamicDetailView):
    """
    Returns subpages of chains
    """
    queryset = Chain.objects.all()
    serializer_class = ChainSerializer

    fields = (
        'id',
        'root_activity',
        'links',
        'errors',
        'activities'
    )


# TODO : put this under the right URL structure (per chain)
class ChainLinkList(DynamicListView):
    """
    Returns a list of chain links.

    ## Request parameters
    - `chain` (*optional*): Comma separated list of chain names.
    - `tier` (*optional*): Comma separated list of tiers the link is in.

    ## Aggregations

    The /chains/aggregations endpoint can be used for chain based aggregations.

    ## Result details

    Each item contains all information on the chain link being shown.

    """

    queryset = ChainLink.objects.all()
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    filter_class = ChainLinkFilter
    serializer_class = ChainLinkSerializer
    pagination_class = None

    ordering_fields = (
        'id',
    )
    fields = (
        'id',
        'activity',
        'parent_activity',
        'direction',)

    def get_queryset(self):
        pk = self.kwargs.get('pk')
        return ChainLink.objects.filter(chain=Chain.objects.get(pk=pk))


class ChainErrorList(DynamicListView):
    """
    Returns a list of chain errors.
    """

    queryset = ChainError.objects.all()
    filter_backends = (DjangoFilterBackend, )
    filter_class = ChainErrorFilter
    serializer_class = ChainErrorSerializer
    pagination_class = None

    fields = (
        'error_location',
        'iati_element',
        'message',
        'level')

    def get_queryset(self):
        pk = self.kwargs.get('pk')
        return ChainError.objects.filter(chain=Chain.objects.get(pk=pk))


class ChainActivities(ActivityList):
    """
    Returns a list of activities
    """

    def get_queryset(self):
        pk = self.kwargs.get('pk')
        return Activity.objects.filter(id__in=Activity.objects.filter(chainlink__chain=pk))



