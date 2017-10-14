import requests
from IPython.core.ultratb import AutoFormattedTB

active=False

def _set_ipython_exception_handler(handler):
  try:
    get_ipython().set_custom_exc((Exception,), handler)
  except:
    pass # Not running in ipython

def notifying(sender='Jupyter Notebook',webhook=None):
  # if not webhook:
  #   webhook = WEBHOOK

  global notify, done, active
  active = True

  def notify(msg):
    if not active:
      return

    payload = {
        "text":msg,
        "username":sender
    }
    requests.post(webhook,json=payload)

  def done(msg="Finished"):
    global active
    notify(msg)
    active = False
    _set_ipython_exception_handler(None)

  # initialize the formatter for making the tracebacks into strings
  itb = AutoFormattedTB(mode = 'Plain', tb_offset = 1,color_scheme='NoColor')

  # this function will be called on exceptions in any cell
  def custom_exc(shell, etype, evalue, tb, tb_offset=None):
    # still show the error within the notebook, don't just swallow it
    shell.showtraceback((etype, evalue, tb), tb_offset=tb_offset)

    # grab the traceback and make it into a list of strings
    stb = itb.structured_traceback(etype, evalue, tb)
    sstb = itb.stb2text(stb)
    notify(sstb)

  # this registers a custom exception handler for the whole current notebook
  _set_ipython_exception_handler(custom_exc)
