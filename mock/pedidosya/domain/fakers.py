from pydantic_factories import ModelFactory

from mock.pedidosya.domain.entities import Authentication


class AuthenticationFactory(ModelFactory):
    __model__ = Authentication
