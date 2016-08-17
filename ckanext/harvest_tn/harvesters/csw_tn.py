# -*- coding: utf-8 -*-

import logging
import requests
import StringIO
import urllib
import urlparse

from lxml import etree

from ckanext.spatial.harvesters.csw import CSWHarvester


log = logging.getLogger(__name__)


class CSWTNHarvester(CSWHarvester):

    def info(self):
        return {
            'name': 'csw_tn',
            'title': 'CSW Server for Trento',
            'description': 'CSW harvester with customizations for TN'
            }

    def fetch_stage(self,harvest_object):
        """
        La maggior parte del codice è copiata dal CSWHarvester.
        La connessione deve essere però effettuata direttamente e non tramite owslib poichè
        il GN di TN non risponde alla GetRecordsById in modo standard
        (i.e. manca l'envelope csw:GetRecordByIdResponse al gmd:MD:Metadata)
        """

        # Check harvest object status
        status = self._get_object_extra(harvest_object, 'status')

        if status == 'delete':
            # No need to fetch anything, just pass to the import stage
            return True

        log.debug('CswTNHarvester fetch_stage for object: %s', harvest_object.id)

        identifier = harvest_object.guid
        try:
            xml = self.getrecordbyid(harvest_object)
        except Exception, e:
            log.info('CswTNHarvester error in getrecordbyid for guid %s: %s', harvest_object.guid, e)
            self._save_object_error('Error getting the CSW record with GUID %s' % identifier, harvest_object)
            return False

        if xml is None:
            self._save_object_error('Empty record for GUID %s' % identifier,
                                    harvest_object)
            return False

        try:
            harvest_object.content = xml.strip()
            harvest_object.save()
        except Exception,e:
            self._save_object_error('Error saving the harvest object for GUID %s [%r]' % \
                                    (identifier, e), harvest_object)
            return False

        log.debug('XML content saved (len %s)', len(xml))
        return True

    def getrecordbyid(self, harvest_object):
        """
        :return an XML string
        """

        url = self.build_url(harvest_object)
        log.debug('CswTNHarvester getrecordbyid(%s): %s', harvest_object.guid, url)

        getrecord = requests.get(url)
        getrecord.raise_for_status()

        exml = etree.parse(StringIO.StringIO(getrecord.content))

        mdlist = exml.xpath("descendant-or-self::gmd:MD_Metadata",namespaces={"gmd":"http://www.isotc211.org/2005/gmd"})
        if len(mdlist) == 0:
            return None

        md = mdlist[0]
        mdtree = etree.ElementTree(md)

        xml = None
        try:
            xml = etree.tostring(mdtree, pretty_print=True, encoding=unicode)
        except TypeError:
            # API incompatibilities between different flavours of elementtree
            try:
                xml = etree.tostring(mdtree, pretty_print=True, encoding=unicode)
            except AssertionError:
                xml = etree.tostring(md, pretty_print=True, encoding=unicode)

        return xml

    def build_url(self, harvest_object):

        parts = urlparse.urlparse(harvest_object.source.url)

        params = {
            'SERVICE': 'CSW',
            'VERSION': '2.0.2',
            'REQUEST': 'GetRecordById',
            'OUTPUTSCHEMA': 'http://www.isotc211.org/2005/gmd',
            'OUTPUTFORMAT':'application/xml' ,
            'ELEMENTSETNAME':'full' ,
            'ID': harvest_object.guid
        }

        url = urlparse.urlunparse((
            parts.scheme,
            parts.netloc,
            parts.path,
            None,
            urllib.urlencode(params),
            None
        ))

        return url
