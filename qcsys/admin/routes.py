# -*- coding:utf8 -*-
#encoding = utf-8

from flask import Blueprint, flash, redirect, url_for, session, request, render_template, jsonify
from functools import wraps
from wtforms import Form, StringField, TextAreaField, validators,SelectField, SelectMultipleField,\
                    IntegerField, DecimalField
from wtforms.fields.html5 import DateField
from datetime import datetime
from ..views import mysql
from math import ceil

adminApp = Blueprint('admin', __name__,
                     template_folder='templates',
                     static_folder='static'
                     )


# ##### Global variable and functions #####
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

# user type
user_type = [('guide', '导游'), ('driver', '司机'), ('agent', '代理'),('bus', '巴士'),('hotel', '酒店'), ('other', '其他')]
# case status
case_status = [('new','新投诉'),('processing','处理中'),('w_response','等待回复'),('w_confirm','等待确认'),('w_email','等待邮件'),
               ('report','反映情况'),('solved','已解决'),('cancel','投诉取消'), ('terminated','投诉终止')]
# departments and bill to items
dept_category = [('hotel','酒店部'),('trans','运输部'),('guide','导游部'),('ec','美东部'),
                 ('local', 'local部'), ('eci', 'ECI部'),('cruise','邮轮部'),('sales','销售部'),
                 ('ticket', '票务部'), ('mkting', '市场部'),('chi','芝加哥分部'),('dc','华盛顿分部'),
                 ('orlando', '奥兰多分部'), ('mia', '迈阿密分部'),('sea','西雅图分部'),('texas','德州分部'),
                 ('spcl', '特殊案例'), ('other', '其他地接'), ('it', 'IT部'), ('acc', '会计部'),
                 ('na', '待输入'), ('bos', '波士顿分部'), ('ap', '接机部')]

# case source select items
case_source_s = [('phone_a', '代理致电'), ('email_a', '代理发邮件'), ('phone_c', '客人致电'), ('email_c', '客人发邮件'),
                 ('phone_e', '内部同事致电'), ('email_e', '内部同事发邮件'), ('wechat', '微信投诉')]

# responsible party select items
case_resp_party_s = [('agent', '代理'), ('uv', '纵横'), ('customer', '客人'), ('uvc', '纵横和客人'), ('uva', '纵横和代理'), ('uvac', '纵横和客人和代理'), ('other', '第四方'), ('na', '待输入')]

# case reference select items
case_reference_s = [('compensation', '赔偿方案'), ('compensation final', '赔偿方案终极'), ('more', '多'), ('less', '少'), ('na', '待输入')]

# customer satisfaction select items
case_satisfaction_s = [('acceptance', '接受赔偿'), ('great', '非常满意'), ('good', '满意'), ('displeasure', '不满意'), ('catastrophic', '非常不满'), ('na', '待输入')]

# payment method select items
case_payment_s = [('credit', 'Credit Memo'), ('quickpay', 'Quickpay'), ('cb', '中国的银行'), ('ub', '美国的银行'),
                  ('check', '支票'), ('bill', 'Billed'), ('tt', 'TT'), ('rtt', 'Refunded By TT'), ('GRF', '导游退款'),
                  ('other', '其他'), ('na', '待输入')]

# other info type select items
other_type_list = [('bus', '巴士'), ('hotel', '酒店'), ('tic', '门票'), ('other', '其他')]

# get user list
def getting_user_list(table_name, user_type):
    cur = mysql.connection.cursor()
    if table_name == 'acct_mgmt':
        result = cur.execute("SELECT username FROM acct_mgmt WHERE is_using=1 AND username NOT IN ('admin')")
    elif table_name == 'user_mgmt' and user_type != 'all':
        str = "SELECT id,name FROM user_mgmt WHERE is_using=1 AND type='{}'".format(user_type)
        result = cur.execute(str)
    elif table_name == 'user_mgmt' and user_type == 'all':
        result = cur.execute("SELECT id, name FROM user_mgmt WHERE is_using=1")
    else:
        result = 0

    if result > 0:
        listItems = cur.fetchall()
        cur.close()
        return listItems
    else:
        cur.close()
        return 0

def user_select_list(table_name, user_type):
    userlist = []
    itemlist = getting_user_list(table_name, user_type)
    if itemlist != 0:
        if table_name == 'acct_mgmt':
            for item in itemlist:
                userlist.append((item['username'],item['username']))
            return  userlist
        elif table_name == 'user_mgmt' and user_type != 'all':
            for item in itemlist:
                userlist.append((str(item['id']),item['name']))
            return userlist
        elif table_name == 'user_mgmt' and user_type == 'all':
            for item in itemlist:
                userlist.append((str(item['id']),item['name']))
            return userlist
        else:
            return 0
    else:
        return 0

def transferContent(content):
    if content is None:
        return None
    else:
        string = ""
        for c in content:
            if c == '"':
                string += '\\\"'
            elif c == "'":
                string += "\\\'"
            elif c == "\\":
                string += "\\\\"
            else:
                string += c
        return string


# ##### Global variable and functions end #####


@adminApp.route('/')
@is_logged_in
def index():
    return render_template('home.html')



# ##### label begin #####
class label(Form):
    title = StringField('标签名', [validators.length(min=1, max=100),validators.InputRequired(message='标签名必填！')])
    under = StringField('所属标签')
    comments = TextAreaField('中文回复范例')
    comments_eng = TextAreaField('英文回复范例')


@adminApp.route('/labels', defaults={'pagenum': 1})
@adminApp.route('/labels&page=<int:pagenum>')
@is_logged_in
def labels(pagenum):
    pages = int(pagenum) -1

    pageCur = mysql.connection.cursor()
    totalResults = pageCur.execute("SELECT * FROM label_mgmt WHERE level=1")
    totalPages = totalResults / 10
    pageCur.close()

    cur = mysql.connection.cursor()
    result = cur.execute("SELECT * FROM label_mgmt WHERE level=1 LIMIT %s,%s", (pages * 10, 10))
    if result > 0:
        listItems = cur.fetchall()
        cur.close()
        return render_template('labels.html', labels=listItems, pages=ceil(totalPages))
    else:
        cur.close()
        msg = 'No Content Found'
        return render_template('labels.html', msg=msg)


