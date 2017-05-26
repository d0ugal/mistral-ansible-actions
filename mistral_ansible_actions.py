import json
import os
import six
import tempfile

import yaml

from mistral.actions import base
from oslo_concurrency import processutils


class AnsibleAction(base.Action):

    def __init__(self, hosts, module=None, module_args=None, remote_user=None,
                 become=None, become_user=None):

        self.hosts = hosts
        self.module = module
        self.module_args = module_args
        self.remote_user = remote_user
        self.become = become
        self.become_user = become_user

    def run(self):

        command = ['ansible', self.hosts, ]

        if self.module:
            command.extend(['--module-name', self.module])

        if self.module_args:
            command.extend(['--args', self.module_args])

        if self.remote_user:
            command.extend(['--user', self.remote_user])

        if self.become:
            command.extend(['--become'])

        if self.become_user:
            command.extend(['--become-user', self.become_user])

        stderr, stdout = processutils.execute(
            *command, log_errors=processutils.LogErrors.ALL)
        return {"stderr": stderr, "stdout": stdout}


class AnsiblePlaybookAction(base.Action):

    def __init__(self, playbook, limit_hosts=None, remote_user=None,
                 become=None, become_user=None, extra_vars=None,
                 inventory=None, verbosity=5):

        self._playbook = playbook
        self.limit_hosts = limit_hosts
        self.remote_user = remote_user
        self.become = become
        self.become_user = become_user
        self.extra_vars = json.dumps(extra_vars)
        self._inventory = inventory
        self.verbosity = verbosity

    @property
    def inventory(self):
        if not self._inventory:
            return None

        # NOTE(flaper87): if it's a path, use it
        if (isinstance(self._inventory, six.string_types) and
            os.path.exists(self._inventory)):
            return open(self._inventory)

        # NOTE(flaper87):
        # We could probably catch parse errors here
        # but if we do, they won't be propagated and
        # we should not move forward with the action
        # if the inventory generation failed
        inventory = tempfile.NamedTemporaryFile(suffix='.yaml')
        inventory.write(yaml.dump(self._inventory))
        # NOTE(flaper87): We need to flush the memory
        # because we're neither filling up the buffer
        # nor closing the file.
        inventory.flush()
        return inventory

    @property
    def playbook(self):
        if not self._playbook:
            return None

        # NOTE(flaper87): if it's a path, use it
        if (isinstance(self._playbook, six.string_types) and
            os.path.exists(self._playbook)):
            return open(self._playbook)

        # NOTE(flaper87):
        # We could probably catch parse errors here
        # but if we do, they won't be propagated and
        # we should not move forward with the action
        # if the playbook generation failed
        playbook = tempfile.NamedTemporaryFile()
        playbook.write(yaml.dump(self._playbook))
        # NOTE(flaper87): We need to flush the memory
        # because we're neither filling up the buffer
        # nor closing the file.
        playbook.flush()
        return playbook

    def run(self):
        playbook = self.playbook
        if 0 < self.verbosity < 6:
            verbosity_option = '-' + ('v' * self.verbosity)
            command = ['ansible-playbook', verbosity_option, playbook.name]
        else:
            command = ['ansible-playbook', playbook.name]

        if self.limit_hosts:
            command.extend(['--limit', self.limit_hosts])

        if self.remote_user:
            command.extend(['--user', self.remote_user])

        if self.become:
            command.extend(['--become'])

        if self.become_user:
            command.extend(['--become-user', self.become_user])

        if self.extra_vars:
            command.extend(['--extra-vars', self.extra_vars])

        inventory = self.inventory
        if inventory:
            command.extend(['--inventory-file', inventory.name])

        try:
            stderr, stdout = processutils.execute(
                *command, log_errors=processutils.LogErrors.ALL)
            return {"stderr": stderr, "stdout": stdout}
        finally:
            # NOTE(flaper87): Close the file
            # this is important as it'll also cleanup
            # temporary files
            if inventory:
                inventory.close()

            playbook.close()
