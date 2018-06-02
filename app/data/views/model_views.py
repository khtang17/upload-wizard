from flask_user import current_user
from flask import url_for, redirect, request, abort
from flask_admin.contrib import sqla
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


class UserView(AdminModelView):
    column_list = ['active', 'username', 'short_name', 'roles', 'email', 'confirmed_at', 'company']
    form_columns = ('active', 'roles', 'username', 'short_name', 'email', 'company')
    column_searchable_list = ('username', 'email')
    column_editable_list = ('active', 'email', 'company')
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


class CompanyView(AdminModelView):
    column_list = ['logo', 'name', 'telephone_number', 'toll_free_number',
                   'sales_email', 'idnumber', 'cmpdname',	'cas', 'price']
    form_excluded_columns = ('users', 'logo')
    page_size = 20

    column_formatters = {
        'logo': _list_thumbnail
    }


class HistoryView(AdminModelView):
    column_default_sort = ('date_uploaded', True)
    column_list = ['date', 'user', 'file_name', 'type', 'purchasability',
                   'natural_products', 'file_size', 'status', 'file_size']
    column_searchable_list = ('file_name', 'type', 'purchasability')
    column_editable_list = ('status',)
    can_create = False
    page_size = 20

    column_formatters = {
        'date': _date_format
    }


class FieldView(AdminModelView):
    form_excluded_columns = ('field_decimal', 'field_allowed_value')
