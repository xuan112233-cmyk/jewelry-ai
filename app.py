"""
11步引导式工作流系统 - 精美动画版
带完整动画效果和流畅交互体验
"""

from flask import Flask, render_template_string, request, session, redirect, url_for, jsonify
from flask_cors import CORS
import json
import hashlib
from pathlib import Path
from datetime import datetime
from functools import wraps
import sys

sys.path.insert(0, str(Path(__file__).parent / "modules"))

app = Flask(__name__)
app.secret_key = 'jewelry-workflow-secret'
CORS(app)

USERS = {
    "admin": {
        "password": hashlib.sha256("admin123".encode()).hexdigest(),
        "email": "admin@jewelry.ai"
    }
}

WORKFLOW_STEPS = [
    {
        "id": 1,
        "title": "美国市场数据采集",
        "desc": "Amazon、TikTok、Pinterest、Instagram",
        "detail": "收集产品图片、销售估算、趋势、消费者需求和评价",
        "icon": "🔍",
        "color": "#FF6B6B"
    },
    {
        "id": 2,
        "title": "建立代表性3D款式素材库",
        "desc": "以Rhino .3dm源文件为主，ZBrush模型为辅",
        "detail": "JewelCAD旧款可导出兼容格式或多角度图片作为参考",
        "icon": "💎",
        "color": "#4ECDC4"
    },
    {
        "id": 3,
        "title": "AI识别、分类及设计元素提取",
        "desc": "通过三视图、渲染图及可读取的几何信息",
        "detail": "提取花形、曲线、风格、结构、镶嵌方式等标签",
        "icon": "🎨",
        "color": "#45B7D1"
    },
    {
        "id": 4,
        "title": "AI自主分析与匹配设计方向",
        "desc": "结合市场趋势和已有代表性款式",
        "detail": "判断是否有可复用母版",
        "icon": "🤖",
        "color": "#96CEB4",
        "options": ["有相似款式 - 保留成熟结构，提出局部改款方案", "无相似款式 - 根据市场设计元素提出全新款方案"]
    },
    {
        "id": 5,
        "title": "AI生成概念图与多角度效果图",
        "desc": "输出设计方案、参考来源、旧款关联及修改说明",
        "detail": "",
        "icon": "🖼️",
        "color": "#FFEAA7"
    },
    {
        "id": 6,
        "title": "第一次人工审版：设计方向",
        "desc": "筛选市场潜力、外观、款式差异化及开发价值",
        "detail": "",
        "icon": "👤",
        "color": "#DFE6E9",
        "needReview": True
    },
    {
        "id": 7,
        "title": "AI辅助生成或修改3D模型",
        "desc": "优先调用Rhino对已有源文件进行改款",
        "detail": "新款可图生3D粗模，再导入Rhino/ZBrush处理",
        "icon": "🎯",
        "color": "#74B9FF"
    },
    {
        "id": 8,
        "title": "Rhino/ZBrush自动化修模与检查",
        "desc": "调整尺寸、曲面、轮廓、厚度、连接件及部分结构",
        "detail": "尽量减少人工二次修改，复杂镶嵌保留人工处理",
        "icon": "🔧",
        "color": "#A29BFE"
    },
    {
        "id": 9,
        "title": "第二次人工审版：生产工艺",
        "desc": "工厂建模师精修并确认镶嵌、铸造和打样可行性",
        "detail": "",
        "icon": "👥",
        "color": "#FD79A8",
        "needReview": True
    },
    {
        "id": 10,
        "title": "输出最终3D源文件及生产文件",
        "desc": "保留可编辑源文件，导出符合工厂要求的喷蜡/打印文件",
        "detail": "",
        "icon": "📦",
        "color": "#FDCB6E"
    },
    {
        "id": 11,
        "title": "一键生成电商营销素材",
        "desc": "主图、详情图、英文文案、场景图和产品宣传视频",
        "detail": "",
        "icon": "📱",
        "color": "#6C5CE7"
    }
]

def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'username' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        password_hash = hashlib.sha256(password.encode()).hexdigest()

        if username in USERS and USERS[username]['password'] == password_hash:
            session['username'] = username
            session['current_step'] = 1
            session['workflow_data'] = {}
            return redirect(url_for('workflow'))
        else:
            return render_template_string(LOGIN_HTML, error="用户名或密码错误")

    return render_template_string(LOGIN_HTML)

