class ItemAssemblier:
    def __init__(self):
        self.item = {
            'value': {}
            'meta': {}
        }

    def create_fields(self, item):
        for field_name in item.fields:
            field = item.fields[field_name]
            if field.get('auto_translate'):
                self.item['meta'][field_name] = field
            

    def set_field(self, field_name, field_value):
        pass

    def append_field(self, field_name, append_value):
        pass

    def is_finished(self):
        pass

    @property
    def item(self):
        return self._item

    @item.setter
    def item(self, v):
        self._item = v
        
