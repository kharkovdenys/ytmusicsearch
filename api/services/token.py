import jwt


def read(token):
    return jwt.decode(token, "_webmusic-chaha_", algorithms=['HS256'], audience="chaha")[
        "http://schemas.xmlsoap.org/ws/2005/05/identity/claims/name"]
