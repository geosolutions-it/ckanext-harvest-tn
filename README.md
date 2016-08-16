==================
ckanext-harvest-tn
==================

Definisce due plugin, `statwebpro_harvester` e `statwebsubpro_harvester` per harvesting di metadati a 
livello "pro" e "subpro" dai servizi esposti da http://www.statweb.provincia.tn.it/.

------------
Requirements
------------

Sviluppato e testato su CKAN 2.5.2.

Richiede che sia installato l'estensione harvester.


------------
Installation
------------

To install ckanext-harvest-tn:

1. Activate your CKAN virtual environment, for example::

     . /usr/lib/ckan/default/bin/activate

2. Install the `ckanext-harvest-tn` Python package into your virtual environment::

     pip install ckanext-harvest-tn

3. Add `statwebpro_harvester` and `statwebsubpro_harvester` to the ``ckan.plugins`` setting in your CKAN
   config file (by default the config file is located at
   ``/etc/ckan/default/production.ini``).

4. Restart CKAN. For example if you've deployed CKAN with Apache on Ubuntu::

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
