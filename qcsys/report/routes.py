# -*- coding:utf8 -*-
#encoding = utf-8

from flask import Blueprint, flash, redirect, url_for, session, request, render_template, jsonify
from functools import wraps
from wtforms import Form, StringField, TextAreaField, validators,SelectField, SelectMultipleField,\
                    IntegerField, DecimalField
from wtforms.fields.html5 import DateField
from datetime import datetime
from ..views import mysql
import calendar
from math import ceil
import logging

reportApp = Blueprint('report', __name__,
                     template_folder='templates',
                     static_folder='static'
                     )

# 部门名称字典
dept_dict = {'酒店部':'hotel', '运输部':'trans', '导游部':'guide', '美东部':'ec', 'local部':'local',
             'ECI部': 'eci', '邮轮部':'cruise', '销售部':'sales', '票务部':'ticket', '市场部':'mkting',
             '芝加哥分部': 'chi', '华盛顿分部':'dc', '奥兰多分部':'orlando', '迈阿密分部':'mia', '西雅图分部':'sea',
             '德州分部': 'texas', '亚特兰大分部':'alt', '特殊案例':'spcl', '其他地接':'other', '波士顿分部':'bos',
             '接机部': 'ap'}

dept_filter = ['酒店部', '运输部', '导游部','美东部', 'local部', 'ECI部',
               '邮轮部', '销售部', '票务部','市场部', '芝加哥分部', '奥兰多分部',
               '华盛顿分部', '迈阿密分部', '西雅图分部','德州分部', '亚特兰大分部', '特殊案例',
               '其他地接', '波士顿分部', '接机部']

#人员，资源分类
source_type = [('guide', '导游'),('bus', '巴士'),('hotel', '酒店'),('pdt', '产品')]

#年度
year_items = [('2018', '2018年'),('2019', '2019年'),('2020', '2020年')]

#年度
period_items = [('1Q', '第一季度'), ('2Q', '第二季度'), ('3Q', '第三季度'), ('4Q', '第四季度'),
                ('1H', '上半年'), ('2H', '下半年'), ('all', '全年')]

#数据内容
#data_type_items = [('case_count', '投诉数量'),('customer', '客户满意度'),('source', '投诉来源'),('refund', '退款金额')]
data_type_items = [('case_count', '投诉数量'),('refund', '退款金额')]

# Check if user logged in
def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Unauthorized, Please login', 'danger')
            return redirect(url_for('index'))
    return wrap


class reportDate(Form):
    start_date = DateField('开始日期',[validators.InputRequired(message='请选择日期')], format='%Y-%m-%d')
    end_date = DateField('结束日期',[validators.InputRequired(message='请选择日期')], format='%Y-%m-%d')

class reportCategory(Form):
    type = SelectField('资源分类', choices=source_type)

class generalStatisics(Form):
    year = SelectField('年份', choices=year_items)
    period = SelectField('周期', choices=period_items)
    data_type = SelectField('数据内容', choices=data_type_items)


@reportApp.route('/')
@is_logged_in
def report_home():
    return render_template('reports.html')



################# 各部门相关的统计 #####################

class departments():
    def __init__(self, depts, case_labels):
        self.depts = depts
        self.case_labels = case_labels

#返回时间区间内的case列表
def get_case_list(my_cur, s_date, e_date):

    get_result_str = 'SELECT qc_num FROM basic_info WHERE creat_date >= "{}" AND creat_date <= "{}"'.format(s_date, e_date)
    get_case_result = my_cur.execute(get_result_str)
    if get_case_result:
        cases = my_cur.fetchall()
        return cases
    return 0

#返回时间区间内出现过的部门list
def get_case_depts(my_cur, cases, dept):

    dept_list = ()
    for case in cases:
        get_result_str = 'SELECT parent_title, title FROM label_info WHERE qc_num = "{}" '.format(case['qc_num'])
        get_case_result = my_cur.execute(get_result_str)
        if get_case_result:
            depts = my_cur.fetchall()
            dept_list = dept_list + depts

    for d in dept_list:
        if d['parent_title'] in dept_filter:
            if d['parent_title'] != '0':
                dept.depts[d['parent_title']] += 1
            else:
                dept.depts[d['title']] += 1
    return 1

