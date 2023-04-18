from flask import Blueprint, render_template

report = Blueprint('user', __name__, url_prefix='/reports', static_folder='../static')

@report.route('/')
def report_list():
    return render_template('reports/list.html')