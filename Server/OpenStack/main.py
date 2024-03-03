from flask import Flask, render_template, request, redirect, session, url_for, flash, json, jsonify
from flask_mysqldb import MySQL
from datetime import datetime
from flask_socketio import SocketIO,emit
import threading
import MySQLdb.cursors
import func, time
import hashlib
import ast

app = Flask(__name__)
app.config['SECRET_KEY'] = "minh"
socketio = SocketIO(app, cors_allowed_origins="*")

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'openstack'
mysql = MySQL(app)

# Template
@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/login', methods =['GET', 'POST'])
def login():
    if 'loggedin' in session:
        return redirect(url_for('index'))
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        hashPass = hashlib.shake_256(password.encode('utf-8')).hexdigest(10)
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE username = % s AND password = % s', (username, hashPass,))
        account = cursor.fetchone()
        if account:
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']
            session['fullname'] = account['fullname']
            return redirect(url_for('index'))
        else:
            msg = 'Thông tin đăng nhập không chính xác !'

    return render_template('login.html', msg=msg)

@app.route('/register', methods =['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'fullname' in request.form:
        username = request.form['username']
        password = request.form['password']
        hashPass = hashlib.shake_256(password.encode('utf-8')).hexdigest(10)
        fullname = request.form['fullname']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE username = % s', (username,))
        account = cursor.fetchone()
        if account:
            msg = 'Tài khoản đã tồn tại !'
        elif not username or not password or not fullname:
            msg = 'Xin hãy điền đủ thông tin !'
        else:
            cursor.execute('INSERT INTO users VALUES (NULL, %s, %s, %s)', (username, hashPass, fullname,))
            mysql.connection.commit()
            msg = 'Đăng ký thành công !'
            return redirect(url_for('login'))
    elif request.method == 'POST':
        msg = 'Xin hãy điền đủ thông tin !'
    return render_template('register.html', msg=msg)

@app.route('/')
def index():
    if 'loggedin' in session:
        data = func.get_instances()
        datalen = len(data['servers'])
        sidebar1 = "active"

        images = func.get_images()
        flavors = func.get_flavors()

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM quyentruycap')
        pms = cursor.fetchall()

        return render_template("index.html",
                               data = data,
                               datalen = datalen,
                               sidebar1 = sidebar1,
                               pms = pms,
                               images = images,
                               flavors = flavors)
    else:
        return redirect(url_for('login'))

@app.route('/pm')
def pm():
    msg = ''
    sidebar2 = "active"
    if 'loggedin' in session:
        data = func.get_instances()

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM mayvatly')
        pms = cursor.fetchall()

        cursor.execute('SELECT * FROM quyentruycap')
        request_access = cursor.fetchall()

        return render_template("PM.html",
                               data = data,
                               msg=msg,
                               sidebar2 = sidebar2,
                               pms = pms,
                               request_access = request_access)
    else:
        return redirect(url_for('login'))

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 400

@app.errorhandler(500)
def page_not_found(e):
    return render_template("500.html"), 500

# Function
@app.route('/create_pm', methods =['GET', 'POST'])
def create_pm():
    if request.method == 'POST' and 'name' in request.form and 'MAC_addr' in request.form:
        name = request.form['name']
        MAC_addr = request.form['MAC_addr'].lower()
        hashMAC = hashlib.shake_256(MAC_addr.encode('utf-8')).hexdigest(10)

        time_created = datetime.now()
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM mayvatly WHERE  MAC_addr = % s', (hashMAC,))
        account = cursor.fetchone()
        if account:
            flash('Máy tính vật lý đã tồn tại !')
            return redirect(url_for('pm'))
        elif not name or not MAC_addr:
            flash('Xin hãy điền đủ thông tin !')
            return redirect(url_for('pm'))
        else:
            cursor.execute('INSERT INTO mayvatly VALUES (NULL, %s, %s, %s)', (name, hashMAC, time_created))
            mysql.connection.commit()
            flash('Thêm thành công !')
            return redirect(url_for('pm'))
    flash('Xảy ra lỗi trong quá trình tạo !')
    return redirect(url_for('pm'))

@app.route('/request_access', methods =['GET', 'POST'])
def request_access():
    if 'loggedin' in session:
        time_created = datetime.now()
        username = ""
        password = ""

        if request.method == 'POST' and 'select_VM' in request.form and 'select_PM' in request.form:
            select_VM = ast.literal_eval(request.form['select_VM'])
            VM_id = list(select_VM.keys())[0]
            obj_id = list(select_VM.values())[0]
            VM_name = obj_id[0]
            ip_addr = obj_id[1]

            select_PM = ast.literal_eval(request.form['select_PM'])
            mac_addr = list(select_PM.keys())[0]
            PM_name = list(select_PM.values())[0]

            if not select_VM:
                flash("Không có máy ảo để cấp quyền!")
                return redirect(url_for('pm'))
            elif not select_PM:
                flash("Không có máy vật lý để cấp quyền!")
                return redirect(url_for('pm'))

            account = {
                "FIT1": "123456",
                "FIT": "123456",
            }

            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM quyentruycap WHERE VM_id = %s', (VM_id,))
            check_VM = cursor.fetchall()

            cursor.execute('SELECT * FROM quyentruycap WHERE mac_addr = %s', (mac_addr,))
            check_PM = cursor.fetchone()

            cursor.execute('SELECT * FROM quyentruycap WHERE VM_id = %s and mac_addr = %s', (VM_id, mac_addr))
            check_Request = cursor.fetchone()


            for i in range(len(list(account.keys()))):
                check_username = list(account.keys())[i]
                check_password = list(account.keys())[i]
                cursor.execute('SELECT * FROM quyentruycap WHERE username = %s and password = %s and VM_id = %s', (check_username, check_password, VM_id, ))
                check_Account = cursor.fetchone()
                if not check_Account:
                    username = list(account.keys())[i]
                    password = account[username]
            if len(check_VM) > 1 and username == "" and password == "":
                flash('Máy ảo đã cấp đủ tài khoản, Xin hãy chọn máy ảo khác!')
            elif check_Request:
                flash('Máy vật lý đã tồn tại quyền truy cập vào máy ảo này! Vui lòng thử lại!')
            elif check_PM:
                flash('Máy vật lý này đã được cấp quyền truy cập vào máy ảo! Hãy chọn máy vật lý khác')
            else:
                cursor.execute('INSERT INTO quyentruycap VALUES (NULL, %s, %s, %s, %s, %s, %s, %s, NULL, %s)', (VM_id, VM_name, PM_name, username, password, ip_addr, mac_addr, time_created ))
                mysql.connection.commit()
                flash('Cấp quyền thành công !')
        elif 'select_VM' not in request.form:
            flash("Không tìm thấy máy ảo để cấp quyền!")
        elif 'select_PM' not in request.form:
            flash("Không tìm thây máy vật lý để cấp quyền!")
        return redirect(url_for('pm'))

@app.route('/delete_access_vm', methods =['GET', 'POST'])
def delete_access_vm():
    if request.method == 'POST' and 'id' in request.form:
        access_id = request.form['id']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('DELETE FROM quyentruycap WHERE id = %s', (access_id,))
        mysql.connection.commit()
        flash('Xóa thành công !')
    return redirect(url_for('index'))

@app.route('/delete_access_pm', methods =['GET', 'POST'])
def delete_access_pm():
    if request.method == 'POST' and 'id' in request.form:
        access_id = request.form['id']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('DELETE FROM quyentruycap WHERE id = %s', (access_id,))
        mysql.connection.commit()
        flash('Xóa thành công !')
        return redirect(url_for('pm'))
    flash('Xóa thất bại! Vui lòng kiểm tra lại hệ thống')
    return redirect(url_for('pm'))

@app.route('/create_vm', methods=['GET', 'POST'])
def create_vm():
    if request.method == 'POST' and 'VM_number' in request.form and 'select_image' in request.form and 'select_flavor' in request.form:
        vm_num = request.form['VM_number']
        select_image = request.form['select_image']
        select_flavor = request.form['select_flavor']
        data = func.get_instances()
        datalen = len(data['servers'])
        if (100 - datalen - int(vm_num)) > 0:
            response_code = func.create_vm(vm_num, select_image, select_flavor)
            if response_code == 202:
                flash("Thêm thành công")
                return redirect(url_for('index'))
            else:
                flash("Thêm thất bại! Vui lòng kiểm tra lại hệ thống")
                return redirect(url_for('index'))
        else:
            flash("Vượt quá số lượng máy ảo. Không thể thêm!")
            return redirect(url_for('index'))
    elif 'select_image' not in request.form:
        flash("Không có hệ điều hành để tạo!")
        return redirect(url_for('index'))
    elif 'vm_num' not in request.form:
        flash("Chưa chọn số lượng máy cần tạo!")
        return redirect(url_for('index'))
    elif 'select_flavor' not in request.form:
        flash("Chưa chọn phần cứng!")
        return redirect(url_for('index'))
    return redirect(url_for('index'))

@app.route('/delete_vm', methods =['GET', 'POST'])
def delete_vm():
    if request.method == 'POST' and 'vm_id' in request.form:
        vm_id = request.form['vm_id']
        delete = func.delete_vm(vm_id)
        if delete == 202:
            flash("Đã xóa máy ảo")
            return redirect(url_for('index'))
        else:
            flash("Có lỗi trong quá trình xóa! Vui lòng kiểm tra lại hệ thống")
            return redirect(url_for('index'))
    flash("Không thể xóa máy ảo!")
    return redirect(url_for('index'))

@app.route('/start_vm', methods=['GET', 'POST'])
def start_vm():
    if request.method == 'POST' and 'select_VM' in request.form:
        select_VM = request.form['select_VM']
        start = func.start_vm(select_VM)
        if start == 202:
            flash("Khởi động thành công")
            return redirect(url_for('index'))
        else:
            flash("Đã xảy ra lỗi trong quá trình khởi động! Hãy kiểm tra lại hệ thống")
            return redirect(url_for('index'))
    return redirect(url_for('index'))

@app.route('/start_all_vm', methods =['GET', 'POST'])
def start_all_vm():
    start_all = func.start_all_vm()
    if start_all == 202:
        flash("Đã khởi động toàn bộ máy ảo")
        return redirect(url_for('index'))
    else:
        flash("Có lỗi trong quá trình khởi động máy ảo! Vui lòng kiểm tra lại hệ thống")
        return redirect(url_for('index'))
    return redirect(url_for('index'))

@app.route('/shutdown_vm', methods =['GET', 'POST'])
def shutdown_vm():
    func.shutdown_vm()
    flash("Đã thực hiện tắt toàn bộ máy ảo! Hãy kiểm tra lại trạng thái máy")
    return redirect(url_for('index'))

@app.route('/delete_pm', methods =['GET', 'POST'])
def delete_pm():
    if request.method == 'POST' and 'id' in request.form:
        pm_id = request.form['id']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('DELETE FROM mayvatly WHERE id = %s', (pm_id,))
        mysql.connection.commit()
        flash('Xóa thành công')
    return redirect(url_for('pm'))

@app.route('/select', methods=['GET', 'POST'])
def select():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    if request.method == 'POST':
        VM_id = request.form['VM_id']
        result = cursor.execute("SELECT * FROM quyentruycap WHERE VM_id = %s", [VM_id])
        PMs = cursor.fetchall()
        PM_list = []
        for pm in PMs:
            PM_dict = {
                    'id': pm['id'],
                    'PM_name': pm['PM_name'],
                    'username': pm['username'],
                    'password': pm['password'],
                    'mac_addr': pm['mac_addr']
            }
            PM_list.append(PM_dict)
        return json.dumps(PM_list)

# Request OpenStack
@app.route('/get_access/<mac_addr>', methods=['GET', 'POST'])
def get_access(mac_addr):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM quyentruycap WHERE mac_addr = %s', (mac_addr,))
    data = cursor.fetchone()
    if data:
        return data
    return {}

@app.route('/get_container/<mac_addr>', methods=['GET', 'POST'])
def get_container(mac_addr):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM container WHERE mac = %s", [mac_addr])
    data = cursor.fetchall()
    if data:
        return jsonify(data)
    return {}

@app.route('/create_snapshot', methods=['GET', 'POST'])
def create_snapshot():
    if request.method == 'POST' and 'select_VM' in request.form and 'snap_name' in request.form:
        select_VM = request.form['select_VM']
        snap_name = request.form['snap_name']
        snapshot = func.create_snapshot(select_VM,snap_name)
        if snapshot == 202:
            flash("Tạo bản sao lưu thành công")
            return redirect(url_for('index'))
        else:
            flash("Có lỗi trong quá trình sao lưu! Vui lòng kiểm tra lại hệ thống")
            return redirect(url_for('index'))
    flash("Không thể sao lưu! Vui lòng kiểm tra lại thông tin nhập vào")
    return redirect(url_for('index'))

# CLIENT REQUEST
@app.route('/get_vm_detail/<vm_id>', methods=['GET', 'POST'])
def get_vm_detail(vm_id):
    data = func.get_vm_detail(vm_id)
    return data
@app.route('/power_on/<vm_id>', methods=['GET', 'POST'])
def power_on(vm_id):
    status = func.start_vm(vm_id)
    return {}
@app.route('/reboot_vm/<vm_id>', methods=['GET', 'POST'])
def reboot_vm(vm_id):
    status = func.reboot_vm(vm_id)
    return {}
@app.route('/get_detail/<vm_id>', methods=['GET', 'POST'])
def get_detail(vm_id):
    vm = func.get_vm_detail(vm_id)
    flavor_id = vm['flavor']['id']
    flavor = func.get_flavor_detail(flavor_id)

    vm_name = vm['name']
    cpu = flavor['vcpus']
    ram = flavor['ram']
    disk = flavor['disk']
    data = [vm_name,cpu,ram,disk]
    return data
# WEB SOCKET
def update_servers_data():
    while True:
        data = func.get_instances()
        socketio.emit('VM_data', data, namespace='/data')
        time.sleep(7)

@socketio.on('connect', namespace='/data')
def data_connect():
    data = func.get_instances()
    emit('VM_data', data)

data_thread = threading.Thread(target=update_servers_data)
data_thread.daemon = True
data_thread.start()