#返回时间区间内部门对应的cases 和 labels
def get_case_labels(my_cur, cases, dept):
    list = ()
    labels = {'label':'','qc_num':''}
    for case in cases:
        get_result_str = 'SELECT parent_title, title, qc_num  FROM label_info WHERE qc_num = "{}" '.format(case['qc_num'])
        get_case_result = my_cur.execute(get_result_str)
        if get_case_result:
            depts = my_cur.fetchall()
            list = list + depts

    for d in list:
        if d['parent_title'] in dept_filter:
            if d['parent_title'] != '0':
                labels['label'] = d['title']
                labels['qc_num'] = d['qc_num']
                dept.case_labels[d['parent_title']].append(labels.copy())
    return 1

@reportApp.route('/reportdept', methods=['GET', 'POST'])
@is_logged_in
def report_dept():
    date_form = reportDate(request.form)
    date_format = '%Y-%m-%d %H:%M:%S'

    r_depts = {'酒店部':0, '运输部':0, '导游部':0, '美东部':0, 'local部':0,
             'ECI部': 0, '邮轮部':0, '销售部':0, '票务部':0, '市场部':0,
             '芝加哥分部': 0, '华盛顿分部':0, '奥兰多分部':0, '迈阿密分部':0, '西雅图分部':0,
             '德州分部': 0, '亚特兰大分部':0, '特殊案例':0, '其他地接':0, '波士顿分部':0,
               '接机部':0}
    r_case_labels = {'酒店部': [], '运输部': [], '导游部': [],
                   '美东部':[], 'local部':[],'ECI部':[],
                   '邮轮部':[], '销售部':[], '票务部':[],
                   '市场部':[],'芝加哥分部':[], '华盛顿分部':[],
                   '奥兰多分部':[], '迈阿密分部':[], '西雅图分部':[],
                   '德州分部':[], '亚特兰大分部':[], '特殊案件':[],
                   '其他地接':[], '波士顿分部':[], '接机部':[]}

    if request.method == 'POST' and date_form.validate():
        dept = departments(r_depts,r_case_labels)
        start_date = date_form.start_date.data
        end_date = date_form.end_date.data

        start_date = datetime.strptime(start_date.strftime(date_format),date_format)
        end_date = datetime.strptime(end_date.strftime(date_format),date_format).replace(hour=23,minute=59,second=59)

        if start_date > end_date:
            msg = '开始日期必须早于或等于结束日期! 请重新输入！'
            return render_template('reportdept.html', dateform=date_form,  num=0, summery=0, msg=msg)

        cur = mysql.connection.cursor()
        case_list = get_case_list(cur, start_date,end_date)
        if case_list:
            if len(case_list) > 0:
                get_case_depts(cur, case_list, dept)
                get_case_labels(cur, case_list, dept)

                #print(dept.case_labels)
                cur.close()
                return render_template('reportdept.html', dateform=date_form, num=dept.depts, summery=dept.case_labels)

            msg = '所选日期范围内没有数据，请重新选择其他日期范围。'
            cur.close()
            return render_template('reportdept.html', dateform=date_form, msg=msg, num=0, summery=0)

        msg = '所选日期范围内没有数据，请重新选择其他日期范围。'
        cur.close()
        return render_template('reportdept.html', dateform=date_form, msg=msg, num=0, summery=0)
    else:
        return render_template('reportdept.html', dateform=date_form, num=0, summery=0)


#############  代理商相关统计 #############

def get_caselist_agent(my_cur, s_date, e_date):

    get_result_str = 'SELECT qc_num FROM basic_info WHERE creat_date >= "{}" AND creat_date <= "{}"'.format(s_date, e_date)
    get_case_result = my_cur.execute(get_result_str)
    if get_case_result:
        cases = my_cur.fetchall()
        return cases
    return 0

