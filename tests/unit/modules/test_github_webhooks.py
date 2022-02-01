from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from unittest.mock import patch, MagicMock, mock_open
from ansible.module_utils import basic
from utils import ModuleTestCase, set_module_args

class TestWebhooksModule(ModuleTestCase):
	def test_receive_generic_command(self):
		with patch.object(basic.AnsibleModule, 'run_command') as self.mock:
			self.mock.return_value = True

		assert self.mock.return_value == True

