def checking_variables_db(funct):
    from config import REQUIRED_ENV_VAR
    def wrapper(*args, **kwargs):
        var = args[0].model_dump()
        for key, value in var.items():
            if key in REQUIRED_ENV_VAR and value is None:
                return None
        funct(*args, **kwargs)
    return wrapper