@adminApp.route('/childlabels&<string:title>', defaults={'pagenum': 1})
@adminApp.route('/childlabels&<string:title>&page=<int:pagenum>')
@is_logged_in
def child_labels(pagenum,title):
    pages = int(pagenum) -1
    pageCur = mysql.connection.cursor()
    totalResults = pageCur.execute("SELECT * FROM label_mgmt WHERE parent=%s", [title])
    totalPages = totalResults / 10
    pageCur.close()

    cur = mysql.connection.cursor()
    result = cur.execute("SELECT * FROM label_mgmt WHERE parent=%s LIMIT %s,%s", ( title, pages * 10, 10))
    if result > 0:
        listItems = cur.fetchall()
        cur.close()
        return render_template('childlabels.html', labels=listItems, pages=ceil(totalPages),parent=title)
    else:
        cur.close()
        msg = 'No Content Found'
        return render_template('childlabels.html', msg=msg, pages=0, parent=title)


@adminApp.route('/addlabel', methods=['GET', 'POST'])
@is_logged_in
def add_label():
    form = label(request.form)

    if request.method == 'POST' and form.validate():
        title = form.title.data
        level = 1
        parent = '0'
        comments = transferContent(form.comments.data)
        comments_eng = transferContent(form.comments_eng.data)
        # Create Cursor
        cur = mysql.connection.cursor()
        # Execute
        cur.execute("INSERT INTO label_mgmt (title, level, parent, comments, comments_eng) VALUES(%s,%s,%s,%s,%s)",
                    (title, level, parent, comments, comments_eng))
        # commit to db
        mysql.connection.commit()
        # close connection
        cur.close()

        flash('New Content Created', 'success')
        return redirect(url_for('admin.labels'))

    return render_template('addlabel.html', form=form, parent=0)

@adminApp.route('/addchildlabel&<string:pt>', methods=['GET', 'POST'])
@is_logged_in
def add_child_label(pt):
    form = label(request.form)
    under_label = 'NULL'
    if request.method == 'POST' and form.validate():
        title = form.title.data
        parent = pt
        level = 2
        if form.under.data != '':
            under_label = form.under.data
        comments = transferContent(form.comments.data)
        comments_eng = transferContent(form.comments_eng.data)
        # Create Cursor
        cur = mysql.connection.cursor()
        # Execute
        cur.execute("INSERT INTO label_mgmt (title, level, parent, comments, comments_eng, under) VALUES(%s,%s,%s,%s,%s,%s)",
                    (title, level, parent, comments, comments_eng, under_label))
        # commit to db
        mysql.connection.commit()
        # close connection
        cur.close()

        flash('New Content Created', 'success')
        return redirect(url_for('admin.child_labels',pagenum=1,title=pt))

    return render_template('addlabel.html', form=form, parent=pt)

@adminApp.route('/editlabel/<string:labelNum>&', methods=['GET', 'POST'], defaults={'parent': 0})
@adminApp.route('/editlabel/<string:labelNum>&<string:parent>', methods=['GET', 'POST'])
@is_logged_in
def edit_label(labelNum, parent):
    form = label(request.form)
    under_label = 'NULL'
    if request.method == 'GET':
        # Create Cursor
        cur = mysql.connection.cursor()
        # Execute
        result = cur.execute("SELECT * FROM label_mgmt WHERE label_num = %s", [labelNum])
        sinContent = cur.fetchone()

        form.title.data = sinContent['title']
        form.comments.data = sinContent['comments']
        form.comments_eng.data = sinContent['comments_eng']
        form.under.data = sinContent['under']
        # close connection
        cur.close()
        return render_template('addlabel.html', form=form, parent=parent)

    elif request.method == 'POST' and form.validate():
        title = form.title.data
        comments = transferContent(form.comments.data)
        comments_eng = transferContent(form.comments_eng.data)
        if form.under.data != '':
            under_label = form.under.data
        # Create Cursor
        cur = mysql.connection.cursor()
        # Execute
        cur.execute("UPDATE label_mgmt SET title=%s, comments=%s, under=%s, comments_eng=%s WHERE label_num=%s",
                    (title, comments, under_label, comments_eng, labelNum))
        # commit to db
        mysql.connection.commit()
        # close connection
        cur.close()

        if parent == 0:
            flash('Content Updated', 'success')
            return redirect(url_for('admin.labels'))
        else:
            flash('Content Updated', 'success')
            return redirect(url_for('admin.child_labels',pagenum=1,title=parent))

    return render_template('addlabel.html', form=form, parent=parent)

@adminApp.route('/deletelabel/<string:labelNum>&', methods=['GET', 'POST'], defaults={'pt': 0})
@adminApp.route('/deletelabel/<string:labelNum>&<string:pt>', methods=['GET', 'POST'])
@is_logged_in
def delete_label(labelNum, pt):
    # Create Cursor
    cur = mysql.connection.cursor()
    # Execute
    result = cur.execute("DELETE FROM label_mgmt WHERE label_num = %s", [labelNum])
    mysql.connection.commit()
    cur.close()

    if pt == 0:
        flash('Content Deleted! ', 'success')
        return redirect(url_for('admin.labels'))
    else:
        flash('Content Deleted! ', 'success')
        return redirect(url_for('admin.child_labels', pagenum=1, title=pt))

@adminApp.route('/searchlabel', methods=['GET', 'POST'], defaults={'pagenum': 1, 'kw':'null'})
@adminApp.route('/searchlabel&page=<int:pagenum>&<string:kw>')
@is_logged_in
def search_label(pagenum,kw):
    page = int(pagenum) - 1
    keyword = kw

    if request.method == 'POST':
        keyword = request.form['search']

    pageCur = mysql.connection.cursor()
    totalResults = pageCur.execute("SELECT * FROM label_mgmt WHERE title LIKE '%" + keyword +"%'")
    totalPages = totalResults / 10
    pageCur.close()

    cur = mysql.connection.cursor()
    str = "SELECT * FROM label_mgmt WHERE title LIKE '%" + keyword +"%' LIMIT {}, {}".format(page * 10,10)
    result = cur.execute(str)
    if result > 0:
        listItems = cur.fetchall()
        cur.close()
        return render_template('labelsearch.html', labels=listItems, pages=ceil(totalPages), keyword = keyword)
    else:
        cur.close()
        msg = 'No Content Found'
        return render_template('labelsearch.html', msg=msg,keyword = keyword, pages=1)

