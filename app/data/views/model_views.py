from flask_user import current_user
from flask import url_for, redirect, request, abort
from flask_admin.contrib import sqla
from flask_admin import AdminIndexView, expose, BaseView
from flask import Markup
from datetime import timezone


class AdminModelView(sqla.ModelView):

    def is_accessible(self):
        if not current_user.is_active or not current_user.is_authenticated:
            return False

        if current_user.has_role('Admin'):
            return True

        return False

    def _handle_view(self, name, **kwargs):
        """
        Override builtin _handle_view in order to redirect users when a view is not accessible.
        """
        if not self.is_accessible():
            if current_user.is_authenticated:
                # permission denied
                abort(403)
            else:
                # login
                return redirect(url_for('user.login', next=request.url))


class MyHomeView(AdminIndexView):
    @expose('/')
    def index(self):
        if not current_user.is_active or not current_user.is_authenticated:
            return redirect(url_for('user.login'))
        else:
            if current_user.has_role('Admin'):
                return self.render('admin/myhome.html')
            else:
                return self.render('errors/404.html'), 404

    # @expose('/result', methods=['GET'])
    # def result(self):
    #     from app.data.models.history import UploadHistoryModel
    #     id = request.args.get('id', type=int)
    #     history = UploadHistoryModel.find_by_id(id)
    #     return self.render('admin/result.html', history=history)


class UserView(AdminModelView):
    column_list = ['active', 'username', 'short_name', 'roles', 'email', 'confirmed_at', 'company']
    form_columns = ('active', 'roles', 'username', 'short_name', 'email', 'company')
    column_searchable_list = ('username', 'email')
    column_editable_list = ('active', 'email', 'company')
    page_size = 20

class CatalogResult(AdminModelView):
    column_list = ['history_id', 'size','filtered', 'errors']
    page_size = 20

class RoleView(AdminModelView):
    column_list = ['name', 'description']
    form_columns = ('name', 'description')
    can_create = False
    can_delete = False
    page_size = 20


def _list_thumbnail(view, context, model, name):
    if not model.logo:
        return ''

    return Markup(
        '<img src="{model.url}" style="height: 40px;">'.format(model=model)
    )


def utc_to_local(utc_dt):
    return utc_dt.replace(tzinfo=timezone.utc).astimezone(tz=None)


def _date_format(view, context, model, name):
    if not model.date_uploaded:
        return ''

    return utc_to_local(model.date_uploaded).strftime("%b %d %Y %H:%M")

def _file_name_link(view, context, model, name):
    if not model.file_name:
        return ''

    return Markup(
        '<a href="/result?id={model.id}">{model.file_name}</a>'.format(model=model)
    )

class CompanyView(AdminModelView):
    column_list = ['logo', 'name', 'telephone_number', 'toll_free_number',
                   'sales_email', 'idnumber', 'cmpdname',	'cas', 'price']
    form_excluded_columns = ( 'logo')
    page_size = 20

    column_formatters = {
        'logo': _list_thumbnail
    }


class HistoryView(AdminModelView):
    column_default_sort = ('date_uploaded', True)
    column_list = ['date_uploaded', 'file_name', 'catalog_type', 'upload_type', 'availability',
                   'file_size', 'status_id']
    form_columns = ['date_uploaded','file_name', 'catalog_type', 'upload_type', 'availability',
                   'file_size', 'status_id']
    column_searchable_list = ('file_name', 'upload_type', 'availability')
    column_editable_list = ['status_id']
    can_create = False
    page_size = 20

    column_formatters = {
        'date': _date_format,
        'file_name': _file_name_link
    }
    # form_widget_args = {
    #     'job_logs': {
    #         'readonly': True
    #     },
    # }
    can_edit = True

# class HistoryView(AdminModelView):
#     column_default_sort = ('date_uploaded', True)
#     column_list = ['date', 'user', 'file_name', 'catalog_type', 'file_size']
#     column_searchable_list = ('file_name', 'catalog_type')
#     column_editable_list = ('status_id',)
#     can_create = False
#     page_size = 20
#
#     column_formatters = {
#         'date': _date_format,
#         'file_name': _file_name_link
#     }


class CatalogStatusView(AdminModelView):
    column_default_sort = ('status_id')
    column_list = ['status_id', 'status']
    can_create = True
    column_editable_list = ['status']
    can_delete = False
    can_edit = True


class FieldView(AdminModelView):
    # form_excluded_columns = ('field_decimal', 'field_allowed_value')
    column_list = ['order', 'field_name', 'mandatory']
    column_default_sort = ('order', False)
    can_create = False
    can_delete = False
