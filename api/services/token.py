import jwt


def read(token):
    decoded_token = jwt.decode(
        token, "_webmusic-chaha_", algorithms=['HS256'], audience="chaha")
    return decoded_token["http://schemas.xmlsoap.org/ws/2005/05/identity/claims/name"]
