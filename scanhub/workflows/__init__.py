"""Module for scanhub workflows."""

# Authors: Christoph Dinh <christoph.dinh@brain-link.de>
#          Johannes Behrens <johannes.behrens@brain-link.de>
#          David Schote <david.schote@brain-link.de>
#
# License: BSD-3-Clause

# PEP0440 compatible formatted version, see:
# https://www.python.org/dev/peps/pep-0440/
#
# Generic release markers:
#   X.Y
#   X.Y.Z   # For bugfix releases
#
# Admissible pre-release markers:
#   X.YaN   # Alpha release
#   X.YbN   # Beta release
#   X.YrcN  # Release Candidate
#   X.Y     # Final release
#
# Dev branch marker is: 'X.Y.devN' where N is an integer.
#

from .mri import (RecoJob)