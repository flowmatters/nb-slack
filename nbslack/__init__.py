import requests
from IPython.core.ultratb import AutoFormattedTB

_active=False
WEBHOOK=None
SENDER="Not set"

def _set_ipython_exception_handler(handler):
  try:
    get_ipython().set_custom_exc((Exception,), handler)
  except:
    pass # Not running in ipython

def notifying(sender='Jupyter Notebook',webhook=None):
  global WEBHOOK, _active, SENDER
  WEBHOOK=_select(webhook)
  SENDER=sender
  _active = WEBHOOK is not None

  # this registers a custom exception handler for the whole current notebook
  _set_ipython_exception_handler(custom_exc)

def notify(msg):
  if not _active:
    print('Notifications not activated')
    return

  payload = {
      "text":msg,
      "username":SENDER
  }
  try:
    requests.post(WEBHOOK,json=payload)
  except:
    print(f'Unable to post message to slack: {SENDER} "{msg}"')

def custom_exc(shell, etype, evalue, tb, tb_offset=None):
  '''this function will be called on exceptions in any cell
  '''
  # still show the error within the notebook, don't just swallow it
  shell.showtraceback((etype, evalue, tb), tb_offset=tb_offset)

  # initialize the formatter for making the tracebacks into strings
  itb = AutoFormattedTB(mode = 'Plain', tb_offset = 1,color_scheme='NoColor')

  # grab the traceback and make it into a list of strings
  stb = itb.structured_traceback(etype, evalue, tb)
  sstb = itb.stb2text(stb)
  notify(sstb)

def done(msg="Finished"):
  global _active
  notify(msg)
  _active = False
  _set_ipython_exception_handler(None)

def _config_fn():
  import os
  home = os.path.expanduser("~")
  return os.path.join(home,'.nbslack.json')     

def _load_config():
  import os
  import json
  fn = _config_fn()
  if os.path.exists(fn):
    try:
      return json.load(open(fn))
    except:
      return {}
  return {}

def _save_config(cfg):
  import json
  fn = _config_fn()
  json.dump(cfg,open(fn,'w'),indent=2)

def _select(webhook):
  if webhook and webhook.startswith('https://'):
    return webhook

  config = _load_config()
  if webhook is None:
    if 'default' in config:
      return config['default']

    for v in config.values():
      return v

  return config.get(webhook,None)

def register(webhook,name):
  config = _load_config()
  config[name]=webhook
  _save_config(config)