CFO
=============

Plataforma de e-learning para os cursos oferecidos pela EPMF.

Dependências
------------

* VirtualBox 5+

 * PS: NÃO INSTALAR O VIRTUALBOX PELO REPOSITÓRIO DO UBUNTU, POIS ELE ESTÁ BUGADO,
   DAR PREFERÊNCIA PARA O REPOSITÓRIO OFICIAL DELES

* Vagrant 1.7.4+

# TODO: Informações de instalação dos dois.


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