@adminApp.route('/underlabelinput', methods=['GET'])
@is_logged_in
def under_label_input():
    search = request.args.get('q')
    # Create Cursor
    cur = mysql.connection.cursor()
    # Execute
    result = cur.execute("SELECT title FROM label_mgmt WHERE level = 2 AND title LIKE '%" + search + "%'")
    auto_result = cur.fetchall()
    # close connection
    cur.close()
    auto_list = []
    for i in auto_result:
        auto_list.append(i['title'])
    return jsonify(matching_result=auto_list)

# ##### label end #####

# ##### user begin #####
class user(Form):
    name = StringField('名称', [validators.length(min=1, max=50),validators.InputRequired(message='名称必填！')])
    remark = TextAreaField('备注信息')
    type = SelectField('分类', choices= user_type)

@adminApp.route('/users', defaults={'pagenum': 1, 'type': 'whole'})
@adminApp.route('/users&page=<int:pagenum>', defaults={'type': 'whole'})
@adminApp.route('/users&page=<int:pagenum>&<string:type>')
@is_logged_in
def users(pagenum,type):
    pages = int(pagenum) - 1
    str_page = ''
    str_result = ''

    pageCur = mysql.connection.cursor()
    if type == 'whole':
        str_page = "SELECT * FROM user_mgmt WHERE is_using = 1"
        str_result = "SELECT * FROM user_mgmt WHERE is_using = 1 LIMIT {},{}".format(pages * 10, 10)
    else:
        str_page = "SELECT * FROM user_mgmt WHERE is_using=1 AND type='{}'".format(type)
        str_result = "SELECT * FROM user_mgmt WHERE is_using=1 AND type='{}' LIMIT {},{}".format(type, pages * 10, 10)

    totalResults = pageCur.execute(str_page)
    totalPages = totalResults / 10
    pageCur.close()

    cur = mysql.connection.cursor()
    result = cur.execute(str_result)
    if result > 0:
        listItems = cur.fetchall()
        cur.close()
        return render_template('users.html', users=listItems, pages=ceil(totalPages),user_type=type)
    else:
        cur.close()
        msg = 'No Content Found'
        return render_template('users.html', msg=msg, pages=1)


@adminApp.route('/adduser', methods=['GET', 'POST'])
@is_logged_in
def add_user():
    form = user(request.form)
    if request.method == 'POST' and form.validate():
        name = form.name.data
        type = form.type.data
        remark = transferContent(form.remark.data)
        #if_unique_str = "SELECT * FROM user_mgmt WHERE is_using=1 AND name=%s AND type=%s ",(name,type)
        # Create Cursor
        cur = mysql.connection.cursor()
        if cur.execute("SELECT * FROM user_mgmt WHERE is_using=1 AND name=%s AND type=%s ",(name,type)) > 0:
            cur.close()
            flash('This user already existed!', 'warning')
            return redirect(url_for('admin.users'))
        else:
            # Execute
            cur.execute("INSERT INTO user_mgmt (name, type, remark) VALUES(%s,%s,%s)",
                        (name, type, remark))
            # commit to db
            mysql.connection.commit()
            # close connection
            cur.close()
            flash('New Content Created', 'success')
            return redirect(url_for('admin.users'))

    return render_template('adduser.html', form=form)


@adminApp.route('/edituser/<int:id>', methods=['GET', 'POST'])
@is_logged_in
def edit_user(id):
    form = user(request.form)
    if request.method == 'GET':
        # Create Cursor
        cur = mysql.connection.cursor()
        # Execute
        result = cur.execute("SELECT * FROM user_mgmt WHERE id = %s", [id])
        sinContent = cur.fetchone()

        form.name.data = sinContent['name']
        form.type.data = sinContent['type']
        form.remark.data = sinContent['remark']
        # close connection
        cur.close()
        return render_template('adduser.html', form=form)

    elif request.method == 'POST' and form.validate():
        name = form.name.data
        remark = transferContent(form.remark.data)
        type = form.type.data
        # Create Cursor
        cur = mysql.connection.cursor()
        # Execute
        cur.execute("UPDATE user_mgmt SET name=%s, type=%s, remark=%s WHERE id=%s",
                    (name, type, remark, id))
        # commit to db
        mysql.connection.commit()
        # close connection
        cur.close()

        flash('Content Updated', 'success')
        return redirect(url_for('admin.users'))

    return render_template('adduser.html', form=form)

@adminApp.route('/deleteuser/<int:id>', methods=['GET', 'POST'])
@is_logged_in
def delete_user(id):
    # Create Cursor
    cur = mysql.connection.cursor()
    # Execute
    result = cur.execute("UPDATE user_mgmt SET is_using=0 WHERE id=%s", [id])
    mysql.connection.commit()
    cur.close()

    flash('Content Deleted! ', 'success')
    return redirect(url_for('admin.users'))

@adminApp.route('/searchuser', methods=['GET', 'POST'], defaults={'pagenum': 1, 'kw':'null'})
@adminApp.route('/searchuser&page=<int:pagenum>&<string:kw>')
@is_logged_in
def search_user(pagenum, kw):
    page = int(pagenum) - 1
    keyword = kw
    if request.method == 'POST':
        keyword = request.form['search']

    pageCur = mysql.connection.cursor()
    totalResults = pageCur.execute("SELECT * FROM user_mgmt WHERE is_using=1 AND name LIKE '%" + keyword + "%'")
    totalPages = totalResults / 10
    pageCur.close()

    cur = mysql.connection.cursor()
    str = "SELECT * FROM user_mgmt WHERE is_using=1 AND name LIKE '%" + keyword + "%' LIMIT {}, {}".format(page * 10, 10)
    result = cur.execute(str)
    if result > 0:
        listItems = cur.fetchall()
        cur.close()
        return render_template('usersearch.html', users=listItems, pages=ceil(totalPages), keyword=keyword)
    else:
        cur.close()
        msg = 'No Content Found'
        return render_template('usersearch.html', msg=msg, pages=1,keyword=keyword)

