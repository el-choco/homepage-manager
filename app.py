import os
from flask import Flask, render_template, request, redirect, url_for, session
from ruamel.yaml import YAML

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'default_secret_key_replace_in_production')

YAML_BASENAMES = ['services', 'settings', 'widgets', 'bookmarks', 'docker', 'kubernetes', 'proxmox']
TEXT_FILES = ['custom.css', 'custom.js']

yaml = YAML()
yaml.preserve_quotes = True
yaml.indent(mapping=4, sequence=4, offset=2)
yaml.width = 4096

def get_actual_filename(basename):
    if os.path.exists(f"{basename}.yaml"):
        return f"{basename}.yaml"
    if os.path.exists(f"{basename}.yml"):
        return f"{basename}.yml"
    return f"{basename}.yaml"

def load_all_configs():
    all_data = {}
    for basename in YAML_BASENAMES:
        filename = get_actual_filename(basename)
        if os.path.exists(filename):
            with open(filename, 'r', encoding='utf-8') as f:
                content_str = f.read()
                f.seek(0)
                parsed_data = yaml.load(f) or {}
                all_data[filename] = {
                    'type': 'yaml',
                    'parsed': parsed_data,
                    'raw': content_str
                }
        else:
            all_data[filename] = None

    for filename in TEXT_FILES:
        if os.path.exists(filename):
            with open(filename, 'r', encoding='utf-8') as f:
                content_str = f.read()
                all_data[filename] = {
                    'type': 'text',
                    'raw': content_str
                }
        else:
            all_data[filename] = {
                'type': 'text',
                'raw': ''
            }
    return all_data

@app.before_request
def require_login():
    allowed_routes = ['login', 'static']
    if request.endpoint not in allowed_routes and not session.get('logged_in'):
        return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username == os.environ.get('APP_USER', 'admin') and password == os.environ.get('APP_PASS', 'admin'):
            session['logged_in'] = True
            return redirect(url_for('index'))
        else:
            error = 'Invalid Credentials'
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))

@app.route('/')
def index():
    configs = load_all_configs()
    active_tab = request.args.get('active_tab')
    return render_template('index.html', configs=configs, active_tab=active_tab)

@app.route('/save_text/<filename>', methods=['POST'])
def save_text(filename):
    if filename not in TEXT_FILES:
        return "Invalid file", 400
    content = request.form.get('content', '')
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
    return redirect(url_for('index', active_tab=filename))

@app.route('/action/<filename>', methods=['POST'])
def handle_action(filename):
    if filename not in [get_actual_filename(b) for b in YAML_BASENAMES]:
        return "Invalid configuration file", 400
        
    action_type = request.form.get('action_type')
    item_path = request.form.get('item_path', '')
    item_data = request.form.get('item_data', '')
    
    with open(filename, 'r', encoding='utf-8') as f:
        data = yaml.load(f)
        
    if data is None:
        if 'services' in filename or 'bookmarks' in filename or 'widgets' in filename:
            data = []
        else:
            data = {}

    try:
        parsed_input = yaml.load(item_data) if item_data else None
    except:
        parsed_input = item_data

    if action_type == 'add_category':
        if isinstance(data, list) and isinstance(parsed_input, dict):
            data.append(parsed_input)
        elif isinstance(data, dict) and isinstance(parsed_input, dict):
            data.update(parsed_input)
    
    elif action_type == 'add_item':
        if isinstance(data, list):
            for group in data:
                if isinstance(group, dict) and item_path in group:
                    if isinstance(group[item_path], list):
                        group[item_path].append(parsed_input)
                    elif group[item_path] is None:
                        group[item_path] = [parsed_input]
        elif isinstance(data, dict):
            if item_path in data:
                if isinstance(data[item_path], list):
                    data[item_path].append(parsed_input)
                elif data[item_path] is None:
                    data[item_path] = [parsed_input]
    
    elif action_type == 'edit_item':
        if isinstance(data, list):
            for group in data:
                if isinstance(group, dict):
                    for cat, items in group.items():
                        if isinstance(items, list):
                            for j, item in enumerate(items):
                                if isinstance(item, dict) and item_path in item:
                                    items[j] = {item_path: parsed_input}
        elif isinstance(data, dict):
            if item_path in data:
                data[item_path] = parsed_input
            elif 'layout' in data and isinstance(data['layout'], dict) and item_path in data['layout']:
                data['layout'][item_path] = parsed_input

    elif action_type == 'delete_item':
        if isinstance(data, list):
            target_group = None
            for group in data:
                if isinstance(group, dict) and item_path in group:
                    target_group = group
                    break
            
            if target_group is not None:
                data.remove(target_group)
            else:
                for group in data:
                    if isinstance(group, dict):
                        for cat, items in group.items():
                            if isinstance(items, list):
                                target_item = None
                                for i in items:
                                    if isinstance(i, dict) and item_path in i:
                                        target_item = i
                                        break
                                if target_item is not None:
                                    items.remove(target_item)
        elif isinstance(data, dict):
            if item_path in data:
                del data[item_path]
            elif 'layout' in data and isinstance(data['layout'], dict) and item_path in data['layout']:
                del data['layout'][item_path]

    with open(filename, 'w', encoding='utf-8') as f:
        yaml.dump(data, f)
        
    return redirect(url_for('index', active_tab=filename))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3335, debug=True)