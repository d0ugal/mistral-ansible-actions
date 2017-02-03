Mistral Actions for Ansible
---------------------------

Note: This project is experimental and in infancy. It might work for you.

However, given interested users and the time I'd like to make it stable and
useful - so input and help is very welcome!


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

Call ansible playbook::

    action: ansible-playbook
    input:
      limit_hosts: overcloud-controller-0
      playbook: /home/stack/ansible/my_playbook.yaml
      remote_user: stack
      become: true
      become_user: root


Plans/Ideas
-----------

- We only support a subset of args ansible and ansible-playbook commands,
  more should be exposed. Maybe we can automatically add them all somehow?
