"""
This module implements the :class:`Label` object. A label
represents an obfuscated truth value. By default, the label
is represented as a random 256 bitstring, but the label
is encoded in base64 for the user. To change the length
of the bitstring, head to :mod:`gabes.settings`.
"""

import os
import base64
import gabes.settings as settings
from gabes.prg import SeedPRG

class Label(object):
    """
        The :class:`Label` object, which contains the label
        that will represent either the boolean *False* or *True* for a
        particular gate.

        :param bool represents: (optional) the boolean value this label \
        represents
        :param bool pp_bit: (optional) the point-and-permute bit

        .. code-block:: python

            >>> from gabes.label import Label
            >>> label = Label(0, pp_bit=True)
            >>> label.label
            b'y\\x8c\\xc4C\\x99\\x9c\\x1d&\\xa3R\\xdbB\\xcep-\\xc5
            \\xe9R=\\xc1\\xd8\\xaeq}\\xe0c\\x80\\xd8g\\xac_\\x96'
            >>> label.to_base64()
            b'eYzEQ5mcHSajUttCznAtxelSPcHYrnF94GOA2GesX5Y='
    """

    def __init__(self, represents, pp_bit=None, PRG=os.urandom):
        """
            Initializes the label with a random 256 bitstring
            and sets the boolean value it represents.

            :param bool represents: the boolean value this label represents
            :param bool pp_bit: the point-and-permute bit
            :param PRG: (optional) a pseudo-random generator to use
        """
        self.label = None
        if isinstance(PRG, SeedPRG):
            self.label = PRG.randbytes(settings.NUM_BYTES)
        else:
            self.label = os.urandom(settings.NUM_BYTES)
            # print("Warning: Using os.urandom() for label generation. "
            #       "Consider using SeedPRG for reproducibility.")
        self.represents = represents
        self.pp_bit = pp_bit

    def __repr__(self):
        return str(self.to_base64())

    def __str__(self):
        return str(self.to_base64())

    def __int__(self):
        """
            Converts the label into an integer.

            :return: the label as an integer
            :rtype: int
        """
        return int.from_bytes(self.label, byteorder='big')

    def to_base64(self):
        """
            Returns the label encoded in base64.

            :return: the label in base64
            :rtype: str
        """
        return base64.urlsafe_b64encode(self.label)

    def to_base32(self):
        """
            Returns the label encoded in base32.

            :return: the label in base32
            :rtype: str
        """
        return base64.b32encode(self.label)

    @staticmethod
    def int_to_bytes(n):
        return int.to_bytes(n, length=32, byteorder='big')
