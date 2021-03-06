from ninja import Schema


class TokenPayload(Schema):
    user_id: int = None