# 登录页面HTML（精美动画版）
LOGIN_HTML = """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>登录 - AI珠宝设计系统</title>
    <style>
        @keyframes gradient {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }

        @keyframes fadeInUp {
            from {
                opacity: 0;
                transform: translateY(30px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }

        @keyframes float {
            0%, 100% { transform: translateY(0px); }
            50% { transform: translateY(-20px); }
        }

        * { margin: 0; padding: 0; box-sizing: border-box; }

        body {
            font-family: -apple-system, BlinkMacSystemFont, 'PingFang SC', sans-serif;
            background: linear-gradient(-45deg, #667eea, #764ba2, #f093fb, #4facfe);
            background-size: 400% 400%;
            animation: gradient 15s ease infinite;
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            overflow: hidden;
        }

        .particles {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            overflow: hidden;
            z-index: 0;
        }

        .particle {
            position: absolute;
            background: rgba(255,255,255,0.5);
            border-radius: 50%;
            animation: float 6s ease-in-out infinite;
        }

        .login-box {
            background: rgba(255,255,255,0.95);
            backdrop-filter: blur(10px);
            padding: 50px;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            width: 420px;
            position: relative;
            z-index: 1;
            animation: fadeInUp 0.8s ease;
        }

        .logo {
            text-align: center;
            font-size: 80px;
            margin-bottom: 20px;
            animation: float 3s ease-in-out infinite;
        }

        h1 {
            text-align: center;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 10px;
            font-size: 32px;
        }

        .subtitle {
            text-align: center;
            color: #666;
            margin-bottom: 40px;
            font-size: 15px;
        }

        .input-group {
            position: relative;
            margin: 25px 0;
        }

        input {
            width: 100%;
            padding: 15px 20px;
            border: 2px solid #e0e0e0;
            border-radius: 12px;
            font-size: 15px;
            transition: all 0.3s;
        }

        input:focus {
            outline: none;
            border-color: #667eea;
            box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
        }

        button {
            width: 100%;
            padding: 16px;
            margin-top: 30px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 12px;
            font-size: 17px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s;
            position: relative;
            overflow: hidden;
        }

        button::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: rgba(255,255,255,0.2);
            transition: left 0.5s;
        }

        button:hover::before {
            left: 100%;
        }

        button:hover {
            transform: translateY(-3px);
            box-shadow: 0 10px 25px rgba(102, 126, 234, 0.4);
        }

        .error {
            background: linear-gradient(135deg, #ff6b6b, #ee5a52);
            color: white;
            padding: 15px;
            border-radius: 12px;
            margin-bottom: 20px;
            animation: fadeInUp 0.5s ease;
        }

        .hint {
            margin-top: 30px;
            padding: 20px;
            background: linear-gradient(135deg, #f8f9fa, #e9ecef);
            border-radius: 12px;
            font-size: 14px;
            color: #666;
        }

        .hint strong {
            display: block;
            margin-bottom: 10px;
            color: #333;
        }
    </style>
</head>
<body>
    <div class="particles">
        <div class="particle" style="width: 5px; height: 5px; left: 20%; top: 30%; animation-delay: 0s;"></div>
        <div class="particle" style="width: 3px; height: 3px; left: 40%; top: 60%; animation-delay: 2s;"></div>
        <div class="particle" style="width: 4px; height: 4px; left: 60%; top: 40%; animation-delay: 4s;"></div>
        <div class="particle" style="width: 6px; height: 6px; left: 80%; top: 70%; animation-delay: 6s;"></div>
        <div class="particle" style="width: 3px; height: 3px; left: 30%; top: 80%; animation-delay: 3s;"></div>
    </div>

    <div class="login-box">
        <div class="logo">💎</div>
        <h1>AI珠宝设计系统</h1>
        <p class="subtitle">11步引导式智能工作流</p>

        {% if error %}
        <div class="error">{{ error }}</div>
        {% endif %}

        <form method="POST">
            <div class="input-group">
                <input type="text" name="username" placeholder="用户名" required autofocus>
            </div>
            <div class="input-group">
                <input type="password" name="password" placeholder="密码" required>
            </div>
            <button type="submit">登录进入</button>
        </form>

        <div class="hint">
            <strong>🔑 测试账号</strong>
            用户名: admin<br>
            密码: admin123
        </div>
    </div>
</body>
</html>
"""

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/')
@login_required
def workflow():
    current_step = session.get('current_step', 1)
    step_data = WORKFLOW_STEPS[current_step - 1]

    return render_template_string(
        WORKFLOW_HTML,
        username=session.get('username'),
        current_step=current_step,
        total_steps=len(WORKFLOW_STEPS),
        step=step_data,
        all_steps=WORKFLOW_STEPS,
        workflow_data=session.get('workflow_data', {})
    )

