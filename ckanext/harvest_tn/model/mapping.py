# -*- coding: utf-8 -*-

import json
import logging
import datetime

from hashlib import sha1

from ckanext.harvest_tn.model.statweb_metadata import StatWebMetadataPro, StatWebMetadataSubPro

log = logging.getLogger(__name__)

tags_remove = [
    'rdnt', 'siat', 'pup', 'db prior 10k', 'pup; rndt',
    'inquadramenti di base', 'suap', 'scritte', 'pupagri', 'pupasc', 'pupbos',
]

tags_subs = {
    'bosc':             'boschi',
    'comun':            'comuni',
    'siti archeolog':   'siti archeologici',
    'archeolog':        'archeologia',
    'specchio d\'acqua': 'specchi d\'acqua',
    'tratte':           'tratte ferroviarie',
    'viabilità di progetto':    'viabilità',
    'viabilità ferroviaria':    'viabilità',
    'viafer':                   'viabilità',
    'viabilità forestale':      'viabilità',
    'zps':                      'zone protezione speciale',
    'udf':                      'distretti forestali',
    'uffici distrettuali forestali': 'distretti forestali',
    'pascolo':                  'pascoli',
    'idrografici':              'idrografia',
}

# mappa Settore verso Categorie
cat_map_pro = {
    u'agricoltura':     'Economia',
    u'pesca':           'Economia',
    u'silvicoltura':    'Economia',
    u'commercio con l\'estero':     'Economia',
    u'commercio con l\'estero e internazionalizzazione': 'Economia',
    u'internazionalizzazione':      'Economia',
    u'conti economici':             'Economia',
    u'pubblica amministrazione': 'Amministrazione',
    u'istruzione formazione':   'Conoscenza',
    u'ricerca':                 'Conoscenza',
    u'sviluppo e innovazione':  'Conoscenza',
    u'mercato del lavoro':               'Welfare',
    u'salute':                           'Welfare',
    u'famiglie e comportamenti sociali': 'Welfare',
    u'assistenza e protezione sociale':  'Welfare',
    u'popolazione':                      'Demografia',
    u'società dell\'informazione':       'Demografia',
}

cat_map_sub = {
    "l'ambiente e il territorio":   "Gestione del territorio",
    'le infrastrutture':            "Gestione del territorio",
    'popolazione':                  "Demografia",
    'famiglie e comportamenti sociali': 'Demografia',
    'istruzione e formazione':      'Conoscenza',
    'mercato del lavoro':           'Economia',
    'le imprese, la formazione e la valorizzazione del capitale produttivo':
                                    'Economia',
    'agricoltura':                  'Economia',
    'servizi':                      'Economia',
    'agricoltura, silvicoltura, pesca': 'Economia',
}

tipoindicatore_map = {
    'R': 'Rapporto',
    'M': 'Media',
    'I': 'Incremento anno precedente',
}

def create_base_dict(guid, metadata, config):
    """
    metadata : StatWebMetadata
       The base statweb metadata object
       
    config : dict
       The configuration set at harvester level
    """

    def dateformat(d):
        return d.strftime(r"%d/%m/%Y %H:%M")
        return d.isoformat()

    start_date = metadata.get_anno_inizio() or '1970'
    created = datetime.datetime(int(start_date), 1, 1)

    last_update = metadata.get_ultimo_aggiornamento() or "01/01/1970"
    day, month, year = [int(a) for a in last_update.split('/')]
    updated = datetime.datetime(year, month, day)

    now = dateformat(datetime.datetime.now())

    package_dict = {
        'title':             metadata.get_descrizione(),
        'groups':            config.get('groups', [{'name': 'statistica'}]),
        'author':           'Servizio Statistica',
        'author_email':     'serv.statistica@provincia.tn.it',
        'maintainer':       'Servizio Statistica',
        'maintainer_email': 'serv.statistica@provincia.tn.it',
        'metadata_modified': now,
         #'tags':              tags,  # i tag non sembrano essere valorizzati
        'license_id':       'cc-by',
        'license':          'Creative Commons Attribution',
        'license_title':    'Creative Commons Attribution 2.5 it',
        'license_url':      'http://creativecommons.org/licenses/by/2.5/it/',
        'isopen':            True,
        'resources':         []
    }

    extras = {
        'holder': 'Provincia Autonoma di Trento',
        'geographical_coverage': 'Provincia di Trento',
        'temporal_coverage_start': dateformat(created),
        'update_frequency': metadata.get_frequenza(),
        'publication_date': now,
        'revision_date': dateformat(updated),
        'encoding': 'UTF-8',
        'Algoritmo':         metadata.get_algoritmo(),
        'Anno di inizio':    metadata.get_anno_inizio(),
        'Measurement unit':  metadata.get_um(),
    }

    return package_dict, extras


