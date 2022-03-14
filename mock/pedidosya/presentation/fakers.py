from pydantic_factories import ModelFactory

from mock.pedidosya.presentation.responses import SucessfullLogin


class SucessfullLoginFactory(ModelFactory):
    __model__ = SucessfullLogin