# 工作流页面HTML（精美动画版）- 由于太长，我会分段创建
WORKFLOW_HTML = """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>步骤 {{ current_step }}/{{ total_steps }} - AI珠宝设计系统</title>
    <style>
        @keyframes slideIn {
            from {
                opacity: 0;
                transform: translateX(-30px);
            }
            to {
                opacity: 1;
                transform: translateX(0);
            }
        }

        @keyframes pulse {
            0%, 100% { transform: scale(1); }
            50% { transform: scale(1.05); }
        }

        @keyframes shimmer {
            0% { background-position: -1000px 0; }
            100% { background-position: 1000px 0; }
        }

        * { margin: 0; padding: 0; box-sizing: border-box; }

        body {
            font-family: -apple-system, BlinkMacSystemFont, 'PingFang SC', sans-serif;
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            min-height: 100vh;
        }

        .navbar {
            background: white;
            padding: 20px 40px;
            box-shadow: 0 2px 15px rgba(0,0,0,0.08);
            display: flex;
            justify-content: space-between;
            align-items: center;
            animation: slideIn 0.5s ease;
        }

        .logo {
            font-size: 24px;
            font-weight: bold;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .user-info {
            display: flex;
            align-items: center;
            gap: 20px;
        }

        .btn-logout {
            padding: 10px 24px;
            background: linear-gradient(135deg, #f8f9fa, #e9ecef);
            border: none;
            border-radius: 8px;
            cursor: pointer;
            text-decoration: none;
            color: #333;
            transition: all 0.3s;
        }

        .btn-logout:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }

        .container {
            max-width: 1100px;
            margin: 40px auto;
            padding: 0 20px;
        }

        .progress-container {
            background: white;
            padding: 40px;
            border-radius: 20px;
            margin-bottom: 30px;
            box-shadow: 0 5px 20px rgba(0,0,0,0.08);
            animation: slideIn 0.6s ease;
        }

        .mini-steps {
            display: flex;
            gap: 15px;
            overflow-x: auto;
            padding: 10px 0;
            margin-bottom: 30px;
        }

        .mini-step {
            min-width: 80px;
            padding: 15px;
            border-radius: 12px;
            text-align: center;
            background: #f8f9fa;
            transition: all 0.3s;
            cursor: pointer;
        }

        .mini-step.completed {
            background: linear-gradient(135deg, #51cf66, #40c057);
            color: white;
        }

        .mini-step.active {
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
            animation: pulse 2s infinite;
        }

        .mini-step-icon {
            font-size: 24px;
            margin-bottom: 5px;
        }

        .mini-step-num {
            font-size: 11px;
            opacity: 0.8;
        }

        .progress-track {
            height: 8px;
            background: #e9ecef;
            border-radius: 4px;
            overflow: hidden;
        }

        .progress-fill {
            height: 100%;
            background: linear-gradient(90deg, #667eea, #764ba2, #667eea);
            background-size: 200% 100%;
            animation: shimmer 2s linear infinite;
            width: {{ (current_step - 1) * 100 / (total_steps - 1) }}%;
            transition: width 0.5s ease;
        }

        .step-card {
            background: white;
            padding: 50px;
            border-radius: 20px;
            box-shadow: 0 5px 20px rgba(0,0,0,0.08);
            animation: slideIn 0.7s ease;
        }

        .step-header {
            text-align: center;
            margin-bottom: 40px;
        }

        .step-icon {
            font-size: 100px;
            margin-bottom: 25px;
            display: inline-block;
            animation: pulse 3s infinite;
        }

        .step-badge {
            display: inline-block;
            padding: 8px 20px;
            background: {{ step.color }};
            color: white;
            border-radius: 20px;
            font-size: 14px;
            margin-bottom: 15px;
        }

        .step-title {
            font-size: 32px;
            color: #2c3e50;
            margin-bottom: 15px;
            font-weight: 700;
        }

        .step-desc {
            font-size: 18px;
            color: #7f8c8d;
            margin-bottom: 10px;
        }

        .step-detail {
            font-size: 15px;
            color: #95a5a6;
        }

        .step-content {
            margin: 40px 0;
        }

        .input-group {
            margin: 25px 0;
        }

        label {
            display: block;
            margin-bottom: 12px;
            color: #2c3e50;
            font-weight: 600;
            font-size: 16px;
        }

        input[type="text"], textarea {
            width: 100%;
            padding: 16px 20px;
            border: 2px solid #e9ecef;
            border-radius: 12px;
            font-size: 16px;
            transition: all 0.3s;
        }

        input:focus, textarea:focus {
            outline: none;
            border-color: #667eea;
            box-shadow: 0 0 0 4px rgba(102, 126, 234, 0.1);
        }

        textarea {
            min-height: 120px;
            resize: vertical;
        }

        .options {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
            margin: 30px 0;
        }

        .option-card {
            padding: 30px;
            border: 3px solid #e9ecef;
            border-radius: 16px;
            cursor: pointer;
            transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
            position: relative;
            overflow: hidden;
        }

        .option-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: linear-gradient(135deg, rgba(102, 126, 234, 0.05), rgba(118, 75, 162, 0.05));
            opacity: 0;
            transition: opacity 0.3s;
        }

        .option-card:hover {
            transform: translateY(-8px);
            border-color: #667eea;
            box-shadow: 0 15px 35px rgba(102, 126, 234, 0.2);
        }

        .option-card:hover::before {
            opacity: 1;
        }

        .option-card.selected {
            border-color: #667eea;
            background: linear-gradient(135deg, rgba(102, 126, 234, 0.1), rgba(118, 75, 162, 0.1));
            transform: scale(1.02);
            box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
        }

        .option-card h3 {
            color: #2c3e50;
            margin-bottom: 15px;
            font-size: 18px;
        }

        .option-card p {
            color: #7f8c8d;
            font-size: 15px;
            line-height: 1.6;
        }

        .status-message {
            text-align: center;
            padding: 30px;
            background: linear-gradient(135deg, #e3f2fd, #bbdefb);
            border-radius: 16px;
            margin: 30px 0;
            font-size: 18px;
            color: #1976d2;
            animation: pulse 2s infinite;
        }

        .action-buttons {
            display: flex;
            justify-content: space-between;
            margin-top: 50px;
            gap: 20px;
        }

        .btn {
            padding: 16px 50px;
            border: none;
            border-radius: 12px;
            font-size: 17px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
            position: relative;
            overflow: hidden;
        }

        .btn::after {
            content: '';
            position: absolute;
            top: 50%;
            left: 50%;
            width: 0;
            height: 0;
            border-radius: 50%;
            background: rgba(255,255,255,0.5);
            transform: translate(-50%, -50%);
            transition: width 0.6s, height 0.6s;
        }

        .btn:active::after {
            width: 300px;
            height: 300px;
        }

        .btn-primary {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            flex: 1;
        }

        .btn-primary:hover {
            transform: translateY(-3px);
            box-shadow: 0 15px 35px rgba(102, 126, 234, 0.4);
        }

        .btn-secondary {
            background: linear-gradient(135deg, #f8f9fa, #e9ecef);
            color: #495057;
        }

        .btn-secondary:hover {
            transform: translateY(-3px);
            box-shadow: 0 10px 25px rgba(0,0,0,0.1);
        }

        .btn:disabled {
            opacity: 0.5;
            cursor: not-allowed;
            transform: none !important;
        }

        @media (max-width: 768px) {
            .options {
                grid-template-columns: 1fr;
            }

            .step-card {
                padding: 30px 20px;
            }
        }
    </style>
</head>
<body>
    <div class="navbar">
        <div class="logo">💎 AI珠宝设计系统</div>
        <div class="user-info">
            <span>👤 {{ username }}</span>
            <a href="{{ url_for('logout') }}" class="btn-logout">退出登录</a>
        </div>
    </div>

    <div class="container">
        <div class="progress-container">
            <div class="mini-steps">
                {% for s in all_steps %}
                <div class="mini-step {% if s.id < current_step %}completed{% elif s.id == current_step %}active{% endif %}">
                    <div class="mini-step-icon">{{ s.icon }}</div>
                    <div class="mini-step-num">步骤 {{ s.id }}</div>
                </div>
                {% endfor %}
            </div>
            <div class="progress-track">
                <div class="progress-fill"></div>
            </div>
            <p style="text-align: center; margin-top: 15px; color: #7f8c8d; font-size: 16px;">
                <strong>{{ current_step }}</strong> / {{ total_steps }} 步骤
            </p>
        </div>

        <div class="step-card">
            <div class="step-header">
                <div class="step-icon">{{ step.icon }}</div>
                <div class="step-badge">步骤 {{ current_step }}</div>
                <h2 class="step-title">{{ step.title }}</h2>
                <p class="step-desc">{{ step.desc }}</p>
                {% if step.detail %}
                <p class="step-detail">{{ step.detail }}</p>
                {% endif %}
            </div>

            <div class="step-content">
                <div id="step-content">
                    {% if current_step == 1 %}
                    <div class="input-group">
                        <label>🔍 输入关键词（多个关键词用逗号分隔）</label>
                        <input type="text" id="keywords" placeholder="例如: diamond ring, luxury necklace, pearl earring">
                    </div>
                    {% elif current_step == 4 and step.options %}
                    <div class="options">
                        {% for option in step.options %}
                        <div class="option-card" onclick="selectOption(this, '{{ option }}')">
                            <h3>{{ option.split(' - ')[0] }}</h3>
                            <p>{{ option.split(' - ')[1] if ' - ' in option else '' }}</p>
                        </div>
                        {% endfor %}
                    </div>
                    {% elif step.needReview %}
                    <div class="status-message">
                        ⏳ 等待人工审核中...
                    </div>
                    <div class="input-group">
                        <label>📝 审核意见（可选）</label>
                        <textarea id="review_notes" placeholder="请输入您的审核意见和建议..."></textarea>
                    </div>
                    {% else %}
                    <div class="status-message">
                        ⚙️ 系统正在自动处理，请稍候...
                    </div>
                    {% endif %}
                </div>
            </div>

            <div class="action-buttons">
                <button class="btn btn-secondary" onclick="previousStep()" {% if current_step == 1 %}disabled{% endif %}>
                    ← 上一步
                </button>
                <button class="btn btn-primary" onclick="nextStep()" id="nextBtn">
                    {{ '🎉 完成' if current_step == total_steps else '下一步 →' }}
                </button>
            </div>
        </div>
    </div>

    <script>
        let selectedOption = null;

        function selectOption(element, option) {
            document.querySelectorAll('.option-card').forEach(card => {
                card.classList.remove('selected');
            });
            element.classList.add('selected');
            selectedOption = option;
        }

        function previousStep() {
            if ({{ current_step }} > 1) {
                window.location.href = '/step/' + ({{ current_step }} - 1);
            }
        }

        function nextStep() {
            const btn = document.getElementById('nextBtn');
            btn.disabled = true;
            btn.textContent = '处理中...';

            const data = {};

            {% if current_step == 1 %}
            data.keywords = document.getElementById('keywords').value;
            if (!data.keywords) {
                alert('请输入关键词');
                btn.disabled = false;
                btn.textContent = '下一步 →';
                return;
            }
            {% elif current_step == 4 %}
            if (!selectedOption) {
                alert('请选择一个选项');
                btn.disabled = false;
                btn.textContent = '下一步 →';
                return;
            }
            data.option = selectedOption;
            {% elif step.needReview %}
            data.review_notes = document.getElementById('review_notes').value;
            {% endif %}

            fetch('/step/next', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify(data)
            })
            .then(response => response.json())
            .then(result => {
                if (result.success) {
                    window.location.href = '/';
                } else {
                    alert('操作失败: ' + result.message);
                    btn.disabled = false;
                    btn.textContent = '下一步 →';
                }
            });
        }
    </script>
</body>
</html>
"""