def get_agent_list(my_cur, cases):
    agents = []
    for case in cases:
        get_result_str = 'SELECT qc_num, u.name FROM order_info AS o, user_mgmt AS u WHERE qc_num = "{}" AND o.agent = u.id'.format(case["qc_num"])
        get_case_result = my_cur.execute(get_result_str)
        if get_case_result:
            agents.append(my_cur.fetchone())
    return agents

def get_agents(agents_list):
    result = {}
    temp_amount = {}
    temp_case = {}

    for a_l in agents_list:
        temp_amount[a_l['name']] = 0
        temp_case[a_l['qc_num']] = a_l['name']

    for a_l in agents_list:
        temp_amount[a_l['name']] += 1

    result['amount'] = temp_amount
    result['cases'] = temp_case

    return  result

@reportApp.route('/reportagent', methods=['GET', 'POST'])
@is_logged_in
def report_agent():
    date_form = reportDate(request.form)
    date_format = '%Y-%m-%d %H:%M:%S'
    agents = []

    if request.method == 'POST' and date_form.validate():
        start_date = date_form.start_date.data
        end_date = date_form.end_date.data
        start_date = datetime.strptime(start_date.strftime(date_format),date_format)
        end_date = datetime.strptime(end_date.strftime(date_format),date_format).replace(hour=23,minute=59,second=59)

        if start_date > end_date:
            msg = '开始日期必须早于或等于结束日期! 请重新输入！'
            return render_template('reportagent.html', dateform=date_form, msg=msg, agents=0)

        cur = mysql.connection.cursor()
        case_list = get_caselist_agent(cur, start_date, end_date)
        if case_list:
            if len(case_list) > 0:
                agent_list = get_agent_list(cur, case_list)
                agents = get_agents(agent_list)

                cur.close()
                return render_template('reportagent.html', dateform=date_form, amount=agents['amount'], cases=agents['cases'])

            msg = '所选日期范围内没有数据，请重新选择其他日期范围。'
            cur.close()
            return render_template('reportagent.html', dateform=date_form, msg=msg, amount=0, cases=0)

        msg = '所选日期范围内没有数据，请重新选择其他日期范围。'
        cur.close()
        return render_template('reportagent.html', dateform=date_form, msg=msg, amount=0, cases=0)
    else:
        return render_template('reportagent.html', dateform=date_form, amount=0, cases=0)


#############  Top 10 排名相关 #############


############# 统计图表-代理商，部门，事业部 ###############

#返回时间区间内的事业部统计
def tours_dept_total(my_cur, s_date, e_date):
    get_result_str = 'SELECT COUNT(CASE WHEN o.invoice LIKE "JL%" THEN 1 END) AS "Local",' \
                     'COUNT(CASE WHEN o.invoice LIKE "JE%" THEN 1 END) AS "EC",' \
                     'COUNT(CASE WHEN o.invoice LIKE "JW%" THEN 1 END) AS "ECI"' \
                     'FROM basic_info AS b, order_info AS o ' \
                     'WHERE b.qc_num = o.qc_num AND b.creat_date >= "{}" AND b.creat_date <= "{}"'.format(s_date, e_date)

    get_case_result = my_cur.execute(get_result_str)
    if get_case_result:
        total = my_cur.fetchone()
        return total
    return 0

#返回时间区间内的case列表和case总数
def case_list_total(my_cur, s_date, e_date):
    result = {}
    get_result_str = 'SELECT qc_num FROM basic_info WHERE creat_date >= "{}" AND creat_date <= "{}"'.format(s_date, e_date)
    get_case_result = my_cur.execute(get_result_str)
    if get_case_result:
        cases = my_cur.fetchall()
        get_result_str = 'SELECT COUNT(*) FROM basic_info WHERE creat_date >= "{}" AND creat_date <= "{}"'.format(s_date, e_date)
        get_case_result = my_cur.execute(get_result_str)
        if get_case_result:
            count = my_cur.fetchone()
            result['cases'] = cases
            result['count'] = count
            return result
        return 0
    return 0

