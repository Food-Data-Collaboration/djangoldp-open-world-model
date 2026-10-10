from djangoldp.views.ldp_viewset import LDPViewSet

from djangoldp_open_world_model.serializers import OpenWorldLDPSerializer


class OpenWorldLDPViewSet(LDPViewSet):
    serializer_class = OpenWorldLDPSerializer
