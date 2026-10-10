from djangoldp import fields
from djangoldp.models import Model


class OpenWorldModel(Model):
    # A JSONField which is used for serializer tricks: include in serializer_fields of your model to store data which
    # was not anticipated in the definition (open world assumption).
    # Data included here will then be serialized out without being nested under an "additional" key, i.e. as a direct attribute.
    additional = fields.JSONField(
        null=True,
        blank=True,
        help_text="DjangoLDP will serialize any data included here as though they are part of the instance, omitting the additional field",
    )

    class Meta(Model.Meta):
        abstract = True

    @classmethod
    @property
    def view_set(cls):
        from djangoldp_open_world_model.views import OpenWorldLDPViewSet

        return OpenWorldLDPViewSet
