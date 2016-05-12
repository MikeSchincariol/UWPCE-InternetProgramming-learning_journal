from wtforms import (
    Form,
    TextField,
    TextAreaField,
    IntegerField,
    FormField,
    validators,
)

from wtforms_components import read_only

strip_filter = lambda x: x.strip() if x else None

class EntryForm(Form):
    id = TextField(
        'Entry ID',
    )

    title = TextField(
        'Entry Title',
        [validators.Length(min=1, max=255)],
        filters=[strip_filter]
    )
    body = TextAreaField(
        'Entry Body',
        [validators.Length(min=1)],
        filters=[strip_filter]
    )

    def __init__(self, *args, **kwargs):
        super(EntryForm, self).__init__(*args, **kwargs)
        read_only(self.id)

class EntryCreateForm(EntryForm):
    pass


class EntryViewForm(EntryForm):
    def __init__(self, *args, **kwargs):
        super(EntryForm, self).__init__(*args, **kwargs)
        read_only(self.id)
        read_only(self.title)
        read_only(self.body)


class EntryEditForm(EntryForm):
    pass