import string
import random
import logging

import ldap
from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

from profiles.models import Profile

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
      # authenticate to LDAP
      l.simple_bind_s("%s@jmu.edu" % username, password)
      # read our attributes
      result = l.search_s(self.base,
                          ldap.SCOPE_SUBTREE,
                          self.search_filter % username,
                          attrlist=self.attrlist)
      attributes = result[0][1]

      # see if we have a user
      try:
        user = User.objects.get(username=username)
      except User.DoesNotExist:
        user = User(username=username, password=self._generate_password())
      # update the user with the current directory information
      user.first_name = attributes['givenName'][0]
      user.last_name = attributes['sn'][0]
      user.email = attributes['mail'][0]
      user.save()

      # see if the user has a profile
      try:
        profile = user.profile
      except Profile.DoesNotExist:
        profile = Profile()
      # update the user's profile
      profile.phone_number = attributes['telephoneNumber'][0]
      profile.mailbox = attributes['postOfficeBox'][0]
      profile.department = attributes['ou'][0]
      if "faculty" in attributes['eduPersonAffiliation']:
        profile.affiliation = "faculty"
      elif "staff" in attributes['eduPersonAffiliation']:
        profile.affiliation = "staff"
      else:
        profile.affiliation = "other"
      # 'jmunickname' attribute may not be set, so give it a default
      profile.nickname = attributes.get('jmunickname', [''])[0]

      # set the profile in the user and save it
      user.profile = profile
      user.profile.save()
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
    try:
      return User.objects.get(pk=user_id)
    except User.DoesNotExist:
      return None


  def _generate_password(self):
    charset = string.ascii_letters + string.digits
    return make_password(''.join(random.sample(charset, 18)))