@app.route('/step/next', methods=['POST'])
@login_required
def next_step():
    data = request.json
    current_step = session.get('current_step', 1)

    workflow_data = session.get('workflow_data', {})
    workflow_data[f'step_{current_step}'] = data
    session['workflow_data'] = workflow_data

    if current_step < len(WORKFLOW_STEPS):
        session['current_step'] = current_step + 1

    return jsonify({'success': True})

@app.route('/step/<int:step_num>')
@login_required
def goto_step(step_num):
    if 1 <= step_num <= len(WORKFLOW_STEPS):
        session['current_step'] = step_num
    return redirect(url_for('workflow'))

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))

    print("\n" + "="*60)
    print("🎨 AI珠宝设计系统 - 精美动画版")
    print("="*60)
    print(f"\n📍 访问地址: http://localhost:{port}")
    print("\n🔐 测试账号:")
    print("   用户名: admin")
    print("   密码: admin123")
    print("\n✨ 新增动画效果:")
    print("   • 渐变背景动画")
    print("   • 卡片悬停效果")
    print("   • 按钮点击涟漪")
    print("   • 进度条动画")
    print("   • 页面淡入效果")
    print("\n按 Ctrl+C 停止服务")
    print("="*60 + "\n")

    app.run(host='0.0.0.0', port=port, debug=True)
