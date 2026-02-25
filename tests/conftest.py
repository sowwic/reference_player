import pathlib
import pytest



@pytest.fixture(scope="session")
def output_dir() -> pathlib.Path:
    """Output directory for tests.

    Returns:
        pathlib.Path: path to test output directory.

    """
    out_dir = pathlib.Path.cwd() / ".test_output"
    out_dir.mkdir(exist_ok=True)
    return out_dir