# ##### user end #####

# ##### open case begin #####
class case(Form):
    qc_num = StringField('投诉编号',[validators.length(min=1, max=20),validators.InputRequired(message='编号必填！')])
    content = TextAreaField('投诉内容')
    source = SelectField('投诉来源',[validators.InputRequired(message='请选投诉来源')])
    source_subject = TextAreaField('来源信息')
    ivsg_result = TextAreaField('调查结果')

class order_info(Form):
    invoice_num = StringField('Invoice 号')
    order_num = StringField('订单号')
    dept_date = DateField('出发日期', format='%Y-%m-%d')
    tour_code = StringField('团号', [validators.length(min=1, max=15)])
    group_code = StringField('组号', [validators.length(min=1, max=180)])
    pax = IntegerField('客人数', [validators.NumberRange(min=0, max=999,message='人数不正确，请重新输入！')],default=0)
    agent = SelectField('代理名', [validators.InputRequired(message='请选择agent')], default=('default', '请选择'))
    rm_num = DecimalField('房间数',[validators.NumberRange(min=0, max=999,message='房数不正确，请重新输入！')],default=0,places=1)
    tour_guide = SelectField('主要导游')
    other_staffs = SelectMultipleField('其他涉及人员')


@adminApp.route('/opencase', methods=['GET', 'POST'])
@is_logged_in
def open_case():
    basic_form = case(request.form)
    order_form = order_info(request.form)
    case_status = 'new'
    #ctrler_list = user_select_list('acct_mgmt',0)
    agent_list = user_select_list('user_mgmt','agent')
    guide_list = user_select_list('user_mgmt','guide')
    staffs = user_select_list('user_mgmt','all')

    # basic_form.category.choices = dept_category
    order_form.agent.choices = agent_list
    order_form.tour_guide.choices = guide_list
    order_form.other_staffs.choices = staffs
    basic_form.source.choices = case_source_s

    if request.method == 'POST' and order_form.validate() and basic_form.validate():

        # basic info
        qc_num = basic_form.qc_num.data
        source = basic_form.source.data
        source_subjest = transferContent(basic_form.source_subject.data)
        content = transferContent(basic_form.content.data)
        ivsg_result = transferContent(basic_form.ivsg_result.data)
        creator = session['username']
        # order info
        agent = order_form.agent.data
        order_num = order_form.order_num.data
        invoice = order_form.invoice_num.data
        dept_date = order_form.dept_date.data
        room_num = float(order_form.rm_num.data)
        tour_guide = order_form.tour_guide.data
        guide_id = order_form.tour_guide.data
        tour_code = order_form.tour_code.data.replace(" ", "")
        group_code = order_form.group_code.data.replace(" ", "")
        pax = order_form.pax.data
        staffs = ''.join(request.form.getlist('handles[]'))

        # Execute
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO basic_info (qc_num, source, source_subject, status, content, ivsg_result, creator) VALUES(%s,%s,%s,%s,%s,%s,%s)",
                    (qc_num, source, source_subjest, case_status, content, ivsg_result, creator))

        order_str = "INSERT INTO order_info (qc_num, agent, order_num, invoice, departure_date, room_num, tour_guide, guide_id, staffs, tour_code, group_code, pax) VALUES('{}','{}','{}','{}','{}',{},'{}','{}','{}','{}','{}',{})"\
                    .format(qc_num, agent, order_num, invoice, dept_date, room_num, tour_guide, guide_id, staffs, tour_code, group_code, pax)
        cur.execute(order_str)
        mysql.connection.commit()
        # close connection
        cur.close()
        flash('New Content Created', 'success')
        return redirect(url_for('admin.case_list'))
        #return "123"

    return render_template('opencase.html', basic=basic_form, order=order_form)



@adminApp.route('/caselist', defaults={'pagenum': 1, 'status': 'whole'})
@adminApp.route('/caselist&page=<int:pagenum>', defaults={'status': 'whole'})
@adminApp.route('/caselist&page=<int:pagenum>&<string:status>')
@is_logged_in
def case_list(pagenum,status):
    pages = int(pagenum) - 1

    pageCur = mysql.connection.cursor()
    if status == 'whole':
        totalResults = pageCur.execute("SELECT basic_info.qc_num, status, creat_date, agent, invoice FROM basic_info, order_info WHERE basic_info.qc_num = order_info.qc_num AND basic_info.status NOT IN ('solved','cancel','terminated')")
    else:
        totalResults = pageCur.execute("SELECT basic_info.qc_num, status, creat_date, agent, invoice FROM basic_info, order_info WHERE basic_info.qc_num = order_info.qc_num AND basic_info.status = '"+ status +"'")
    totalPages = totalResults / 10
    pageCur.close()

    cur = mysql.connection.cursor()
    if status == 'whole':
        result = cur.execute("SELECT basic_info.qc_num, status, creat_date, agent, invoice, us.name FROM basic_info,order_info,user_mgmt AS us WHERE basic_info.qc_num = order_info.qc_num AND order_info.agent = us.id AND basic_info.status NOT IN ('solved','cancel','terminated') ORDER BY creat_date DESC LIMIT %s,%s ", (pages * 10, 10))
    else:
        result = cur.execute("SELECT basic_info.qc_num, status, creat_date, agent, invoice, us.name FROM basic_info,order_info,user_mgmt AS us WHERE basic_info.qc_num = order_info.qc_num AND order_info.agent = us.id AND basic_info.status = '"+ status +"' ORDER BY creat_date DESC LIMIT %s,%s ", (pages * 10, 10))
    if result > 0:
        listItems = cur.fetchall()
        cur.close()
        return render_template('caselist.html', caseinfos=listItems, pages=ceil(totalPages), status=status)
    else:
        cur.close()
        msg = 'No Content Found'
        return render_template('caselist.html', msg=msg,pages=1,status=status)

