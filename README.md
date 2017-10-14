# nb-slack

Jupyter notebook extension for sending slack notifications from long running notebooks

## Installation

You'll need Python 3

```
pip install https://github.com/flowmatters/nb-slack/archive/master.zip
```

At this stage we haven't tagged releases so you just install from the latest version.

To upgrade, uninstall the one you've got, then install again

```
pip uninstall nb-slack
pip install https://github.com/flowmatters/nb-slack/archive/master.zip
```

## Setup

You'll need a webhook configured in you Slack team. Most likely you'll want the webhook configured to send a private message to you, rather than one of the broader channels.

To set up a new webhook, go to [https://my.slack.com/services/new/incoming-webhook/](https://my.slack.com/services/new/incoming-webhook/), and select the channel you want to post to from Jupyter. Then click 'Add Incoming WebHooks integration'.

You'll then be presented with a Webhook URL, and a lot of options that you can ignore in the first instance. The Webhook URL is all you need - it's in the form of:

```
https://hooks.slack.com/services/LETTERS/AND/NUMBERS
```

Copy the URL into your notebook as a variable:

```
webhook='https://hooks.slack.com/services/LETTERS/AND/NUMBERS'
```

## Usage

Once you've got the webhook and the URL, you're ready to use nbslack:

```
import nbslack

# Initialise notifications - 
nbslack.notifying('Username that will appear in slack',webhook)
# The call to notifying doesn't send any notifications itself, but it does
# setup the functions notify and done and an IPython hook for unhandled exceptions

# Send a notification
nbslack.notify("I've gotten past the tricky bit")

# Notifications sent on unhandled exceptions
assert False

# Send one final notification and disable further notifications (including exceptions)
nbslack.done('Woohoo!')

