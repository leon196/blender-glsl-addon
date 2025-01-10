# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

import bpy

from . import Metadata
from . import Panel
from . import auto_load

auto_load.init()

def register():

    auto_load.register()

    bpy.types.Object.metadata = bpy.props.PointerProperty(type=Metadata.Metadata)
    bpy.types.Scene.framedata = bpy.props.PointerProperty(type=Metadata.FrameData)

    for panel in Panel.get_panels():
        panel.COMPAT_ENGINES.add('SHADER')

def unregister():

    auto_load.unregister()

    del bpy.types.Object.metadata
    del bpy.types.Scene.framedata

    for panel in Panel.get_panels():
        if 'SHADER' in panel.COMPAT_ENGINES:
            panel.COMPAT_ENGINES.remove('SHADER')

if __name__ == "__main__":
    register()