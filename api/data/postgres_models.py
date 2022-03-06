from tortoise import fields
from tortoise.models import Model


class ClientPostgres(Model):
    id = fields.IntField(pk=True, index=True)
    cuid = fields.TextField()
    email = fields.TextField()
    api_key = fields.TextField()
    company_name = fields.TextField()
    logo_name = fields.TextField()
    list_apps = fields.JSONField()
    webhook_url = fields.TextField()
    extra_data = fields.JSONField(null=True)
    list_of_countries = fields.JSONField()
    created_at = fields.DatetimeField(auto_now=True)
    updated_at = fields.DatetimeField(auto_now=True)

    class Meta:
        table = "clients"


class UserPostgres(Model):
    id = fields.IntField(pk=True, index=True)
    cuid = fields.TextField()
    extra_data = fields.JSONField(null=True)
    client: fields.ForeignKeyRelation[ClientPostgres] = fields.ForeignKeyField(
        "models.ClientPostgres"
    )
    created_at = fields.DatetimeField(auto_now=True)
    updated_at = fields.DatetimeField(auto_now=True)

    class Meta:
        table = "users"


class AppLoginPostgres(Model):
    id = fields.IntField(pk=True, index=True)
    client: fields.ForeignKeyRelation[ClientPostgres] = fields.ForeignKeyField(
        "models.ClientPostgres"
    )
    user: fields.ForeignKeyRelation[ClientPostgres] = fields.ForeignKeyField(
        "models.UserPostgres"
    )
    country = fields.TextField()
    platform = fields.TextField()
    login = fields.TextField()
    status = fields.TextField()
    password = fields.TextField(null=True)
    source = fields.TextField(null=True)
    worker_id = fields.TextField(null=True)
    access_token = fields.TextField(null=True)
    refresh_token = fields.TextField(null=True)
    expiration_date = fields.DatetimeField(null=True)
    failed_reason = fields.TextField(null=True)
    extra_data = fields.JSONField(null=True)
    created_at = fields.DatetimeField(auto_now=True)
    updated_at = fields.DatetimeField(auto_now=True)

    class Meta:
        table = "app_logins"


class PlatformPostgres(Model):
    id = fields.IntField(pk=True, index=True)
    code = fields.TextField()
    status = fields.TextField()
    available_countries = fields.JSONField(null=True)
    created_at = fields.DatetimeField(auto_now=True)
    updated_at = fields.DatetimeField(auto_now=True)

    class Meta:
        table = "platforms"
