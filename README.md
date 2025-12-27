# 视频案例展示网站

一个基于 Flask 的视频案例展示网站，集成飞书多维表格 API。

## 功能特点

- ✅ 从飞书多维表格获取视频案例数据
- ✅ 产品类型筛选功能
- ✅ 科技感 UI 设计（玻璃态、霓虹效果）
- ✅ 粒子背景动画
- ✅ 响应式设计
- ✅ 图片和视频代理（解决飞书认证问题）

## 本地开发

### 环境要求

- Python 3.9+
- pip

### 安装依赖

```bash
pip install -r requirements.txt
```

### 配置环境变量

复制 `.env.example` 为 `.env` 并填写飞书配置：

```bash
cp .env.example .env
```

编辑 `.env` 文件：

```
FEISHU_APP_ID=your_app_id
FEISHU_APP_SECRET=your_app_secret
BASE_ID=your_base_id
TABLE_ID=your_table_id
SECRET_KEY=your_secret_key
```

### 运行应用

```bash
python app.py
```

访问 `http://localhost:5000`

## 部署到 Vercel

### 方法 1：通过 Vercel CLI

1. 安装 Vercel CLI：
```bash
npm install -g vercel
```

2. 登录 Vercel：
```bash
vercel login
```

3. 部署：
```bash
vercel
```

4. 配置环境变量：
在 Vercel Dashboard 中添加以下环境变量：
- `FEISHU_APP_ID`
- `FEISHU_APP_SECRET`
- `BASE_ID`
- `TABLE_ID`
- `SECRET_KEY`

### 方法 2：通过 GitHub 集成

1. 将代码推送到 GitHub 仓库
2. 在 Vercel Dashboard 中导入项目
3. 配置环境变量
4. 部署

## 性能优化

- ✅ 数据缓存（30分钟）
- ✅ 静态资源缓存（1年）
- ✅ 图片/视频缓存（24小时）
- ✅ 页面缓存（首页60秒，详情页5分钟）

## 项目结构

```
website/
├── app.py              # 主应用文件
├── config.py           # 配置文件
├── requirements.txt    # Python 依赖
├── vercel.json        # Vercel 配置
├── static/
│   ├── css/
│   │   └── style.css  # 样式文件
│   └── js/
│       └── script.js  # JavaScript 文件
└── templates/
    ├── base.html      # 基础模板
    ├── index.html     # 首页
    └── detail.html    # 详情页
```

## 技术栈

- **后端**: Flask
- **前端**: HTML, CSS, JavaScript
- **样式**: Tailwind CSS + 自定义 CSS
- **图标**: Font Awesome
- **字体**: Inter, Orbitron
- **部署**: Vercel

## 许可证

MIT License
