from rest_framework_jwt.settings import api_settings


def create_jwt_token(user: object):
    """为用户创建一个jwt的加密token"""
    jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER  # 导出payload载荷生成对象
    jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER  # 导出jwt编码对象

    payload = jwt_payload_handler(user)  # 生成载荷payload部分，主要包含 id, username, expire, email等
    token = jwt_encode_handler(
        payload)  # 生成加密后的token。header部分自动加上，secret部分取用settings文件中的SECRET_KEY,没有则用jwt默认的secret

    return token
