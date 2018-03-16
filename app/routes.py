from flask import render_template, flash, redirect, url_for
from app import app
from flask_user import current_user, roles_required

from app.data.models.format import FileFormatModel
from app.data.forms.upload_form import UploadForm
from flask import request
# from werkzeug.urls import url_parse

from app.exception import InvalidUsage
from app.helpers.validation import validate

from flask import jsonify
from flask_user import login_required


#
# @app.route('/uploads/<filename>')
# def uploaded_file(filename):
#     return send_from_directory(app.instance_path, filename)

@app.route('/profile')
@login_required
@roles_required('Vendor')
def profile():
    return '<h1>This is the protected profile page!</h1>'


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    if current_user.has_role('Admin'):
        return redirect(url_for('admin.index'))
    elif current_user.has_role('Vendor'):
        return redirect(url_for('history'))
    else:
        return redirect(url_for('welcome'))


@app.route('/welcome')
def welcome():
    return render_template('welcome.html', title='Welcome')


@app.route('/history', methods=['GET', 'POST'])
@login_required
@roles_required('Vendor')
def history():
    page = request.args.get('page', 1, type=int)
    histories = current_user.upload_histories.paginate(
        page, app.config['LISTS_PER_PAGE'], False)
    next_url = url_for('history', page=histories.next_num) \
        if histories.has_next else None
    prev_url = url_for('history', page=histories.prev_num) \
        if histories.has_prev else None
    pagestart = (page-1)*app.config['LISTS_PER_PAGE']
    return render_template('history.html', title='Home Page', histories=histories.items,
                           next_url=next_url,
                           prev_url=prev_url,
                           pagestart=pagestart)


@app.route('/upload', methods=['GET', 'POST'])
@login_required
@roles_required('Vendor')
def upload():
    # file_format = FileFormatModel(title='smiles', col_type="str", order=1)
    # file_format.save_to_db()
    # file_format = FileFormatModel(title='product_id', col_type="str", order=2)
    # file_format.save_to_db()
    # file_format = FileFormatModel(title='cas_number', col_type="str", order=3)
    # file_format.save_to_db()
    form = UploadForm()
    formats = FileFormatModel.find_all()
    if form.validate_on_submit():
        return_msg = validate(form.file.data)
        #flash(validate(form.file.data))
        return jsonify(return_msg)
    return render_template('upload.html', title='Upload File', form=form, formats=formats)


# @app.errorhandler(InvalidUsage)
# def handle_invalid_usage(error):
#     response = jsonify(error.to_dict())
#     response.status_code = error.status_code
#     return response


# @app.route('/admin/', methods=['GET', 'POST'])
# @login_required
# @roles_required('Admin')    # Use of @roles_required decorator
# def admin_page():
#     return render_template('admin/index.html', title='Upload File')
