from flask import Flask, render_template, request, redirect, url_for, send_file
import yaml
import os
import subprocess
from subprocess import PIPE, run

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    overall_score = None  # Initialize the variable to store the overall score

    # Check if ratings.log exists, if not create it
    log_filename = 'ratings.log'
    if not os.path.exists(log_filename):
        with open(log_filename, 'w') as f:
            pass  # Create an empty file
   
    if request.method == 'POST':
        # Load existing YAML config
        with open('employ.yaml', 'r') as f:
            config = yaml.safe_load(f)
    
        # Update only the keys that are present in the form and are not empty
        if request.form['business_name']:
            config['business_name'] = request.form['business_name']
        if request.form['location']:
            config['location'] = request.form['location']
    
        config['yelp']['weight'] = float(request.form['yelp_weight']) if request.form['yelp_weight'] else None
        config['turnover']['rate'] = int(request.form['turnover_rate']) if request.form['turnover_rate'] else None
        config['turnover']['weight'] = float(request.form['turnover_weight']) if request.form['turnover_weight'] else None
        config['credit_score']['score'] = int(request.form['credit_score']) if request.form['credit_score'] else None
        config['credit_score']['weight'] = float(request.form['credit_weight']) if request.form['credit_weight'] else None
        config['bbb']['weight'] = float(request.form['bbb_weight']) if request.form['bbb_weight'] else None
        config['google']['weight'] = float(request.form['google_weight']) if request.form['google_weight'] else None
    
        # Save updated YAML config
        with open('employ.yaml', 'w') as f:
            yaml.safe_dump(config, f)
        
        # Run your existing Python code and capture the output
        result = run(["python", "main.py"], stdout=PIPE, stderr=PIPE, universal_newlines=True)
        output = result.stdout

        # Extract the overall score from the output
        for line in output.split('\n'):
            if "The overall score for the business is" in line:
                overall_score = line.split("is")[1].strip()
        
        # Redirect to the same page to display the updated values
        return redirect(url_for('index', overall_score=overall_score))
    
    # Load existing YAML config
    with open('employ.yaml', 'r') as f:
        config = yaml.safe_load(f)
        
    # Load the content of ratings.log
    with open(log_filename, 'r') as f:
        log_content = f.read()
        
    # Load the content of api_details.log
    api_details_content = ""
    if os.path.exists('api_details.log'):
        with open('api_details.log', 'r') as f:
           api_details_content = f.read()
                
    # Load the content of overall_score.txt
    with open('overall_score.txt', 'r') as f:
        overall_score = f.read()

    return render_template('index.html', config=config, log_content=log_content, api_details_content=api_details_content, overall_score=overall_score)

@app.route('/clear_ratings_log', methods=['POST'])
def clear_ratings_log():
    with open('ratings.log', 'w') as f:
        f.write("")
    return redirect(url_for('index'))

@app.route('/clear_api_details_log', methods=['POST'])
def clear_api_details_log():
    with open('api_details.log', 'w') as f:
        f.write("")
    return redirect(url_for('index'))

@app.route('/download_ratings_log')
def download_ratings_log():
    return send_file('ratings.log', as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
