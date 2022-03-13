from mock.pedidosya.domain.entities import Authentication

from pydantic_factories import ModelFactory


class AuthenticationFactory(ModelFactory):
    __model__ = Authentication
