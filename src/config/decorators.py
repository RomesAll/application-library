def checking_variables_db(funct):
    from .config_project import REQUIRED_ENV_VAR
    def wrapper(*args, **kwargs):
        var = args[0].model_dump()
        for key, value in var.items():
            if key in REQUIRED_ENV_VAR and value is None:
                from .config_project import settings
                settings.logging.logger.warning(f'Недостаточно данных для получения url к базе данных. '
                            f'Возможно, не все параметры были подгружены из env файла. Обязательные параметры: {REQUIRED_ENV_VAR}')
                return None
        return funct(*args, **kwargs)
    return wrapper