# terraform-pytest

This is a simple example of how to use `pytest` to test Terraform configurations. PyTest is a useful library for writing tests in Python and can be used to collect, execute, and provide results of tests. This repo uses PyTest in conjunction with a custom Python context manager to create and deploy the provided Terraform code, execute tests, and then attempt to teardown the created resources. The context manager relies on the `python_terraform` library which handles executing the Terraform binary on the host system using the `subprocess` library.

# pre-requisites

- Terraform binary on the host system (this is untested with most newer Terraform versions, so ymmv)

# usage

From the root of the project, execute the pytest command:
```bash
pytest tests
```

The context manager will automatically create a temporary working directory, copy the Terraform contents to it and then perform the following commands: init, validate, and apply. After the apply step is complete the tests will execute, and once finished the context manager will perform a destroy.

In the example `conftest.y` the `tfenv` fixture is scoped to the session, which means the context will run only once per pytest execution. You can change the scope so that it will execute for each test but this will likely increase your testing time significantly as Terraform will need to apply and detroy the same resources with each iteration.

# customizing

The context manager can be customized using its arguments for provider, module, path_factory, and env_vars. The env_vars argument will take in a dictionary and create environment variables that are prepended with the TF_VAR_ string. The path_factory argument specifies a class that creates a temporary directory. In the example the TempPathFactory class included with PyTest is used. The provider and module arguments specify what directories are copied to the temporary directory. By default the current working directory is used for the module parameter and it represents the location of the terraform code to be tested. If your Terraform code exists in a subdirectory from the root of your project you need to pass in a string of its relative location. The provider argument works similarly and is used to copy and Terraform submodules that may be needed for the configuration if they are not part of the module path. 
