Prevent password re-use
=======================

A PAS plugin to prevent users from re-using passwords they have used before.

Implementation
--------------

A PAS Validation plugin checks the password against a stored list of previously
used passwords. If the password has been used before an error is returned.

Plone doesn't use PAS to validate passwords so included is a patch to
Products.CMFPlone.RegistrationTool.RegistrationTool.testPasswordValidity
which makes Plone use PAS validation plugins.

Passwords are stored in a local utility to make it easier to use different
storages. The default storage implementation keeps passwords in a BTree within
the ZODB, but you could, for example, provide a relational database storage.
The default storage keeps hashed passwords for security.

Also included is a patch for PlonaPAS to fire an event when users are deleted.
A subscriber for this event calls an event handler which removes the password
history for the deleted user.

Requirements
------------

This package requires Plone 3.0 or later.

Copyright and credits
---------------------

collective.passwordhistory is copyright 2007 by `Emyr Thomas`_, and is
licensed under the GPL. See LICENSE.txt for details.

.. _Emyr Thomas: emyr.thomas@gmail.com

Credits
_______

Thanks to Dylan Jay of PretaWeb_ for his PasswordStrength_ plugin which served
as a basis for this package.

.. _PretaWeb: http://www.pretaweb.com
.. _PasswordStrength: http://plone.org/products/passwordstrength
