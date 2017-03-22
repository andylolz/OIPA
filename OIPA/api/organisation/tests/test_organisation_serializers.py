from django.test import TestCase
import pytest
from django.test import RequestFactory
from api.organisation import serializers
from iati.factory import iati_factory


# class TestCountrySerializers(TestCase):
#     request_dummy = RequestFactory().get('/')

#     @pytest.mark.django_db
#     def test_OrganisationSerializer(self):
#         organisation = iati_factory.OrganisationFactory.build(
#             code=' some code',
#             abbreviation='sc',
#             original_ref=' some code')

#         serializer = serializers.OrganisationSerializer(
#             organisation,
#             context={'request': self.request_dummy})

#         assert serializer.data['code'] == organisation.code,\
#             """
#             'organisation.code' should be serialized to a field called 'code'
#             """
#         assert serializer.data['abbreviation'] == organisation.abbreviation,\
#             """
#             'organisation.abbreviation' should be serialized to a field called
#             'abbreviation'
#             """
#         assert serializer.data['original_ref'] == organisation.original_ref,\
#             """
#             'organisation.original_ref' should be serialized to a field called
#             'original_ref'
#             """

#         required_fields = (
#             'url',
#             'name',
#             'reported_activities',
#             'participated_activities',
#             'provided_transactions',
#             'received_transactions',
#         )

#         msg = "the field '{0}' should be in the serialized organisation"
#         for field in required_fields:
#             assert field in serializer.data, msg.format(field)

#     def test_OrganisationDifficultNameSerializer(self):
#         difficult_name = u'"Campa\xc3\x83\xc6\x92\xc3\x82\xc2\xb1aGlobalporlaLibertaddeExpresi\xc3\x83\xc6\x92\xc3\x82\xc2\xb3nA19",Asociaci\xc3\x83\xc6\x92\xc3\x82\xc2\xb3nCivil'
#         organisation = iati_factory.OrganisationFactory.build(
#             code=difficult_name,
#             abbreviation='sc',
#             original_ref=' some code')
#         try:
#             serializer = serializers.OrganisationSerializer(
#                 organisation,
#                 context={'request': self.request_dummy})
#             serializer.data['reported_activities']
#         except Exception as e:
#             assert e is None, e

#     def test_OrganisationTypeSerializer(self):
#         type = iati_factory.OrganisationTypeFactory.build(
#             code=10,
#             name='Government'
#         )
#         serializer = serializers.OrganisationSerializer.TypeSerializer(type)
#         assert serializer.data['code'] == type.code,\
#             """
#             'organisation_type.code' should be serialized to a field called
#             'code'
#             """

#     def test_OrganisationNameSerializer(self):
#         name = 'some name'
#         serializer = serializers.OrganisationSerializer.NameSerializer(name)
#         assert serializer.data['narratives'][0]['text'] == name,\
#             """
#             'organisation.name' should be serialized to a field called 'name'
#             """
