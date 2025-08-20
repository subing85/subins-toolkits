# Copyright (c) 2025, Motion-Craft-Works Production All rights reserved.
# Author: Subin. Gopi (motioncraftworks85@gmail.com, subing85@gmail.com).
# Description: Motion-Craft-Works ID - Card  Resolver queue stack management source code.
# WARNING! All changes made in this file will be lost when recompiling UI file!


from __future__ import absolute_import


class Pause(object):
    def __init__(self, node):
        self.node = node

    def __enter__(self):  # Opens pause chunk.
        self.node.pause = True

    def __exit__(self, *args):  # Close pause chunk.
        self.node.pause = False


if __name__ == "__main__":
    pass
