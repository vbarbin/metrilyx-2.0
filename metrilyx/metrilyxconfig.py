
import os
import ujson as json

def jsonFromFile(filepath):
    fh = open(filepath)
    jdata = json.load(fh)
    fh.close()
    return jdata

_abspath = os.path.abspath(__file__)

_apphome = os.environ.get('METRILYX_HOME')
if _apphome == None:
    print " * Warning: METRILYX_HOME environment variable not set!"
    _apphome = os.path.dirname(os.path.dirname(_abspath))
_appconf = os.environ.get('METRILYX_CONF')
if _appconf == None:
    _appconf = os.path.join(_apphome, "etc/metrilyx")

_appversion = open(os.path.join(_apphome, "VERSION")).read()

CONFIG_FILE = os.path.join(os.path.join(_apphome, _appconf), "metrilyx.conf")
if not os.path.exists(CONFIG_FILE):
    raise RuntimeError("Configuration file not found: %s!" % (CONFIG_FILE))


try:
    config = jsonFromFile(CONFIG_FILE)
except Exception, e:
    raise e
        

if config.has_key("error"):
    raise RuntimeError("Configuration error: %s" %(str(config)))

# Set the default creds to mangae dashboards.
config["django"] = {"user": "admin", "password": "metrilyx"}

# Check version
if not config.has_key("version"):
    config["version"] = _appversion
elif config["version"] != _appversion:
    raise RuntimeError("Configuration version not supported: Config version: %s; App version: %s;" 
        % (config["version"], _appversion))


if not config.has_key("static_path"):
    config["static_path"] = os.path.join(os.path.dirname(_apphome), "www")

if not config.has_key("schema_path"):
    config["schema_path"] = os.path.join(os.path.join(_apphome, _appconf), "schemas")

if config["version"].startswith("2.4"):
    adp = config['annotations']['dataprovider']
    if not adp.has_key('default_mapping'):
        adp['default_mapping'] = os.path.join(os.path.join(_apphome, _appconf), "ess-default-mappings.json")

    default_mapping = jsonFromFile(adp['default_mapping'])
    if default_mapping.has_key('error'):
        raise RuntimeError("Invalid mapping config: %s" % (adp['default_mapping']))

    adp['default_mapping'] = default_mapping

