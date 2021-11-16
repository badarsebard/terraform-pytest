from .terraform import TerraformManager
import pytest
from _pytest.tmpdir import TempPathFactory


@pytest.fixture(scope='session')
def tfenv(tmp_path_factory: TempPathFactory):
    env_vars = {
        
    }
    with TerraformManager(path_factory=tmp_path_factory, env_vars=env_vars) as deployment:
        yield deployment
