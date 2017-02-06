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
                 become=None, become_user=None, extra_vars=None):

        self.playbook = playbook
        self.limit_hosts = limit_hosts
        self.remote_user = remote_user
        self.become = become
        self.become_user = become_user
        self.extra_vars = extra_vars

    def run(self):

        command = ['ansible-playbook', self.playbook]

        if self.limit_hosts:
            command.extend(['--args', self.limit_hosts])

        if self.remote_user:
            command.extend(['--user', self.remote_user])

        if self.become:
            command.extend(['--become'])

        if self.become_user:
            command.extend(['--become-user', self.become_user])

        if self.extra_vars:
            command.extend(['--extra-vars', self.extra_vars])

        stderr, stdout = processutils.execute(
            *command, log_errors=processutils.LogErrors.ALL)
        return {"stderr": stderr, "stdout": stdout}
