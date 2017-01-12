Mistral Actions for Ansible
---------------------------

Note: This project is experimental and in infancy. It might work for you.


Install
~~~~~~~

The actions can be installed via pip, then we need to tell Mistral about them
and restart Mistral::

    pip install mistral-ansible-actions;
    sudo mistral-db-manage populate;
    systemctrl restart openstack-mistral*;


Usage
-----

Simple task example::

    task:
      action: ansible.playbook
      input:
        playbook: path/to/playbook.yaml

Optionally the directory can be provided if you want to execute the
ansible-playbook command from a specific location::

    task:
      action: ansible.playbook
      input:
        playbook: playbook.yaml
        directory: path/to


Plans/Ideas
-----------

- "directory" should probably be renamed to "cwd" or something
- We only support the ansible-playbook command, others should be added.
- We only support the very minimum options for the ansible-playbook command,
  more should be exposed.
