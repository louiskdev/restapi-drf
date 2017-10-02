# encoding: utf-8

from __future__ import unicode_literals

import json

from django.test import Client, TestCase

from rest_framework import status

from restapi.testspecs.CreateTestData import CreateTestData
from restapi.views.advertiser.AdvertiserDetail import AdvertiserDetail


class AdvertiserDetailSpecs(TestCase, CreateTestData):
    def setUp(self):
        self.client = Client()
        self.advertiser_detail = AdvertiserDetail

    def test__class_methods__exists(self):
        self.assert_(hasattr(self.advertiser_detail, 'queryset'))
        self.assert_(hasattr(self.advertiser_detail, 'get_queryset'))

    def test__advertiser_detail__not_provided_without_login(self):
        # arrange
        self._create_client()
        advertiser = self.create_advertiser(advertiser_name='test advertiser')

        # act
        response = self.client.get('/advertisers/{0}'.format(advertiser.advertiser_id))

        # assert
        result = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(result['HTTP-STATUS'], status.HTTP_403_FORBIDDEN)
        self.assertEqual(result['detail'], 'Authentication credentials were not provided.')

    def test__advertiser_detail__provided_with_login(self):
        # arrange
        self._create_client()
        advertiser = self.create_advertiser(advertiser_name='test advertiser')
        self.client.login(username='user@mng.com', password='password1')

        # act
        response = self.client.get('/advertisers/{0}'.format(advertiser.advertiser_id), follow=True)

        # assert
        result = json.loads(response.content)
        self.assertEqual(result['HTTP-STATUS'], status.HTTP_200_OK)
        self.assertEqual(result['advertiser'], 'test advertiser')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
