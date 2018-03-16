from flask_user import current_user
from flask import url_for, redirect, request, abort
from flask_admin.contrib import sqla


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
                return redirect(url_for('security.login', next=request.url))


class UserView(AdminModelView):
    column_list = ['active', 'username', 'roles', 'email', 'confirmed_at', 'company']
    form_columns = ('active', 'roles', 'username', 'email', 'company')
    column_searchable_list = ('username', 'email')
    column_editable_list = ('active', 'username', 'email', 'company')
    page_size = 20


class RoleView(AdminModelView):
    column_list = ['name', 'description']
    form_columns = ('name', 'description')
    can_create = False
    can_delete = False
    page_size = 20


class CompanyView(AdminModelView):
    column_exclude_list = ['name', 'description', 'telephone_number', 'toll_free_number', 'address']
    form_excluded_columns = ('users', 'logo')
    page_size = 20


class HistoryView(AdminModelView):
    column_list = ['date_uploaded', 'file_name', 'user']
    column_searchable_list = ('date_uploaded', 'file_name')
    can_create = False
    can_edit = False
    page_size = 20