def create_pro_package_dict(guid, metadata, config):
    """
    :param StatWebMetadataPro metadata:  The statweb metadata object for PRO level.
    ;param dict config:  The configuration set at harvester level.
    :return: the package dict.
    :rtype: dict
    """

    package_dict, extras = create_base_dict(guid, metadata, config)

    extras['Fenomeno'] =  metadata.get_fenomeno()
    extras['Confronti territoriali'] = metadata.get_confronti()
    extras['_harvest_source'] = 'statistica:' + guid

    package_dict['extras'] = _extras_as_dict(extras)


    category = cat_map_pro.get((metadata.get_settore() or 'default').lower(), 'Conoscenza')
    description = create_pro_description(metadata)

    package_dict['id'] = sha1('statistica:' + guid).hexdigest(),
    package_dict['url'] = 'http://www.statweb.provincia.tn.it/INDICATORISTRUTTURALI/ElencoIndicatori.aspx'
    package_dict['Categorie'] = category
    package_dict['notes'] = description

    return package_dict

def create_subpro_package_dict(guid, metadata, config):
    """
    metadata : StatWebMetadataSubPro
               The statweb metadata object for SUB PRO level

    config : dict
       The configuration set at harvester level
    """

    package_dict, extras = create_base_dict(guid, metadata, config)

    extras['Fonte'] =  metadata.get_fonte()
    extras['Tipo di Fenomeno'] =  metadata.get_tipo_fenomeno()
    extras['Tipo di Indicatore'] =  metadata.get_tipo_indicatore()
    extras['Settore'] =  metadata.get_settore()
    extras['Livello Geografico Minimo'] =  metadata.get_min_livello()
    extras['_harvest_source'] = 'statistica_subpro:' + guid

    package_dict['extras'] = _extras_as_dict(extras)

    category = cat_map_sub.get((metadata.get_settore() or 'default').lower(), 'Conoscenza')
    description = create_subpro_description(metadata)

    package_dict['id'] = sha1('statistica_subpro:' + guid).hexdigest(),
    package_dict['url'] = 'http://www.statweb.provincia.tn.it/INDICATORISTRUTTURALISubPro/'
    package_dict['Categorie'] = category
    package_dict['notes'] = description

    return package_dict

def create_pro_description(metadata):
    d = ''
    d = _add_field(d, 'Area', metadata.get_area())
    d = _add_field(d, 'Settore', metadata.get_settore())
    d = _add_field(d, 'Algoritmo', metadata.get_algoritmo())
    d = _add_field(d, 'Fenomeno', metadata.get_fenomeno())
    d = _add_field(d, 'Confronti territoriali', metadata.get_confronti())

    return d

def create_subpro_description(metadata):
    d = ''
    d = _add_field(d, 'Settore', metadata.get_settore())
    d = _add_field(d, 'Algoritmo', metadata.get_algoritmo())
    d = _add_field(d, 'Tipo Indicatore', tipoindicatore_map.get(metadata.get_tipo_indicatore()))
    d = _add_field(d, 'Livello Geografico Minimo', metadata.get_min_livello())

    return d

def _add_field(base, label, data):
    if data:
        return base + '**' + label + ':** ' + data + '\n\n'
    else:
        return base

def _extras_as_dict(extras):
    extras_as_dict = []
    for key, value in extras.iteritems():
        if isinstance(value, (list, dict)):
            extras_as_dict.append({'key': key, 'value': json.dumps(value)})
        else:
            extras_as_dict.append({'key': key, 'value': value})

    return extras_as_dict
