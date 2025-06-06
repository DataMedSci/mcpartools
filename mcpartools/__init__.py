# mcpartools/__init__.py
try:
    from ._version import version as __version__
except ImportError:
    # Fallback for when the package is not installed in editable mode or
    # setuptools_scm hasn't generated _version.py yet (e.g., bare Git clone)
    __version__ = "0.0.0+unknown"
