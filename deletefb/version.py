import pkg_resources  # part of setuptools

try:
    version = pkg_resources.require("delete-facebook-posts")[0].version
except pkg_resources.DistributionNotFound:
    version = "source"
