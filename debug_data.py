import requests
import json
from config import Config

def debug_feishu_data():
    print("正在获取飞书数据...\n")
    
    try:
        token = get_feishu_tenant_access_token()
        url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{Config.BASE_ID}/tables/{Config.TABLE_ID}/records"
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        
        response = requests.get(url, headers=headers)
        result = response.json()
        
        if result.get('code') == 0:
            records = result.get('data', {}).get('items', [])
            print(f"✓ 成功获取 {len(records)} 条记录\n")
            
            if len(records) > 0:
                first_record = records[0]
                fields = first_record.get('fields', {})
                
                print("=== 第一条记录的字段 ===")
                print(f"Record ID: {first_record.get('record_id')}\n")
                
                for field_name, field_value in fields.items():
                    print(f"字段名: {field_name}")
                    print(f"字段类型: {type(field_value)}")
                    print(f"字段值: {field_value}")
                    print(f"字段值长度: {len(str(field_value))} 字符")
                    print("-" * 80)
                    
                    if field_name in ['图片', '视频']:
                        print(f"详细内容:")
                        print(json.dumps(field_value, indent=2, ensure_ascii=False))
                        print("-" * 80)
        else:
            print(f"✗ 获取数据失败: {result}")
            
    except Exception as e:
        print(f"✗ 发生错误: {e}")
        import traceback
        traceback.print_exc()


def get_feishu_tenant_access_token():
    url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
    headers = {"Content-Type": "application/json"}
    data = {
        "app_id": Config.FEISHU_APP_ID,
        "app_secret": Config.FEISHU_APP_SECRET
    }
    
    response = requests.post(url, headers=headers, json=data)
    result = response.json()
    
    if result.get('code') == 0:
        return result.get('tenant_access_token')
    else:
        raise Exception(f"获取飞书token失败: {result}")


if __name__ == '__main__':
    debug_feishu_data()
