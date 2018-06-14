# pylint: disable=too-many-ancestors
"""
Views for organizations end points.
"""
from edx_rest_framework_extensions.authentication import JwtAuthentication
from rest_framework import viewsets
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework_oauth.authentication import OAuth2Authentication

from organizations.models import Organization
from organizations.serializers import OrganizationSerializer

from openedx.core.djangoapps.site_configuration import helpers as configuration_helpers


class OrganizationsViewSet(viewsets.ReadOnlyModelViewSet):
    """Organization view to fetch list organization data or single organization
    using organization short name.
    """
    serializer_class = OrganizationSerializer
    lookup_field = 'short_name'
    authentication_classes = (OAuth2Authentication, JwtAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """
        The organizations will be filtered by the current site list of available orgs
        """
        site_orgs = configuration_helpers.get_value('course_org_filter', False)
        if site_orgs:
            return Organization.objects.filter(
                active=True,
                short_name__iregex=r'(^' + '$|^'.join(site_orgs) + '$)'
            )  # pylint: disable=no-member
        else:
            return Organization.objects.filter(active=True)  # pylint: disable=no-member
