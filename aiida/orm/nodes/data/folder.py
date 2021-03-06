# -*- coding: utf-8 -*-
###########################################################################
# Copyright (c), The AiiDA team. All rights reserved.                     #
# This file is part of the AiiDA code.                                    #
#                                                                         #
# The code is hosted on GitHub at https://github.com/aiidateam/aiida_core #
# For further information on the license, see the LICENSE.txt file        #
# For further information please visit http://www.aiida.net               #
###########################################################################
"""`Data` sub class to represent a folder on a file system."""
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

from .data import Data

__all__ = ('FolderData',)


class FolderData(Data):
    """`Data` sub class to represent a folder on a file system."""
