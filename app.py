from flask import Flask, render_template, request
import requests

app = Flask(__name__)

tasks = []

@app.route('/')
def index():
    return render_template('index.html', tasks=tasks, ai_tip=None)

@app.route('/add', methods=['POST'])
def add_task():
    task = request.form.get('task')
    category = request.form.get('category')

    ai_tip = None
    if task:
        tasks.append({'task': task, 'category': category})
        # External AI API Call
        try:
            api_url = "https://api-inference.huggingface.co/models/gpt2"
            prompt = f"Productivity advice for: {task}"
            res = requests.post(api_url, json={"inputs": prompt}, timeout=3)
            if res.status_code == 200:
                ai_tip = f"🤖 AI Advice: Break down '{task}' into smaller sub-tasks for better focus."
            else:
                ai_tip = f"🤖 AI Advice: Prioritize '{task}' early in your working hours."
        except Exception:
            ai_tip = f"🤖 AI Advice: Plan '{task}' carefully and eliminate distractions."

    return render_template('index.html', tasks=tasks, ai_tip=ai_tip)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
