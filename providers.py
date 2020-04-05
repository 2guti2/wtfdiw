import injector
import os
from flask import Config
from flask_injector import request
from config.configuration import ConfigurationModule


class AppProvidersModule(injector.Module):

    def configure(self, binder):
        binder.bind(
            ConfigurationModule,
            to=self.create,
            scope=request
        )

    @injector.inject
    def create(
        self,
        config: Config,
    ) -> ConfigurationModule:
        return ConfigurationModule(config, os)

