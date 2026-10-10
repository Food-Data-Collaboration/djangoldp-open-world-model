from django.contrib.auth.models import AbstractUser
from djangoldp import fields
from djangoldp.models import Model
from djangoldp.permissions import OwnerPermissions, ReadAndCreate

from djangoldp_open_world_model.models import OpenWorldModel


class User(AbstractUser, Model):
    class Meta(AbstractUser.Meta, Model.Meta):
        depth = 0
        empty_containers = []
        ordering = ["pk"]
        serializer_fields = ["@id", "username", "first_name", "last_name", "email"]
        permission_classes = [ReadAndCreate | OwnerPermissions]
        rdf_type = "foaf:user"
        nested_fields = []


class Organization(OpenWorldModel):
    name = fields.TextField(rdf_type="dfc-b:name", blank=True, null=True)

    class Meta(OpenWorldModel.Meta):
        rdf_type = "dfc-b:Organization"
        serializer_fields = ["@id", "additional", "name"]
