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

Calling ansible::

    action: ansible
    input:
      hosts: '*'
      module: copy
      module_args: 'src=file.txt dest=/root/file.txt'
      remote_user: stack
      become: true
      become_user: root
      tags: tag1
      skip_tags: tag2

Call ansible playbook::

    action: ansible-playbook
    input:
      limit_hosts: overcloud-controller-0
      playbook: /home/stack/ansible/my_playbook.yaml
      remote_user: stack
      become: true
      become_user: root
      tags: tag1
      skip_tags: tag2


Plans/Ideas
-----------

- "directory" should probably be renamed to "cwd" or something
- We only support the ansible-playbook command, others should be added.
- We only support the very minimum options for the ansible-playbook command,
  more should be exposed.
