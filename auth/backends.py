from django.conf import settings
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied

import ldap
import logging

class LDAPBackend(object):
  logger = logging.getLogger(__name__)

  uri = settings.LDAP_AUTH['uri']
  base = settings.LDAP_AUTH['base']
  secure = settings.LDAP_AUTH['secure']
  search_filter = settings.LDAP_AUTH['search_filter']
  attrlist = settings.LDAP_AUTH['attrlist']
  local_admin_user = settings.LDAP_AUTH['local_admin_user']

  def authenticate(self, username=None, password=None):
    if self.local_admin_user and username == self.local_admin_user:
      # let the configured local admin user pass-through
      return None

    try:
      l = ldap.initialize(self.uri)
      if self.secure: l.start_tls_s()
      l.simple_bind_s("%s@jmu.edu" % username, password)
      result = l.search_s(self.base,
                          ldap.SCOPE_SUBTREE,
                          self.search_filter % username,
                          attrlist=self.attrlist)
      # stub, for now just return our local user
      user = User.objects.get(pk=2)
      return user

    except ldap.INVALID_CREDENTIALS:
      self.logger.debug("failed authentication for user '%s'" % username)
      raise PermissionDenied

    except ldap.LDAPError, e:
      if type(e.message) == dict:
        info = e.message.get('info', "<no info>")
        desc = e.message.get('desc', "<no desc>")
        self.logger.error("LDAP Error: %s (%s)" % (info, desc))
      else:
        self.logger.error("LDAP Error: %s" % e)

    finally:
      if l: l.unbind_s()

    return None




  def get_user(self, user_id):
    pass
