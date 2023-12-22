# editor_web.py
from flask import Flask, render_template, request, jsonify, redirect, url_for
import os
import yaml

app = Flask(__name__)

def get_yaml_files():
    """
    Get a list of YAML files in the current directory.

    Returns:
        list: List of YAML file names.
    """
    files = [f for f in os.listdir('./') if f.endswith('.yaml')]
    return files

def load_yaml(file_path):
    """
    Load YAML data from a file.

    Args:
        file_path (str): Path to the YAML file.

    Returns:
        dict: Loaded YAML data.
    """
    with open(file_path, 'r') as file:
        data = yaml.safe_load(file)
    return data

def save_yaml(file_path, data):
    """
    Save YAML data to a file.

    Args:
        file_path (str): Path to the YAML file.
        data (dict): Data to be saved.
    """
    with open(file_path, 'w') as file:
        yaml.dump(data, file, default_flow_style=False)

def convert_form_data(form_data):
    """
    Convert form data to a dictionary.

    Args:
        form_data (ImmutableMultiDict): Form data received from a POST request.

    Returns:
        dict: Converted dictionary.
    """
    data = []

    for key, value in form_data.items():
        temp_key = key.replace('data[', '').replace(']', '')
        temp_key = temp_key.split('[')
        if temp_key[0] == 'file':
            continue

        data.append((temp_key, [convert_value(value[0])]))

    result = {}
    for keys, values in data:
        current_level = result
        for i, key in enumerate(keys):
            if i == len(keys) - 1:
                current_level[key] = values[0] if len(values) == 1 else values
            else:
                current_level = current_level.setdefault(key, {})

    return result

def convert_value(value):
    """
    Convert a string value to an appropriate Python type.

    Args:
        value (str): Input string.

    Returns:
        int, float, bool, or str: Converted value.
    """
    try:
        return int(value) if value.isdigit() else float(value)
    except ValueError:
        if value == 'true':
            return True
        elif value == 'false':
            return False
        else:
            return value

@app.route('/')
def home():
    """
    Render the home page.

    Returns:
        render_template: Home page template.
    """
    yaml_files = get_yaml_files()
    return render_template('index.html', yaml_files=yaml_files)

@app.route('/edit', methods=['POST'])
def edit():
    """
    Handle the edit POST request.

    Returns:
        jsonify: JSON response with the YAML data.
    """
    file_name = request.form['file']
    file_path = os.path.join('./', file_name)
    data = load_yaml(file_path)
    return jsonify(data)

@app.route('/save', methods=['POST'])
def save():
    """
    Handle the save POST request.

    Returns:
        redirect or str: Redirect to home page on success, or error message on failure.
    """
    file_name = request.form['file']
    file_path = os.path.join('./', file_name)
    
    try:
        form_data = request.form.to_dict(flat=False)
        data = convert_form_data(form_data)
        save_yaml(file_path, data)
        return redirect(url_for('home'))
    except Exception as e:
        print(e)
        return "Error saving data"

if __name__ == '__main__':
    app.run(debug=True)