import datetime
import factory
from ..misc.tests import TortoiseModelFactory

from .models import ClientPostgres, UserPostgres
from ..domain.enums import Platform, CountryCode, UserPurpose


class ClientPostgresFaker(TortoiseModelFactory):

    id = factory.Faker("random_int")
    email = factory.Faker("email")
    api_key = factory.Faker("uuid4")
    company_name = factory.Faker("company")
    client_id = str(factory.Faker("uuid4"))[:8]
    logo_name = factory.Faker("image_url")
    list_apps = [Platform.CABIFY.value, Platform.INDRIVER.value]
    webhook_url = factory.Faker("url")
    extra_data = {"somenthing": "something"}
    list_of_countries = [CountryCode.COLOMBIA.value, CountryCode.MEXICO.value]
    created_at = factory.LazyAttribute(lambda o: datetime.datetime.utcnow())
    updated_at = factory.LazyAttribute(lambda o: datetime.datetime.utcnow())

    class Meta:
        model = ClientPostgres


class UserExtraDataPostgresFaker(factory.DictFactory):
    purpose = UserPurpose.CHANGE_BANK_ACCOUNT.value


class UserPostgresFaker(TortoiseModelFactory):

    id = factory.Faker("random_int")
    user_id = str(factory.Faker("uuid4"))[:8]
    created_at = factory.LazyAttribute(lambda o: datetime.datetime.utcnow())
    updated_at = factory.LazyAttribute(lambda o: datetime.datetime.utcnow())
    extra_data = factory.SubFactory(UserExtraDataPostgresFaker)
    client = factory.SubFactory(ClientPostgresFaker)

    class Meta:
        model = UserPostgres