@adminApp.route('/uniquecheck', methods=['GET'])
@is_logged_in
def unique_check():
    qc_num = request.args.get('qcnum')
    msg = '请输入不重复且正确的投诉编号'
    if qc_num == ''or qc_num.find('#') != -1:
        return jsonify(errormsg=msg)
    else:
        cur = mysql.connection.cursor()
        str = 'SELECT qc_num FROM basic_info WHERE qc_num = "{}"'.format(qc_num)
        result = cur.execute(str)
        if result > 0:
            cur.close()
            return jsonify(errormsg=1)
        else:
            return jsonify(errormsg=0)


@adminApp.route('/staffinput', methods=['GET'])
@is_logged_in
def staff_input():
    search = request.args.get('q')
    # Create Cursor
    cur = mysql.connection.cursor()
    # Execute
    result = cur.execute("SELECT name FROM user_mgmt WHERE type <> 'agent' AND name like '%" + search + "%'")
    auto_result = cur.fetchall()
    # close connection
    cur.close()
    auto_list = []
    for i in auto_result:
        auto_list.append(i['name'])
    return jsonify(matching_result=auto_list)

# ##### open case end #####

# ##### processing case begin #####
@adminApp.route('/changestatus', methods=['POST'])
@is_logged_in
def change_status():
    current_user = session['username']
    if request.method == 'POST':
        qc_id = request.form['s_qc_id']
        comment = transferContent(request.form['s_message_t'])
        status = request.form['s_status']

        cur = mysql.connection.cursor()

        status_str = "UPDATE basic_info SET status = '{}' WHERE qc_num = '{}'".format(status, qc_id)
        cur.execute(status_str)

        comment_str = "INSERT INTO mdfy_comments (cmt_user, cmt_content, qc_num, case_status, type) VALUES('{}','{}','{}','{}','{}')" \
            .format(current_user, comment, qc_id, status, 'status')
        cur.execute(comment_str)

        mysql.connection.commit()
        cur.close()

        return redirect(url_for('admin.case_list',pagenum=1))
    return redirect(url_for('admin.case_list',pagenum=1))


@adminApp.route('/caseprocessing', methods=['POST'])
@is_logged_in
def case_processing():
    current_user = session['username']
    if request.method == 'POST':
        qc_id = request.form['p_qc_id']
        result = transferContent(request.form['p_message_t'])

        cur = mysql.connection.cursor()

        comment_str = "INSERT INTO mdfy_comments (cmt_user, cmt_content, qc_num, type) VALUES('{}','{}','{}','{}')" \
            .format(current_user, result, qc_id, 'processing')
        cur.execute(comment_str)

        mysql.connection.commit()
        cur.close()

        return redirect(url_for('admin.case_list',pagenum=1))
    return redirect(url_for('admin.case_list',pagenum=1))

@adminApp.route('/caselabels/', methods=['GET', 'POST'], defaults={'qccode': 'NULL'})
@adminApp.route('/caselabels/<string:qccode>', methods=['GET', 'POST'])
@is_logged_in
def case_labels(qccode):
    depts = []
    if request.method == 'POST' and qccode != 'NULL' :
        cur = mysql.connection.cursor()
        labels = request.form.getlist('labels[]')
        for lb in labels:
            p_title = lb.split(':')[0]
            c_title = lb.split(':')[1]
            case_label_insert = "INSERT INTO label_info (qc_num, parent_title, title) VALUES('{}','{}','{}')".\
                format(qccode, p_title, c_title)
            cur.execute(case_label_insert)
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('admin.case_list', pagenum=1))
    elif request.method == 'GET' and qccode != 'NULL':
        cur = mysql.connection.cursor()

        case_labels_str = "SELECT li.parent_title,li.title,li.qc_num, lm.comments, lm.comments_eng FROM label_info AS li, label_mgmt AS lm WHERE qc_num='{}' AND li.title = lm.title AND li.parent_title = lm.parent ".format(qccode)
        if cur.execute(case_labels_str) :
            case_labels_results = cur.fetchall()
            cur.close()
            return render_template('caselabels.html', labels=case_labels_results)
        else:
            cur.close()
            return render_template('caselabels.html', labels=0)
    else:
        msg = 'No Content Found'
        return render_template('caselabels.html', msg=msg, labels=0)


@adminApp.route('/labelinput', methods=['GET'])
@is_logged_in
def label_input():
    search = request.args.get('labeldata')
    # Create Cursor
    cur = mysql.connection.cursor()
    # Execute
    result = cur.execute("SELECT title,parent FROM label_mgmt WHERE title like '%" + search + "%'")
    auto_result = cur.fetchall()
    # close connection
    cur.close()
    auto_list = []
    for i in auto_result:
        if i['parent'] == 0:
            auto_list.append(i['title'] +':'+i['title'])
        else:
            auto_list.append(i['parent'] +':'+i['title'])
    return jsonify(matching_result=auto_list)


@adminApp.route('/deletecaselabel/', defaults={'qccode': 'NULL'})
@adminApp.route('/deletecaselabel/<string:code>')
@is_logged_in
def delete_case_label(code):
    qc_code = ''
    if code != 'NULL':
        qc_code = code.split(':')[0]
        del_title = code.split(':')[1]
        del_p_title = code.split(':')[2]
        # Create Cursor
        cur = mysql.connection.cursor()
        # Execute
        result = cur.execute("DELETE FROM label_info WHERE qc_num = %s AND title = %s AND parent_title = %s ", (qc_code, del_title, del_p_title))
        mysql.connection.commit()
        cur.close()
        flash('Content Deleted! ', 'success')
        return redirect(url_for('admin.case_labels', qccode=qc_code))

    flash('Something Wrong! ', 'danger')
    return redirect(url_for('admin.case_labels', qccode=qc_code))


