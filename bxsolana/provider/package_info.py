import pkg_resources

dist = pkg_resources.get_distribution("bxsolana-trader")
NAME = dist.project_name
VERSION = dist.version