def get_dpt_dict(dept):
    dpt_dict = {}
    dpt_name = []
    dpt_num = []
    for key,value in dept.items() :
        if value > 0:
            dpt_name.append(key)
            dpt_num.append(value)
    dpt_dict['name'] = dpt_name.copy()
    dpt_dict['num'] = dpt_num.copy()

    return dpt_dict

def get_agt_dict(agent):
    agt_dict = {}
    agent_name = []
    agent_num = []
    for key, value in agent.items():
        agent_name.append(key)
        agent_num.append(value)

    agt_dict['name'] = agent_name.copy()
    agt_dict['num'] = agent_num.copy()
    return agt_dict

def get_total(cases, label_num):
    label_total = sum(label_num.values())
    case_total = cases['COUNT(*)']
    return {'case_total':case_total,'label_total':label_total}

@reportApp.route('/charts_statistics', methods=['GET', 'POST'])
@is_logged_in
def normal_charts():
    date_form = reportDate(request.form)
    date_format = '%Y-%m-%d %H:%M:%S'
    title_format = '%Y-%m-%d'
    r_depts = {'酒店部': 0, '运输部': 0, '导游部': 0, '美东部': 0, 'local部': 0,
               'ECI部': 0, '邮轮部': 0, '销售部': 0, '票务部': 0, '市场部': 0,
               '芝加哥分部': 0, '华盛顿分部': 0, '奥兰多分部': 0, '迈阿密分部': 0, '西雅图分部': 0,
               '德州分部': 0, '亚特兰大分部': 0, '特殊案例': 0, '其他地接': 0, '波士顿分部': 0,
               '接机部': 0}
    r_case_labels = {'酒店部': [], '运输部': [], '导游部': [],
                     '美东部': [], 'local部': [], 'ECI部': [],
                     '邮轮部': [], '销售部': [], '票务部': [],
                     '市场部': [], '芝加哥分部': [], '华盛顿分部': [],
                     '奥兰多分部': [], '迈阿密分部': [], '西雅图分部': [],
                     '德州分部': [], '亚特兰大分部': [], '特殊案件': [],
                     '其他地接': [], '波士顿分部': [], '接机部': []}

    if request.method == 'POST' and date_form.validate():
        dept = departments(r_depts, r_case_labels)
        start_date = date_form.start_date.data
        end_date = date_form.end_date.data
        title = start_date.strftime(title_format) + " 至 " + end_date.strftime(title_format)

        start_date = datetime.strptime(start_date.strftime(date_format),date_format)
        end_date = datetime.strptime(end_date.strftime(date_format),date_format).replace(hour=23,minute=59,second=59)
        if start_date > end_date:
            msg = '开始日期必须早于或等于结束日期! 请重新输入！'
            return render_template('reportagent.html', dateform=date_form, msg=msg, agents=0)

        cur = mysql.connection.cursor()
        tours_dpt = tours_dept_total(cur, start_date, end_date)
        cases_summery = case_list_total(cur, start_date, end_date)
        if cases_summery:
            get_case_depts(cur, cases_summery['cases'], dept)
            agent_list = get_agent_list(cur, cases_summery['cases'])
            agents = get_agents(agent_list)

            dpt_dict = get_dpt_dict(dept.depts)
            agt_dict = get_agt_dict(agents['amount'])
            total = get_total(cases_summery['count'], dept.depts)

            cur.close()
            return render_template('charts_statistics.html', dateform=date_form, title=title, total=total, dpt_dict=dpt_dict,agt_dict=agt_dict,dpt_total=tours_dpt)

        msg = '所选日期范围内没有数据，请重新选择其他日期范围。'
        cur.close()
        return render_template('charts_statistics.html', dateform=date_form, title="N/a", total=0, dpt_dict=0,agt_dict=0,dpt_total=0)

    else:
        return render_template('charts_statistics.html', dateform=date_form, title="N/a", total=0, dpt_dict=0, agt_dict=0,dpt_total=0)