@adminApp.route('/editcase/<string:qccode>', methods=['GET', 'POST'])
@is_logged_in
def edit_case(qccode):
    basic_form = case(request.form)
    order_form = order_info(request.form)

    agent_list = user_select_list('user_mgmt', 'agent')
    guide_list = user_select_list('user_mgmt', 'guide')
    staffs = user_select_list('user_mgmt', 'all')

    order_form.agent.choices = agent_list
    order_form.tour_guide.choices = guide_list
    order_form.other_staffs.choices = staffs
    basic_form.source.choices = case_source_s

    if request.method == 'GET':
        cur = mysql.connection.cursor()
        get_basic_str = 'SELECT source,source_subject,content,ivsg_result FROM basic_info WHERE qc_num = "{}"'.format(qccode)
        get_basic_result = cur.execute(get_basic_str)
        if get_basic_result:
            get_basic = cur.fetchone()
            # basic info
            basic_form.source.data = get_basic['source']
            basic_form.source_subject.data = get_basic['source_subject']
            basic_form.content.data = get_basic['content']
            basic_form.ivsg_result.data = get_basic['ivsg_result']

        get_order_str = 'SELECT agent,order_num,invoice,departure_date,room_num,tour_guide,tour_code,group_code,pax,staffs FROM order_info WHERE qc_num = "{}"'.format(qccode)
        get_order_result = cur.execute(get_order_str)
        if get_order_result:
            get_order = cur.fetchone()
            # order info
            basic_form.qc_num.data = qccode
            order_form.agent.data = get_order['agent']
            order_form.order_num.data = get_order['order_num']
            order_form.invoice_num.data = get_order['invoice']
            order_form.dept_date.data = datetime.strptime(get_order['departure_date'],'%Y-%m-%d')
            order_form.rm_num.data = get_order['room_num']
            order_form.tour_guide.data = get_order['tour_guide']
            order_form.tour_code.data = get_order['tour_code']
            order_form.group_code.data = get_order['group_code']
            order_form.pax.data = get_order['pax']
            staffs = get_order['staffs'].split(';')

        return render_template('editcase.html', basic=basic_form, order=order_form, qc_num=qccode, staffs=staffs)

    if request.method == 'POST' and basic_form.validate() and order_form.validate():
        # # basic info
        source = basic_form.source.data
        source_subject = transferContent(basic_form.source_subject.data)
        content = transferContent(basic_form.content.data)
        ivsg_result = transferContent(basic_form.ivsg_result.data)
        # # order info
        agent = order_form.agent.data
        order_num = order_form.order_num.data
        invoice = order_form.invoice_num.data
        dept_date = order_form.dept_date.data
        room_num = float(order_form.rm_num.data)
        tour_guide = order_form.tour_guide.data
        guide_id = order_form.tour_guide.data
        tour_code = order_form.tour_code.data.replace(" ", "")
        group_code = order_form.group_code.data.replace(" ", "")
        pax = order_form.pax.data
        staffs = ''.join(request.form.getlist('handles[]'))

        comment = transferContent(request.form['e_case_msg'])
        current_user = session['username']
        # Execute
        cur = mysql.connection.cursor()
        cur.execute(
            "UPDATE basic_info SET source=%s, source_subject=%s, content=%s, ivsg_result=%s WHERE qc_num=%s",
            (source, source_subject, content, ivsg_result, qccode))

        order_str = "UPDATE order_info SET agent='{}', order_num='{}', invoice='{}', departure_date='{}', room_num={}, tour_guide='{}', guide_id='{}', staffs='{}', tour_code='{}', group_code='{}', pax={} WHERE qc_num='{}'" \
            .format(agent, order_num, invoice, dept_date, room_num, tour_guide, guide_id, staffs, tour_code,
                    group_code, pax, qccode)
        cur.execute(order_str)
        mysql.connection.commit()

        if comment != ''and comment != 'null':
            comment_str = "INSERT INTO mdfy_comments (cmt_user, cmt_content, qc_num, type) VALUES('{}','{}','{}','{}')" \
                .format(current_user, comment, qccode, 'edit')
            cur.execute(comment_str)
        # close connection
        cur.close()
        flash('Updated!', 'success')
        return redirect(url_for('admin.case_list'))

    msg = 'Something Wrong!'
    return render_template('editcase.html', msg=msg, basic=basic_form, order=order_form)


class result_info(Form):
    result = TextAreaField('最终处理结果')
    payment = SelectField('退款方式')
    payment_memo = TextAreaField('退款信息')
    compensation = DecimalField('退款金额', default=0)
    resp_party = SelectField('责任归属方')
    satisfaction = SelectField('客户满意度')
    bill = SelectField('开账单')
    bill_value = DecimalField('账单金额',default=0)
    bill_num = StringField('账单号')
    reference = SelectField('处理依据')
    analysis = TextAreaField('案件分析')

def is_code_exist(cur, code, table):
    search_str = 'SELECT qc_num FROM {} WHERE qc_num = "{}"'.format(table, code)
    search_result = cur.execute(search_str)
    if search_result:
        return 1
    else:
        return 0


