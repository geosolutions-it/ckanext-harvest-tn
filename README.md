==================
ckanext-harvest-tn
==================

Estensione CKAN per la Provincia di Trento

------
Plugin
------

Plugin definiti nell'estensione:

- ``statwebpro_harvester``: effettua harvesting dei metadati a livello "**pro**" dai servizi esposti da
  http://www.statweb.provincia.tn.it/.
- ``statwebsubpro_harvester``: effettua harvesting dei metadati a livello "**subpro**" dai servizi esposti da
  http://www.statweb.provincia.tn.it/.
- ``csw_tn_harvester``: effettua harvesting tramite CSW, bypassando la validazione del response alla chiamata *GetRecordById*, dato che l'elemento ``gmd:MD_Metadata`` ritornato dal servizio http://www.territorio.provincia.tn.it/geoportlet/srv/eng/csw non è incluso in un element ``csw:GetRecordByIdResponse``.


------------
Requirements
------------

Sviluppato e testato su CKAN 2.5.2.

Richiede che siano installate le estensioni ``ckanext-harvester`` e ``ckanext-spatial``.


------------
Installation
------------

To install ``ckanext-harvest-tn``:

1. Activate your CKAN virtual environment, for example::

     . /usr/lib/ckan/default/bin/activate

2. Install the ``ckanext-harvest-tn`` Python package into your virtual environment::

     pip install ckanext-harvest-tn

3. Add ``statwebpro_harvester`` and ``statwebsubpro_harvester`` to the ``ckan.plugins`` setting in your CKAN
   config file (by default the config file is located at ``/etc/ckan/default/production.ini``).

4. Add `csw_tn_harvester` to the ``ckan.plugins`` setting in your CKAN config file.

5. Restart CKAN. For example if you've deployed CKAN with Apache on Ubuntu::

     sudo service apache2 reload


------------------------
Development Installation
------------------------

To install `ckanext-harvest-tn` for development, activate your CKAN virtualenv and
do::

    git clone https://github.com/geosolution-it/ckanext-harvest-tn.git
    cd ckanext-harvest-tn
    python setup.py develop
    pip install -r dev-requirements.txt
