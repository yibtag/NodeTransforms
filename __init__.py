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

class NT_PGT_Transform(bpy.types.PropertyGroup):
    node_x: bpy.props.FloatProperty(name="Node X", default=0.0)
    node_y: bpy.props.FloatProperty(name="Node Y", default=0.0)

    node_width: bpy.props.FloatProperty(name="Node Width", default=0.0)
    node_height: bpy.props.FloatProperty(name="Node Height", default=0.0)

    snap_mode: bpy.props.EnumProperty(
        name="Side",
        items={
            ("x", "X Axis", ""),
            ("y", "Y Axis", ""),
            ("xy", "X And Y Axis", "")
        },
        default="x"
    )

class NT_PT_Transform(bpy.types.Panel):
    bl_idname = "NT_PT_Transform"
    bl_label = "Transform"

    bl_space_type = "NODE_EDITOR"
    bl_region_type = "UI"
    bl_category = "Transform"

    def draw(self, context):
        props = context.scene.node_transform_props

        self.layout.label(text="Position:")
        self.layout.prop(props, "node_x")
        self.layout.prop(props, "node_y")

        self.layout.label(text="Size:")
        self.layout.prop(props, "node_width")
        self.layout.prop(props, "node_height")

        self.layout.separator()
        self.layout.operator("node.get_transform", text="Get Transform", icon="COPYDOWN")
        self.layout.operator("node.set_transform", text="Set Transform", icon="SNAP_VOLUME")

        self.layout.label(text="Snapping:")
        self.layout.prop(props, "snap_mode")
        self.layout.operator("node.snap_nodes", text="Snap nodes", icon="SNAP_ON")

class NT_OT_GetTransform(bpy.types.Operator):
    bl_idname = "node.get_transform"
    bl_label = "Get Node Transform"

    def execute(self, context):
        if not context.space_data.type == "NODE_EDITOR":
            return { "FINISHED" }
    
        if not context.selected_nodes:
            return { "FINISHED" }
        
        props = context.scene.node_transform_props

        node = context.selected_nodes[0]
        props.node_x = node.location.x
        props.node_y = node.location.y
        props.node_width = node.width
        props.node_height = node.height
        
        return { "FINISHED" }

class NT_OT_SetTransform(bpy.types.Operator):
    bl_idname = "node.set_transform"
    bl_label = "Set Node Transform"

    def execute(self, context):
        if not context.space_data.type == "NODE_EDITOR":
            return { "FINISHED" }
    
        if not context.selected_nodes:
            return { "FINISHED" }
        
        props = context.scene.node_transform_props

        node = context.selected_nodes[0]
        node.location.x = props.node_x
        node.location.y = props.node_y
        node.width = props.node_width
        node.height = props.node_height

        return { "FINISHED" }
    
class NT_OT_SnapNodes(bpy.types.Operator):
    bl_idname = "node.snap_nodes"
    bl_label = "Snap nodes"

    def execute(self, context):
        if not context.space_data.type == "NODE_EDITOR":
            return { "FINISHED" }
        
        if not len(context.selected_nodes) > 1:
            return { "FINISHED" }
        
        snap_mode = context.scene.node_transform_props.snap_mode

        node = context.selected_nodes[0]
        target = context.selected_nodes[1]

        if snap_mode == "x":
            node.location.x = target.location.x
        elif snap_mode == "y":
            node.location.y = target.location.y
        elif snap_mode == "xy":
            node.location.x = target.location.x
            node.location.y = target.location.y

        return { "FINISHED" }
        


classes = [
    NT_PGT_Transform,
    NT_PT_Transform,
    NT_OT_GetTransform,
    NT_OT_SetTransform,
    NT_OT_SnapNodes
]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.Scene.node_transform_props = bpy.props.PointerProperty(type=NT_PGT_Transform)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

    del bpy.types.Scene.node_transform_props