@adminApp.route('/caseresult/<string:qccode>', methods=['GET', 'POST'])
@is_logged_in
def case_result(qccode):
    result_form = result_info(request.form)

    result_form.payment.choices = case_payment_s
    result_form.resp_party.choices = case_resp_party_s
    result_form.satisfaction.choices = case_satisfaction_s
    result_form.bill.choices = dept_category
    result_form.reference.choices = case_reference_s

    if request.method == 'GET':
        cur = mysql.connection.cursor()
        if is_code_exist(cur, qccode, 'result_info'):
            get_result_str = 'SELECT * FROM result_info WHERE qc_num = "{}"'.format(qccode)
            get_case_result = cur.execute(get_result_str)
            if get_case_result:
                get_result = cur.fetchone()
                # result info
                result_form.result.data = get_result['result']
                result_form.payment.data = get_result['payment']
                result_form.payment_memo.data = get_result['payment_memo']
                result_form.compensation.data = get_result['compensation_amount']
                result_form.resp_party.data = get_result['resp_party']
                result_form.satisfaction.data = get_result['satisfaction']
                result_form.bill.data = get_result['bill']
                result_form.bill_num.data = get_result['bill_num']
                result_form.bill_value.data = get_result['bill_value']
                result_form.reference.data = get_result['reference']
                result_form.analysis.data = get_result['analysis']

            cur.close()
            return render_template('caseresult.html', result=result_form, qc_num=qccode)
        else:
            cur.close()
            return render_template('caseresult.html', result=result_form, qc_num=qccode)

    if request.method == 'POST' and result_form.validate():
        # # result info
        result = transferContent(result_form.result.data)
        payment = result_form.payment.data
        payment_memo = transferContent(result_form.payment_memo.data)
        compensation = result_form.compensation.data
        resp_party = result_form.resp_party.data
        satisfaction = result_form.satisfaction.data
        bill = result_form.bill.data
        bill_num = result_form.bill_num.data
        bill_value = result_form.bill_value.data
        reference = result_form.reference.data
        analysis = transferContent(result_form.analysis.data)

        #current_user = session['username']
        # Execute
        cur = mysql.connection.cursor()
        if is_code_exist(cur, qccode, 'result_info'):
            result_str = "UPDATE result_info SET result='{}', payment='{}', payment_memo='{}', compensation_amount={}, resp_party='{}', satisfaction='{}', bill='{}', bill_num='{}', bill_value={}, reference='{}', analysis='{}' WHERE qc_num='{}'" \
                .format(result, payment, payment_memo, compensation, resp_party, satisfaction, bill, bill_num,bill_value, reference, analysis, qccode)
            cur.execute(result_str)
            mysql.connection.commit()
        else:
            result_str = "INSERT INTO result_info (qc_num, result, payment, payment_memo, compensation_amount, resp_party, satisfaction, bill, bill_num, bill_value, reference, analysis )" \
                         "VALUES ('{}', '{}', '{}', '{}', {}, '{}', '{}', '{}', '{}', {}, '{}', '{}')"\
                .format(qccode, result, payment, payment_memo, compensation, resp_party, satisfaction, bill, bill_num,bill_value, reference, analysis)

            cur.execute(result_str)
            mysql.connection.commit()
        # close connection
        cur.close()
        flash('Updated!', 'success')
        return redirect(url_for('admin.case_list'))

    msg = 'Something Wrong!'
    return render_template('caseresult.html', msg=msg, result=result_form, qc_num='')

class case_attachment_form(Form):
    comments = TextAreaField('备注')
    name = StringField('附件名', [validators.InputRequired(message='请输入附件名')])
    url = StringField('附件URL', [validators.InputRequired(message='请输入URL')])

@adminApp.route('/caseattachment/<string:qccode>', methods=['GET', 'POST'])
@is_logged_in
def case_attachment(qccode):
    attach_form = case_attachment_form(request.form)
    attach_user = session['username']

    if request.method == 'GET':
        cur = mysql.connection.cursor()
        get_result_str = 'SELECT name,date,user,url,comment,id FROM attachment WHERE qc_num = "{}"'.format(qccode)
        get_atch_result = cur.execute(get_result_str)
        if get_atch_result:
            attachments = cur.fetchall()
            cur.close()
            return render_template('caseattachment.html', attachments=attachments, form=attach_form, qc_num=qccode)
        else:
            cur.close()
            return render_template('caseattachment.html', attachments=0, form=attach_form, qc_num=qccode)
    if request.method == 'POST' and attach_form.validate():

        name = transferContent(attach_form.name.data)
        url = attach_form.url.data
        comment = transferContent(attach_form.comments.data)

        cur = mysql.connection.cursor()
        get_result_str = 'INSERT INTO attachment (name,user,url,comment,qc_num) VALUES ("{}","{}","{}","{}","{}")'.format(name,attach_user,url,comment,qccode)
        cur.execute(get_result_str)
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('admin.case_list'))

    msg = 'Something Wrong! Please check the form and re-submit！'
    return render_template('caseattachment.html', attachments=0, form=attach_form, qc_num=qccode)



@adminApp.route('/deleteattachment/<string:id>&<string:qc_num>')
@is_logged_in
def delete_attachment(id,qc_num):
    if qc_num != 'NULL':
        # Create Cursor
        cur = mysql.connection.cursor()
        # Execute
        result = cur.execute("DELETE FROM attachment WHERE qc_num = %s AND id = %s", (qc_num, id))
        if result:
            mysql.connection.commit()
            cur.close()
            flash('Content Deleted! ', 'success')
            return redirect(url_for('admin.case_attachment', qccode=qc_num))
        else:
            cur.close()
            flash('Something Wrong! ', 'danger')
            return redirect(url_for('admin.case_attachment', qccode=qc_num))

    flash('Something Wrong! ', 'danger')
    return redirect(url_for('admin.case_attachment', qccode=qc_num))

@adminApp.route('/casesearch', methods=['GET', 'POST'], defaults={'pagenum': 1, 'kw':'null'})
@adminApp.route('/casesearch&page=<int:pagenum>&<string:kw>')
@is_logged_in
def case_search(pagenum, kw):
    page = int(pagenum) - 1
    keyword = kw
    if request.method == 'POST':
        keyword = request.form['search_case']

    pageCur = mysql.connection.cursor()
    page_str = "SELECT bi.qc_num, status, creat_date, agent, invoice " \
               "FROM basic_info AS bi, order_info AS oi " \
               "WHERE bi.qc_num = oi.qc_num AND bi.status NOT IN ('cancel','terminated') " \
               "AND (bi.qc_num LIKE '%" + keyword + "%' OR oi.invoice LIKE '%" + keyword +"%' " \
               "OR oi.order_num LIKE '%" + keyword +"%')"
    totalResults = pageCur.execute(page_str)
    totalPages = totalResults / 10
    pageCur.close()

    cur = mysql.connection.cursor()
    str = "SELECT bi.qc_num, status, creat_date, agent, invoice " \
            "FROM basic_info AS bi, order_info AS oi " \
            "WHERE bi.qc_num = oi.qc_num AND bi.status NOT IN ('cancel','terminated') " \
            "AND (bi.qc_num LIKE '%" + keyword + "%' OR oi.invoice LIKE '%" + keyword +"%' " \
            "OR oi.order_num LIKE '%" + keyword +"%')" \
            "LIMIT {}, {}".format(page * 10, 10)
    result = cur.execute(str)
    if result > 0:
        listItems = cur.fetchall()
        cur.close()
        return render_template('casesearch.html', caseinfos=listItems, pages=ceil(totalPages), keyword=keyword)
    else:
        cur.close()
        msg = 'No Content Found'
        return render_template('casesearch.html', msg=msg, pages=1,keyword=keyword)


