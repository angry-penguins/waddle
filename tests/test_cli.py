import os
from shutil import copyfile
from unittest import TestCase
from click.testing import CliRunner
from waddle import cli
from waddle.param_bunch import ParamBunch


class TestCli(TestCase):
    def test_cli(self):
        runner = CliRunner()
        result = runner.invoke(cli.main, ['--version'])
        self.assertIn('waddle', result.output)

    def test_add_key(self):
        filename = 'tests/conf/cli.yml'
        copyfile('tests/conf/nested.yml', filename)
        runner = CliRunner()
        runner.invoke(
            cli.main, [
                'add-key',
                'dev',
                filename,
            ])
        b = ParamBunch()
        b.load(filename=filename)
        self.assertGreater(len(b.meta.encryption_key), 0)
        self.assertEqual(b.meta.kms_key, 'dev')
        result = runner.invoke(
            cli.main, [
                'add-key',
                'dev',
                filename,
            ])
        self.assertIn('already has an encryption key', result.output)
        os.remove(filename)