bl_info = {
    "name": "Select All then Save (Alt/Option+S) - Object Mode",
    "author": "ChatGPT",
    "version": (1, 3, 0),
    "blender": (3, 0, 0),
    "location": "Alt/Option + S (Object Mode)",
    "description": "Seleciona todos os objetos visíveis/selecionáveis e salva. Se o arquivo nunca foi salvo, abre 'Save As'. Atalho: Alt/Option+S apenas no Object Mode.",
    "category": "System",
}

import bpy

def select_all_visible_and_selectable(context):
    try:
        if context.mode != 'OBJECT':
            bpy.ops.object.mode_set(mode='OBJECT')
    except Exception:
        pass

    vl = context.view_layer

    for o in vl.objects:
        try:
            o.select_set(False)
        except Exception:
            pass

    first = None
    for o in vl.objects:
        try:
            if o.visible_get() and not o.hide_select:
                o.select_set(True)
                if first is None:
                    first = o
        except Exception:
            pass

    try:
        if first is not None:
            vl.objects.active = first
    except Exception:
        pass

class WM_OT_select_all_then_save_alt(bpy.types.Operator):
    bl_idname = "wm.select_all_then_save_alt"
    bl_label = "Selecionar tudo (robusto) e salvar — Alt/Option+S"
    bl_options = {'REGISTER'}

    @classmethod
    def poll(cls, context):
        return context.mode == 'OBJECT'

    def execute(self, context):
        select_all_visible_and_selectable(context)

        if not bpy.data.filepath:
            bpy.ops.wm.save_as_mainfile('INVOKE_DEFAULT')
            self.report({'INFO'}, "Tudo selecionado — escolha onde salvar.")
        else:
            bpy.ops.wm.save_mainfile()
            self.report({'INFO'}, "Tudo selecionado e salvo.")
        return {'FINISHED'}

addon_keymaps = []

def register():
    bpy.utils.register_class(WM_OT_select_all_then_save_alt)

    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    if kc:
        km = kc.keymaps.new(name='Object Non-modal', space_type='EMPTY')
        kmi = km.keymap_items.new(
            WM_OT_select_all_then_save_alt.bl_idname,
            'S',
            'PRESS',
            alt=True
        )
        addon_keymaps.append((km, kmi))

def unregister():
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()

    bpy.utils.unregister_class(WM_OT_select_all_then_save_alt)

if __name__ == "__main__":
    register()
