import json
from drone.utils.json_schema_validator import json_validate


def get_config(config, config_schema):

    try:
        with open(config, 'r') as f:
            config_text = f.read()
    except IOError:
        config_text = '{}'

    config_object = json.loads(config_text)
    json_validate(config_object, config_schema)
    return config_object