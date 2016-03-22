CFO
=============

Plataforma de e-learning para cursos.

Dependências
------------

* VirtualBox 5+
* Vagrant 1.7.4+

Instalação
----------

.. code:: bash

   $ vagrant up

Rodar o Sistema
---------------

.. code:: bash

   $ vagrant ssh
   <vagrant-machine> $ workon cfo
   <vagrant-machine> $ python manage.py runserver 0.0.0.0:8000
