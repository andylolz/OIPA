from django.core.urlresolvers import reverse

from rest_framework import status
from rest_framework.test import APITestCase
from iati_synchroniser.factory import synchroniser_factory


class TestDatasetEndpoints(APITestCase):

    def test_datasets_endpoint(self):
        url = reverse('datasets:dataset-list')

        msg = 'datasets endpoint should be localed at {0}'
        expect_url = '/api/datasets/'
        assert url == expect_url, msg.format(expect_url)
        response = self.client.get(url)
        self.assertTrue(status.is_success(response.status_code))

    def test_dataset_detail_endpoint(self):
        synchroniser_factory.DatasetFactory.create(id=1)
        url = reverse('datasets:dataset-detail', args={1})

        msg = 'dataset detail endpoint should be localed at {0}'
        expect_url = '/api/datasets/1/'
        assert url == expect_url, msg.format(expect_url)
        response = self.client.get(url)
        self.assertTrue(status.is_success(response.status_code))

