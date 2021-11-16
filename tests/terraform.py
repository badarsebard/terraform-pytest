import os
import pathlib
import shutil
from _pytest.tmpdir import TempPathFactory
from python_terraform import Terraform, IsFlagged


class TerraformInitFailure(BaseException):
    pass


class TerraformValidationError(BaseException):
    pass


class TerraformApplyError(BaseException):
    pass


class TerraformDestroyError(BaseException):
    pass


class TerraformManager(Terraform):
    def __init__(self,
                 provider: str = None,
                 module: str = ".",
                 path_factory: TempPathFactory = None,
                 env_vars: dict = None):
        if env_vars is not None and type(env_vars) == dict:
            for v in env_vars.copy():
                env_vars[f"TF_VAR_{v}"] = env_vars[v]
            os.environ.update(env_vars)
        wd = str(path_factory.mktemp("terraform"))
        cwd = str((pathlib.Path() / module).absolute())
        shutil.copytree(cwd, wd, dirs_exist_ok=True,
                        ignore=shutil.ignore_patterns("*.tfstate",
                                                      ".terraform",
                                                      ".terraform.lock.hcl"
                                                      ))
        if provider:
            shutil.copy(str(pathlib.Path()/provider), wd)
        super().__init__(working_dir=wd)
        return_code, stdout, stderr = self.init()
        if return_code:
            print(stderr)
            raise TerraformInitFailure

    def __enter__(self):
        # validate
        return_code, stdout, stderr = self.cmd('validate', no_color=IsFlagged)
        if return_code:
            print(stderr)
            raise TerraformValidationError
        # apply
        return_code, stdout, stderr = self.apply(skip_plan=True, no_color=IsFlagged)
        if return_code:
            print(stderr)
            raise TerraformApplyError
        self.read_state_file(file_path='terraform.tfstate')
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        # destroy
        return_code, stdout, stderr = self.cmd('apply',
                                               destroy=IsFlagged,
                                               no_color=IsFlagged,
                                               auto_approve=IsFlagged)
        if return_code:
            print(stderr)
            raise TerraformDestroyError
