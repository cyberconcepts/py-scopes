# scopes.org.mail

from zope.interface import implementer
from zope.sendmail.interfaces import IMailDelivery

"""Utilities for creating and sending emails."""


@implementer(IMailDelivery)
class DummyMailDelivery:
    """For testing purposes: just store mails in maildata.log"""

    def send(self, fromaddr, toaddrs, message):
        print("DummyMailDelivery")
        print(f"fromaddr: {fromaddr}, toaddrs: {toaddrs}")
        print(message)
