# DjangoLDP-Open-World-Model

This package extends DjangoLDP's Model base class to support storing and serving field data which is not a part of the subclass model's specification (known as the open world assumption of RDF).

# How to use

After adding the package to your `settings.yml`, extend your models from the base class provided by this package, and make sure to also extend your model's `Meta` from the base class:

```python
class MyModel(OpenWorldModel):
    class Meta(OpenWorldModel.Meta):
        pass
```

If you have set `serializer_fields` on your model, you will need to make sure that the field `"additional"` is among them.

If, for example, you receive `{"someUnknownField": "value"}` with your POST data, it will be serialized in the object like so:

```json
{
    "@id": "https://...",
    "someUnknownField": "value"
}
```

i.e., the field `"additional"` will not appear as a sub-object of the JSON-LD.

# Security

POSTing to a model with this behaviour enabled implies being able to inject any arbitrary data into the objects which your server will then serve. Please take care to set appropriate permissions and restrictions around this power and be cautious about the context in which you are using this package.