@adminApp.route('/casedetails/<string:qc_num>')
@is_logged_in
def case_details(qc_num):
    b_result = 0
    o_result = 0
    l_result = 0
    comments_result = 0
    r_result = 0
    s_result = 0
    b_dataset =0
    o_dataset = 0
    l_dataset = 0
    comments_dataset = 0
    r_dataset = 0
    s_dataset = 0

    if qc_num != '' and qc_num != '':
        cur = mysql.connection.cursor()

        b_info_str = 'SELECT * FROM basic_info WHERE qc_num = "{}"'.format(qc_num)
        o_info_str = 'SELECT * FROM order_info WHERE qc_num = "{}"'.format(qc_num)
        l_info_str = 'SELECT * FROM label_info WHERE qc_num = "{}"'.format(qc_num)
        comments_str = 'SELECT * FROM mdfy_comments WHERE qc_num = "{}" AND type = "{}"'.format(qc_num, 'processing')
        r_info_str = 'SELECT * FROM result_info WHERE qc_num = "{}"'.format(qc_num)
        status_str = 'SELECT * FROM mdfy_comments WHERE qc_num = "{}" AND type = "{}"'.format(qc_num, 'status')

        b_result = cur.execute(b_info_str)
        if b_result:
            b_dataset = cur.fetchone()

            o_result = cur.execute(o_info_str)
            if o_result:
                o_dataset = cur.fetchone()
                agentname_str = 'SELECT name FROM user_mgmt WHERE id = "{}"'.format(o_dataset['agent'])
                guidename_str = 'SELECT name FROM user_mgmt WHERE id = "{}"'.format(o_dataset['tour_guide'])
                if cur.execute(agentname_str):
                    o_dataset['agent'] = cur.fetchone()['name']
                if cur.execute(guidename_str):
                    o_dataset['tour_guide'] = cur.fetchone()['name']

            l_result = cur.execute(l_info_str)
            if l_result:
                l_dataset = cur.fetchall()
            comments_result = cur.execute(comments_str)
            if comments_result:
                comments_dataset = cur.fetchall()
            r_result = cur.execute(r_info_str)
            if r_result:
                r_dataset = cur.fetchone()
            s_result = cur.execute(status_str)
            if s_result:
                s_dataset = cur.fetchall()

            cur.close()
            return render_template('casedetails.html', qc_num=qc_num, basic=b_dataset, order=o_dataset,label=l_dataset, comments=comments_dataset, results=r_dataset, status=s_dataset)

        cur.close()
        msg = 'No Content Found'
        return redirect(url_for('admin.case_list', msg=msg))

    msg = 'Something Wrong'
    return redirect(url_for('admin.case_list', msg=msg))

### 巴士，酒店等其他信息 ###
class otherInfoBus(Form):
    o_date = DateField('使用日期',[validators.InputRequired(message='请选择日期')], format='%Y-%m-%d')
    o_type = SelectField('资源类型',[validators.InputRequired(message='请选择资源类型')])
    o_info = StringField('资源内容')
    o_comments = TextAreaField('备注')


@adminApp.route('/caseotherinfo/', methods=['GET', 'POST'], defaults={'qccode': 'NULL'})
@adminApp.route('/caseotherinfo/<string:qccode>', methods=['GET', 'POST'])
@is_logged_in
def case_other_info(qccode):
    other_info = otherInfoBus(request.form)
    other_info.o_type.choices = other_type_list
    if request.method == 'POST' and qccode != 'NULL' and other_info.validate():
        o_date = datetime.combine(other_info.o_date.data, datetime.min.time())
        o_type = other_info.o_type.data
        o_info = other_info.o_info.data
        o_cmts = other_info.o_comments.data
        o_user = session['username']

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO other_info (src_user, src_name, src_cmts, src_date, src_type, qc_num)"
                    "VALUES(%s,%s,%s,%s,%s,%s)", (o_user, o_info, o_cmts, o_date, o_type, qccode))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('admin.case_other_info', qccode=qccode))

    elif request.method == 'GET' and qccode != 'NULL':
        cur = mysql.connection.cursor()
        case_labels_str = "SELECT src_name,src_cmts, DATE(src_date) AS date,src_type,id, qc_num FROM other_info WHERE qc_num='{}' ORDER BY date".format(qccode)
        if cur.execute(case_labels_str):
            case_labels_results = cur.fetchall()
            cur.close()
            return render_template('caseotherinfo.html', other_info=other_info, source=case_labels_results)
        else:
            cur.close()

            return render_template('caseotherinfo.html', other_info=other_info, source=0)
    else:
        msg = 'Something Wrong！Please check the form！'
        return render_template('caseotherinfo.html',msg=msg, other_info=other_info, source=0)

@adminApp.route('/otherinfoinput', methods=['GET'])
@is_logged_in
def other_info_input():
    search = request.args.get('oinfo')
    # Create Cursor
    cur = mysql.connection.cursor()
    # Execute
    if cur.execute("SELECT name FROM user_mgmt "
                         "WHERE (name like '%" + search + "%' AND type='bus' AND is_using = 1) "
                          "OR (name like '%" + search + "%' AND type='hotel' AND is_using = 1) ") :
        auto_result = cur.fetchall()
        # close connection
        cur.close()
        result_list = []
        for a in auto_result:
            result_list.append(a['name'])
        return jsonify(matching_result=result_list)

    return jsonify(matching_result=['没有结果'])

@adminApp.route('/deletecaseother/', defaults={'code': 'NULL'})
@adminApp.route('/deletecaseother/<string:code>')
@is_logged_in
def delete_case_other(code):
    qc_num = ''
    if code != 'NULL' and code != '':
        qc_num = code.split(':')[1]
        del_id = code.split(':')[0]
        # Create Cursor
        cur = mysql.connection.cursor()
        # Execute
        result = cur.execute("DELETE FROM other_info WHERE id = %s", [del_id])
        mysql.connection.commit()
        cur.close()
        flash('Content Deleted! ', 'success')
        return redirect(url_for('admin.case_other_info', qccode=qc_num))

    msg = 'Something Wrong! '
    return redirect(url_for('admin.case_list', msg=msg))

# ##### processing case end #####

# ##### account begin #####
# ##### account end #####