############# 报告中心-综合统计 ###############

def get_general_report(my_cur, s_date, e_date, s_type):
    get_result_str = ''
    if s_type == 'guide': # 导游
        get_result_str = 'SELECT u.name, COUNT(o.qc_num) AS "subtotal" ' \
                        'FROM basic_info AS b, order_info AS o, user_mgmt AS u ' \
                        'WHERE b.qc_num = o.qc_num AND u.id = o.tour_guide AND b.creat_date >= "{}" AND b.creat_date <= "{}" ' \
                         'GROUP BY u.name ' \
                         'ORDER BY subtotal DESC'.format(s_date, e_date)
    if s_type == 'bus': # 巴士
        get_result_str = 'SELECT o.src_name AS name, COUNT(o.qc_num) AS "subtotal" ' \
                         'FROM basic_info AS b, other_info AS o ' \
                         'WHERE b.qc_num = o.qc_num AND o.src_type = "bus" AND b.creat_date >= "{}" AND b.creat_date <= "{}" ' \
                         'GROUP BY name ' \
                         'ORDER BY subtotal DESC'.format(s_date, e_date)
    if s_type == 'hotel': # 酒店
        get_result_str = 'SELECT o.src_name AS name, COUNT(o.qc_num) AS "subtotal" ' \
                         'FROM basic_info AS b, other_info AS o ' \
                         'WHERE b.qc_num = o.qc_num AND o.src_type = "hotel" AND b.creat_date >= "{}" AND b.creat_date <= "{}" ' \
                         'GROUP BY name ' \
                         'ORDER BY subtotal DESC'.format(s_date, e_date)
    if s_type == 'pdt': # 产品
        get_result_str = 'SELECT o.tour_code AS name, COUNT(o.qc_num) AS "subtotal" ' \
                         'FROM basic_info AS b, order_info AS o ' \
                         'WHERE b.qc_num = o.qc_num AND b.creat_date >= "{}" AND b.creat_date <= "{}" ' \
                         'GROUP BY o.tour_code ' \
                         'ORDER BY subtotal DESC'.format(s_date, e_date)

    if get_result_str != '':
        get_case_result = my_cur.execute(get_result_str)
        if get_case_result:
            total = my_cur.fetchall()
            return total
    return 0

@reportApp.route('/generalreport', methods=['GET', 'POST'])
@is_logged_in
def general_report():
    date_form = reportDate(request.form)
    category_form = reportCategory(request.form)
    date_format = '%Y-%m-%d %H:%M:%S'

    if request.method == 'POST' and date_form.validate():
        start_date = date_form.start_date.data
        end_date = date_form.end_date.data
        category = category_form.type.data
        #title = start_date.strftime(title_format) + " 至 " + end_date.strftime(title_format)

        start_date = datetime.strptime(start_date.strftime(date_format),date_format)
        end_date = datetime.strptime(end_date.strftime(date_format),date_format).replace(hour=23,minute=59,second=59)
        if start_date > end_date:
            msg = '开始日期必须早于或等于结束日期! 请重新输入！'
            return render_template('generalreport.html', dateform=date_form, category=category_form, msg=msg, g_report=0)

        cur = mysql.connection.cursor()
        g_report = get_general_report(cur, start_date, end_date, category)
        print(g_report)
        if g_report:
            return render_template('generalreport.html', dateform=date_form, category=category_form, g_report=g_report)

        msg = '没有找到数据，请选择其他时间段'
        return render_template('generalreport.html', dateform=date_form, category=category_form, msg=msg, g_report=0)
    return render_template('generalreport.html', dateform=date_form, category=category_form, g_report=0)


