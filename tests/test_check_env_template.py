import pytest

from pch.check_env_template import main as check_env_template
from testing_utils import get_resource_path


@pytest.mark.parametrize('envfile,template,ignore,expected_retval', (
        (get_resource_path('env'), get_resource_path('env.tpl'), "", 1),
        (get_resource_path('env'), get_resource_path('env.tpl'), "-i ENV2 -i ALIEN1", 0),
        (get_resource_path('env'), get_resource_path('env'), "", 0)
))
def test_check_env_template(envfile, template, ignore, expected_retval):
    ignored = ignore.split()
    ret = check_env_template(["-e", envfile, '-t', template] + ignored)
    assert ret == expected_retval
