from flask import Flask, render_template, request, Response, make_response
import requests
import json
from datetime import datetime, timedelta
from config import Config

app = Flask(__name__)
app.config.from_object(Config)


@app.template_filter('nl2br')
def nl2br_filter(text):
    if text is None:
        return ''
    return text.replace('\n', '<br>\n')

@app.template_filter('format_selling_points')
def format_selling_points_filter(text):
    if text is None:
        return ''
    lines = text.strip().split('\n')
    result = []
    for line in lines:
        line = line.strip()
        if line:
            result.append(f'<li>{line}</li>')
    return '<ul>' + ''.join(result) + '</ul>'

cache = {
    'data': None,
    'timestamp': None,
    'expires_in': 1800
}


def get_feishu_tenant_access_token():
    url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
    headers = {
        "Content-Type": "application/json"
    }
    data = {
        "app_id": app.config['FEISHU_APP_ID'],
        "app_secret": app.config['FEISHU_APP_SECRET']
    }
    
    response = requests.post(url, headers=headers, json=data)
    result = response.json()
    
    if result.get('code') == 0:
        return result.get('tenant_access_token')
    else:
        raise Exception(f"获取飞书token失败: {result}")


def extract_file_url(file_field):
    if not file_field:
        return ''
    
    original_url = ''
    
    if isinstance(file_field, list) and len(file_field) > 0:
        file_obj = file_field[0]
        if isinstance(file_obj, dict):
            original_url = file_obj.get('url') or file_obj.get('tmp_url', '')
    
    if isinstance(file_field, str):
        original_url = file_field
    
    if not original_url:
        return ''
    
    from urllib.parse import quote
    return f"/proxy/file?url={quote(original_url, safe='')}"


def get_bitable_records():
    current_time = datetime.now()
    
    if cache['data'] and cache['timestamp']:
        if current_time - cache['timestamp'] < timedelta(seconds=cache['expires_in']):
            return cache['data']
    
    try:
        token = get_feishu_tenant_access_token()
        url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{app.config['BASE_ID']}/tables/{app.config['TABLE_ID']}/records"
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        
        response = requests.get(url, headers=headers)
        result = response.json()
        
        if result.get('code') == 0:
            records = result.get('data', {}).get('items', [])
            formatted_data = []
            
            for record in records:
                fields = record.get('fields', {})
                formatted_data.append({
                    'record_id': record.get('record_id'),
                    'asin': fields.get('ASIN', ''),
                    'image': extract_file_url(fields.get('图片')),
                    'link': fields.get('链接', ''),
                    'title': fields.get('标题', ''),
                    'title_translation': fields.get('标题翻译', ''),
                    'selling_points': fields.get('五行卖点', ''),
                    'selling_points_translation': fields.get('五行卖点翻译', ''),
                    'product_short_name': fields.get('产品简称', ''),
                    'product_type': fields.get('产品类型', ''),
                    'prompt': fields.get('提示词', ''),
                    'video': extract_file_url(fields.get('视频'))
                })
            
            cache['data'] = formatted_data
            cache['timestamp'] = current_time
            
            return formatted_data
        else:
            raise Exception(f"获取飞书数据失败: {result}")
    except Exception as e:
        print(f"Error fetching data: {e}")
        return []


@app.route('/')
def index():
    records = get_bitable_records()
    product_type_filter = request.args.get('product_type', '')
    
    if product_type_filter:
        records = [r for r in records if r.get('product_type') == product_type_filter]
    
    all_product_types = sorted(list(set(r.get('product_type', '') for r in get_bitable_records() if r.get('product_type'))))
    
    response = make_response(render_template('index.html', records=records, all_product_types=all_product_types, current_filter=product_type_filter))
    response.headers['Cache-Control'] = 'public, max-age=60'
    return response


@app.route('/favicon.ico')
@app.route('/favicon.png')
def favicon():
    return '', 204


@app.route('/detail/<record_id>')
def detail(record_id):
    records = get_bitable_records()
    record = next((r for r in records if r['record_id'] == record_id), None)
    
    if not record:
        return "记录不存在", 404
    
    response = make_response(render_template('detail.html', record=record))
    response.headers['Cache-Control'] = 'public, max-age=300'
    return response


@app.route('/proxy/file')
def proxy_file():
    file_url = request.args.get('url')
    if not file_url:
        return "缺少 URL 参数", 400
    
    try:
        token = get_feishu_tenant_access_token()
        headers = {
            "Authorization": f"Bearer {token}"
        }
        
        response = requests.get(file_url, headers=headers, stream=True, timeout=30)
        response.raise_for_status()
        
        content_type = response.headers.get('Content-Type', 'application/octet-stream')
        
        return Response(
            response.iter_content(chunk_size=8192),
            content_type=content_type,
            headers={
                'Cache-Control': 'public, max-age=86400, immutable',
                'ETag': f'"{hash(file_url)}"',
                'Access-Control-Allow-Origin': '*'
            }
        )
    except Exception as e:
        print(f"代理文件下载失败: {e}")
        return f"文件下载失败: {str(e)}", 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
