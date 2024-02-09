import sys
from unittest import TestCase

from bx_py_utils.path import assert_is_file
from cli_base.cli_tools.code_style import assert_code_style
from cli_base.cli_tools.subprocess_utils import verbose_check_output
from manageprojects.test_utils.project_setup import check_editor_config, get_py_max_line_length
from packaging.version import Version

from inverter import __version__
from inverter.constants import PACKAGE_ROOT


class ProjectSetupTestCase(TestCase):
    app_cli_bin = PACKAGE_ROOT / 'cli.py'
    dev_cli_bin = PACKAGE_ROOT / 'dev-cli.py'

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()

        assert_is_file(cls.app_cli_bin)
        assert_is_file(cls.dev_cli_bin)

    def test_version(self):
        self.assertIsNotNone(__version__)

        version = Version(__version__)  # Will raise InvalidVersion() if wrong formatted
        self.assertEqual(str(version), __version__)

        # The "app" cli:
        output = verbose_check_output(sys.executable, self.app_cli_bin, 'version')
        self.assertIn(f'inverter v{__version__}', output)

        # The "development" cli:
        output = verbose_check_output(sys.executable, self.dev_cli_bin, 'version')
        self.assertIn(f'inverter v{__version__}', output)

    def test_code_style(self):
        return_code = assert_code_style(package_root=PACKAGE_ROOT)
        self.assertEqual(return_code, 0, 'Code style error, see output above!')

    def test_check_editor_config(self):
        check_editor_config(package_root=PACKAGE_ROOT)

        max_line_length = get_py_max_line_length(package_root=PACKAGE_ROOT)
        self.assertEqual(max_line_length, 119)
