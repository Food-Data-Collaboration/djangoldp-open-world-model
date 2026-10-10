import json

from rest_framework.test import APIClient, APIRequestFactory, APITestCase

from djangoldp_open_world_model.tests.models import Organization


class PostViewTestCase(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.client = APIClient()

    def test_post_additional_field(self):
        """
        LDPSerializer can save additional data (that which is missing from the model definition),
        if serializing the field Model.additional
        """
        # Organization is serializing "additional"
        body = {"dfc-b:name": "Test", "dfc-b:UnknownField": "value"}
        response = self.client.post(
            "/organizations/", data=json.dumps(body), content_type="application/ld+json"
        )
        self.assertEqual(response.status_code, 201)
        org = Organization.objects.get()  # Also asserts count == 1
        self.assertEqual(org.name, body["dfc-b:name"])
        self.assertEqual(org.additional["dfc-b:UnknownField"], "value")
