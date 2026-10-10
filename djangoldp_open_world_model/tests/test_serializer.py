from django.conf import settings
from django.test import TestCase

from djangoldp_open_world_model.serializers import OpenWorldLDPSerializer
from djangoldp_open_world_model.tests.models import Organization


class OpenWorldLDPSerializerTestCase(TestCase):
    def _get_serializer_class(self, model, depth, fields):
        try:
            serializer_class = model.serializer_class()
        except AttributeError:
            serializer_class = OpenWorldLDPSerializer

        # NOTE: LDPSerializer cannot be used without meta args:
        #   https://git.startinblox.com/djangoldp-packages/djangoldp/-/issues/277
        meta_args = {
            "model": model,
            "depth": depth,
            "fields": fields,
        }
        meta_class = type("Meta", (), meta_args)
        return type(serializer_class)(
            serializer_class.__class__.__name__,
            (serializer_class,),
            {"Meta": meta_class},
        )

    def test_additional_field_serialization(self):
        # Pass a serializer data which is not known to the model.
        org = Organization.objects.create(name="job test")
        post = {
            "@id": f"{settings.BASE_URL}/organizations/{org.pk}/",
            "name": "Organization Name",
            "someUnknownField": "Additional data, unknown to the model definition",
        }
        serializer_class = self._get_serializer_class(
            Organization, 1, ("@id", "name", "additional")
        )
        serializer = serializer_class(data=post, instance=org)
        serializer.is_valid(raise_exception=True)
        result = serializer.save()

        # The unknown field should be stored on the saved instance.
        self.assertEqual(result.name, post["name"])
        self.assertEqual(
            result.additional, {"someUnknownField": post["someUnknownField"]}
        )
