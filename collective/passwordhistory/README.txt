Password History PAS plug-in
=============================

This PAS plug-in can be used to prevent users of a Plone site from re-using the
same password multiple times.

Let's change the password::

    >>> from Products.CMFCore.utils import getToolByName
    >>> membership = getToolByName(self.portal, 'portal_membership')
    >>> membership.setPassword('secret')

Now let's try that again with the same password::

    >>> membership.setPassword('secret')
    Traceback (most recent call last):
    BadRequest: You have used this password before...

If we try a different password, we should be okay::

    >>> membership.setPassword('foobar')

We can set the number of previous passwords to check against by setting the
history_size attribute on the storage. Let's only check 1 previous password by
setting history_size 1. In doing this we don't actually loose any of our
stored history, we're merely changing the number of previous passwords to check
against::

    >>> plugin = self.portal.acl_users.password_history
    >>> plugin.history_size = 1

So now, it should stop us from setting the password to 'foobar'::

    >>> membership.setPassword('foobar')
    Traceback (most recent call last):
    BadRequest: You have used this password before...

But we should now be able to set it to 'secret' once again::

    >>> membership.setPassword('secret')

So let's make sure we haven't blown away our history. Setting the history_size
attribute to 0 should check the password against every password this user has
ever used. Let's try and use a password we have used before, but not the most
recent one::

    >>> plugin.setHistorySize = 0
    >>> membership.setPassword('foobar')
    Traceback (most recent call last):
    BadRequest: You have used this password before...
