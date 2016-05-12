from pyramid.response import Response
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPNotFound
from pyramid.httpexceptions import HTTPFound
from .forms import (
    EntryCreateForm,
    EntryViewForm,
    EntryEditForm
    )

import transaction

from sqlalchemy.exc import DBAPIError

from .models import (
    DBSession,
    MyModel,
    Entry,
    )


# @view_config(route_name='home', renderer='templates/mytemplate.pt')
# def my_view(request):
#     try:
#         one = DBSession.query(MyModel).filter(MyModel.name == 'one').first()
#     except DBAPIError:
#         return Response(conn_err_msg, content_type='text/plain', status_int=500)
#     return {'one': one, 'project': 'learning_journal'}

@view_config(route_name='home', renderer='templates/list.jinja2')
def index_page(request):
    entries = Entry.all()
    return {'entries': entries}


@view_config(route_name='detail', renderer='templates/view.jinja2')
# and update this view function:
def view(request):
    this_id = request.matchdict.get('id', -1)
    entry = Entry.by_id(this_id)
    if not entry:
        return HTTPNotFound()
    form = EntryViewForm(formdata=None, obj=entry)
    return {'form': form}


@view_config(route_name='action', match_param='action=create', renderer='templates/edit.jinja2')
def create(request):
    form = EntryCreateForm(request.POST)
    if request.method == 'POST' and form.validate():
        # If an ID not empty on a POST, then edits to an existing entry
        # are being submittied. Otherwise, we are createing a brand
        # new entry.
        if request.POST['id'] != "":
            entry = Entry.by_id(request.POST['id'], DBSession)
        else:
            entry = Entry()
        entry.title = form.title.data
        entry.body = form.body.data
        with transaction.manager:
            DBSession.add(entry)
        return HTTPFound(location=request.route_url('home'))

    else:
        # Must be a GET request to show a new, empty, create form.
        return {'form': form, 'action': request.matchdict.get('action')}


@view_config(route_name='action', match_param='action=edit', renderer='templates/edit.jinja2')
def update(request):
    entry = Entry.by_id(request.POST['id'], DBSession)
    form = EntryEditForm(request.POST)
    return {'form': form, 'action': request.matchdict.get('action')}


conn_err_msg = """\
Pyramid is having a problem using your SQL database.  The problem
might be caused by one of the following things:

1.  You may need to run the "initialize_learning_journal_db" script
    to initialize your database tables.  Check your virtual
    environment's "bin" directory for this script and try to run it.

2.  Your database server may not be running.  Check that the
    database server referred to by the "sqlalchemy.url" setting in
    your "development.ini" file is running.

After you fix the problem, please restart the Pyramid application to
try it again.
"""

