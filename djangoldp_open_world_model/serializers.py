from djangoldp.serializers.model_serializer import LDPSerializer


class OpenWorldLDPSerializer(LDPSerializer):
    store_jsonld_terms = False

    def serialize_additional_fields(self, obj, data):
        """
        Serializes additional fields, not configured on the model. By default leverages the "additional" field on Model.
        :param obj: the instance serialized.
        :param data: the serialized data
            NOTE that at this time it will contain serialized data, from to_representation
        """
        if getattr(obj, "additional", None) is not None:
            for key in obj.additional:
                if key in data:
                    continue  # The "additional" field is not a means of overriding values.
                data[key] = obj.additional[key]
            data.pop("additional")
        return data

    def to_internal_value_pre_process_data(self, data):
        super().to_internal_value_pre_process_data(data)

        # the OpenWorldModel field "additional", which is used for storing/serializing unforeseen fields.
        additional_fields = set(data.keys()).difference({*self.fields})
        if not self.store_jsonld_terms:
            # NOTE: the assumption is made that only JSON-LD is using "@".
            additional_fields = {f for f in additional_fields if not f.startswith("@")}
        data["additional"] = {k: data[k] for k in additional_fields}
