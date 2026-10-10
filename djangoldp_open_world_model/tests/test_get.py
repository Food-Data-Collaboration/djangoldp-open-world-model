from rest_framework.test import APIClient, APIRequestFactory, APITestCase

from djangoldp_open_world_model.tests.models import Organization


class GetViewTestCase(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.client = APIClient()

    def test_get_additional_fields(self):
        """
        LDPSerializer can serve additional data (that which is missing from the model definition),
        if serializing the field Model.additional
        """
        org = Organization.objects.create(
            name="FDC", additional={"withoutRdf": "test", "dfc-b:withRdf": "Test"}
        )
        response = self.client.get(
            "/organizations/", content_type="application/ld+json"
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["ldp:contains"]), 1)
        serialized_org = response.data["ldp:contains"][0]
        self.assertEqual(serialized_org["dfc-b:name"], org.name)
        self.assertEqual(serialized_org["withoutRdf"], "test")
        self.assertEqual(serialized_org["dfc-b:withRdf"], "Test")
        self.assertNotIn("additional", serialized_org)

        response = self.client.get(
            f"/organizations/{org.pk}/", content_type="application/ld+json"
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["dfc-b:name"], org.name)
        self.assertEqual(response.data["withoutRdf"], "test")
        self.assertEqual(response.data["dfc-b:withRdf"], "Test")
        self.assertNotIn("additional", response.data)
