import datetime
from platform import platform
import factory
from ..misc.tortoise import TortoiseModelFactory
from ..misc.utils import create_cuid
from .models import AppLoginPostgres, ClientPostgres, PlatformPostgres, UserPostgres
from ..domain.enums import (
    AppLoginFailedReason,
    AppLoginStatus,
    PlatformCode,
    CountryCode,
    PlatformStatus,
    UserPurpose,
    Source,
)


class ClientPostgresFaker(TortoiseModelFactory):

    id = factory.Faker("random_int")
    email = factory.Faker("email")
    api_key = factory.Faker("uuid4")
    company_name = factory.Faker("company")
    cuid = create_cuid()
    logo_name = factory.Faker("image_url")
    list_apps = [PlatformCode.CABIFY.value, PlatformCode.INDRIVER.value]
    webhook_url = factory.Faker("url")
    extra_data = {"key": "something"}
    list_of_countries = [CountryCode.COLOMBIA.value, CountryCode.MEXICO.value]
    created_at = factory.LazyAttribute(lambda o: datetime.datetime.utcnow())
    updated_at = factory.LazyAttribute(lambda o: datetime.datetime.utcnow())

    class Meta:
        model = ClientPostgres


class UserExtraDataPostgresFaker(factory.DictFactory):
    purpose = UserPurpose.CHANGE_BANK_ACCOUNT.value


class UserPostgresFaker(TortoiseModelFactory):

    id = factory.Faker("random_int")
    cuid = create_cuid()
    created_at = factory.LazyAttribute(lambda o: datetime.datetime.utcnow())
    updated_at = factory.LazyAttribute(lambda o: datetime.datetime.utcnow())
    extra_data = factory.SubFactory(UserExtraDataPostgresFaker)
    client = factory.SubFactory(ClientPostgresFaker)

    class Meta:
        model = UserPostgres


class AppLoginExtraDataFaker(factory.DictFactory):
    key = str(factory.Faker("uuid4"))


class AppLoginPostgresFaker(TortoiseModelFactory):
    id = factory.Faker("random_int")
    client = factory.SubFactory(ClientPostgresFaker)
    user = factory.SubFactory(UserPostgresFaker)
    country = CountryCode.MEXICO.value
    platform = PlatformCode.PEDIDOSYA.value
    login = factory.Faker("email")
    password = "plain_password"
    source = Source.WIDGET.value
    worker_id = create_cuid()
    status = AppLoginStatus.CREATED.value
    failed_reason = AppLoginFailedReason.CREDENTIALS_INVALID.value
    access_token = str(factory.Faker("uuid4"))
    refresh_token = str(factory.Faker("uuid4"))
    extra_data = factory.SubFactory(AppLoginExtraDataFaker)
    expiration_date = factory.LazyAttribute(lambda o: datetime.datetime.utcnow())
    created_at = factory.LazyAttribute(lambda o: datetime.datetime.utcnow())
    updated_at = factory.LazyAttribute(lambda o: datetime.datetime.utcnow())

    class Meta:
        model = AppLoginPostgres


class PlatformPostgresFaker(TortoiseModelFactory):
    id = factory.Faker("random_int")
    code = PlatformCode.CABIFY.value
    status = PlatformStatus.OPERATING.value
    available_countries = [CountryCode.MEXICO.value, CountryCode.COLOMBIA.value]
    created_at = factory.LazyAttribute(lambda o: datetime.datetime.utcnow())
    updated_at = factory.LazyAttribute(lambda o: datetime.datetime.utcnow())

    class Meta:
        model = PlatformPostgres
