import json

class JsonMixin:
    __abstract__ = True

    def convert_to_python_object(self, relationship=True):
        if relationship is False:
            dumps_string = self.get_model_attr_without_relations()
            return json.dumps(dumps_string)
        dumps_string = self.get_model_attr_with_relations()
        for key, value in dumps_string.items():
            try:
                if isinstance(value, list):
                    dumps_string[key]: list = []
                    for model_object in value:
                        dumps_string[key].append(model_object.get_model_attr_without_relations())
                elif not isinstance(value, (int, float, bool, str)):
                    dumps_string[key] = value.get_model_attr_without_relations()
            except:
                pass
        return dumps_string

    def dumps_to_json(self, relationship=True):
        return json.dumps(self.convert_to_python_object(relationship=relationship))