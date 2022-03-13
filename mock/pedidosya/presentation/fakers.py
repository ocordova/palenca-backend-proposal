from mock.pedidosya.presentation.responses import SucessfullLogin

from pydantic_factories import ModelFactory


class SucessfullLoginFactory(ModelFactory):
    __model__ = SucessfullLogin
