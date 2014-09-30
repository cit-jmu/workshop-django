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
  logger = logging.getLogger("workshop.auth.ldap")

  uri = settings.LDAP_AUTH['uri']
  base = settings.LDAP_AUTH['base']
  secure = settings.LDAP_AUTH['secure']
  search_filter = settings.LDAP_AUTH['search_filter']
  attributes = settings.LDAP_AUTH['attributes']
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
      results = l.search_s(self.base,
                          ldap.SCOPE_SUBTREE,
                          self.search_filter % username,
                          attrlist=self.attributes.keys())
      results = results[0][1]

      # split results into user/profile attributes and normalize field names
      attributes = {'user': {}, 'profile': {}}
      for attr in self.attributes:
        (obj, field) = self.attributes[attr].split('.')
        attributes[obj][field] = results.get(attr, [''])

      # see if we have a user
      try:
        user = User.objects.get(username=username)
      except User.DoesNotExist:
        user = User.objects.create_user(username)

      # update the user with the current directory information
      user.first_name = attributes['user']['first_name'][0]
      user.last_name = attributes['user']['last_name'][0]
      user.email = attributes['user']['email'][0]
      user.save()

      # see if the user has a profile
      try:
        profile = user.profile
      except Profile.DoesNotExist:
        profile = Profile()

      # update the user's profile
      profile.employee_id = attributes['profile']['employee_id'][0]
      profile.phone_number = attributes['profile']['phone_number'][0]
      profile.mailbox = attributes['profile']['mailbox'][0]
      profile.department = attributes['profile']['department'][0]
      profile.nickname = attributes['profile']['nickname'][0]
      # affiliation is handled a little differently, we need to check to see
      # if 'faculty' or 'staff' is in the affiliation list
      if "faculty" in attributes['profile']['affiliation']:
        profile.affiliation = "faculty"
      elif "staff" in attributes['profile']['affiliation']:
        profile.affiliation = "staff"
      else:
        profile.affiliation = "other"

      # if there is no employee_id, set it to all zeros
      if not profile.employee_id:
        profile.employee_id = '000000000'

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
      if l:
        l.unbind_s()

    return None


  def get_user(self, user_id):
    try:
      return User.objects.get(pk=user_id)
    except User.DoesNotExist:
      return None