############# 报告中心-综合统计 ###############
def get_start_end_date(year, period):
    date_format = '%Y-%m-%d %H:%M:%S'
    dates = {}
    if period == '1Q':
        dates['start'] = datetime.strptime(year+'-01-01 00:00:00', date_format)
        dates['end'] = datetime.strptime(year+'-03-31 00:00:00', date_format).replace(hour=23,minute=59,second=59)
        dates['label'] = ['January','February','March']
        return dates
    elif period == '2Q':
        dates['start'] = datetime.strptime(year + '-04-01 00:00:00', date_format)
        dates['end'] = datetime.strptime(year + '-06-30 00:00:00', date_format).replace(hour=23, minute=59, second=59)
        dates['label'] = ['April', 'May', 'June']
        return dates
    elif period == '3Q':
        dates['start'] = datetime.strptime(year + '-07-01 00:00:00', date_format)
        dates['end'] = datetime.strptime(year + '-09-30 00:00:00', date_format).replace(hour=23, minute=59, second=59)
        dates['label'] = ['July', 'August', 'September']
        return dates
    elif period == '4Q':
        dates['start'] = datetime.strptime(year + '-10-01 00:00:00', date_format)
        dates['end'] = datetime.strptime(year + '-12-31 00:00:00', date_format).replace(hour=23, minute=59, second=59)
        dates['label'] = ['October', 'November', 'December']
        return dates
    elif period == '1H':
        dates['start'] = datetime.strptime(year + '-01-01 00:00:00', date_format)
        dates['end'] = datetime.strptime(year + '-06-30 00:00:00', date_format).replace(hour=23, minute=59, second=59)
        dates['label'] = ['January', 'February', 'March', 'April', 'May', 'June']
        return dates
    elif period == '2H':
        dates['start'] = datetime.strptime(year + '-07-01 00:00:00', date_format)
        dates['end'] = datetime.strptime(year + '-12-31 00:00:00', date_format).replace(hour=23, minute=59, second=59)
        dates['label'] = ['July', 'August', 'September', 'October', 'November', 'December']
        return dates
    elif period == 'all':
        dates['start'] = datetime.strptime(year + '-01-01 00:00:00', date_format)
        dates['end'] = datetime.strptime(year + '-12-31 00:00:00', date_format).replace(hour=23, minute=59, second=59)
        dates['label'] = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
        return dates
    else:
        return 0

def get_statistics_data(my_cur, dates, type):
    get_result_str = ''
    if type == 'case_count': # 投诉数量
        get_result_str = "SELECT COUNT(qc_num) AS total, MONTHNAME(creat_date) AS month, MONTH(creat_date) AS m " \
                         "From basic_info " \
                         "WHERE creat_date >= '{}' AND creat_date <= '{}' " \
                         "GROUP BY month, m " \
                         "ORDER BY m ".format(dates['start'], dates['end'])
    elif type == 'refund': #退款金额
        pass
    else:
        return 0
    if get_result_str != '':
        get_case_result = my_cur.execute(get_result_str)
        if get_case_result:
            result = my_cur.fetchall()
            return list(result)


@reportApp.route('/general_statistics', methods=['GET', 'POST'])
@is_logged_in
def general_statistics():
    date_form = generalStatisics(request.form)

    if request.method == 'POST' and date_form.validate():
        stc_year = date_form.year.data
        stc_period = date_form.period.data
        stc_type = date_form.data_type.data
        dates = get_start_end_date(stc_year,stc_period)
        if dates:
            cur = mysql.connection.cursor()
            stc_data = get_statistics_data(cur, dates,stc_type)
            labels = []
            if stc_data:
                for d in stc_data:
                    labels.append(d['month'])
                return render_template('general_statistics.html', dateform=date_form, stc_data=stc_data, labels=labels,legend=stc_type)

            msg = '没有找到数据，请选择其他时间段'
            return render_template('general_statistics.html', dateform=date_form, msg=msg, stc_data=0, labels=0, legend=0)

    return render_template('general_statistics.html', dateform=date_form, stc_data=0, labels=0, legend=0)