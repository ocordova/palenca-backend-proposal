from tortoise import fields
from tortoise.models import Model


class ClientPostgres(Model):
    id = fields.IntField(pk=True, index=True)
    email = fields.TextField()
    api_key = fields.TextField()
    company_name = fields.TextField()
    client_id = fields.TextField()
    logo_name = fields.TextField()
    list_apps = fields.JSONField()
    webhook_url = fields.TextField()
    extra_data = fields.JSONField(default={})
    list_of_countries = fields.JSONField()
    created_at = fields.DatetimeField(auto_now=True)
    updated_at = fields.DatetimeField(auto_now=True)

    class Meta:
        table = "clients"


class UserPostgres(Model):
    id = fields.IntField(pk=True, index=True)
    user_id = fields.TextField()
    extra_data = fields.JSONField(default={})
    client = fields.ForeignKeyField("models.ClientPostgres", related_name="client")
    created_at = fields.DatetimeField(auto_now=True)
    updated_at = fields.DatetimeField(auto_now=True)

    class Meta:
        table = "users"
