class Config:
  """
  This are the configurations for the application
  """
  # SQLALCHEMY_TRACK_MODIFICATIONS=True
  SQLALCHEMY_DATABASE_URI='sqlite:///site.db'

  SECRET_KEY ='0bb329d58e8699441d3c6f5b5089a523'
class ProdConfig(Config):
  """
  This are the configurations for the production environment
  Args:
  Config : The main configuration
  """


class DevConfig(Config):
    """
    This are the configurations for the development environment
    Args:
        Config : The main configuration
    """
    DEBUG = True


config_options = {
    'development': DevConfig,
    'production': ProdConfig
}
