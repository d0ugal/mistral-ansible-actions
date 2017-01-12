from mistral.actions import base
from oslo_concurrency import processutils


class AnsiblePlaybookAction(base.Action):

    def __init__(self, playbook, directory=None):
        self.playbook = playbook
        self.directory = directory

    def run(self):
        stderr, stdout = processutils.execute(
            'ansible-playbook', self.playbook, cwd=self.directory,
            log_errors=processutils.LogErrors.ALL)
        return {"stderr": stderr, "stdout": stdout}
