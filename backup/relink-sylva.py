"""Run inside Blender to create a portable copy of a restored scene."""

import sys
from pathlib import Path, PureWindowsPath

import bpy


ORIGINAL_ROOT = PureWindowsPath("E:/NUS/EE1111A")
PLANT_STUDY = Path("output/plant-story-realism-r01")
ORIGINAL_ATLAS = Path("sites/ee01-product/dist/assets/plant-realism")
ATLAS_NAMES = {"leaf-albedo.png", "leaf-normal.png", "leaf-roughness.png"}


root, scene = [Path(arg).resolve() for arg in sys.argv[sys.argv.index("--") + 1:]]
if not scene.is_relative_to(root):
    raise ValueError("The Blender file must be inside the restored workspace")

destination = scene.with_name(scene.name + ".relinked.blend")
if destination.exists():
    raise FileExistsError(destination)

bpy.ops.wm.open_mainfile(filepath=str(scene), use_scripts=False, load_ui=False)
changes = 0
for image in bpy.data.images:
    if not image.filepath or image.packed_files or image.source != 'FILE' or image.library:
        continue
    original = PureWindowsPath(image.filepath)
    current = Path(bpy.path.abspath(image.filepath.replace("\\", "/"))).resolve()
    if original.is_relative_to(ORIGINAL_ROOT) and not image.filepath.startswith("//"):
        replacement = root.joinpath(*original.relative_to(ORIGINAL_ROOT).parts)
    elif current.parent == root / ORIGINAL_ATLAS and current.name in ATLAS_NAMES and not current.is_file():
        replacement = root / PLANT_STUDY / "web-originals" / current.name
    else:
        continue
    if not replacement.is_file():
        raise FileNotFoundError(replacement)
    image.filepath = bpy.path.relpath(str(replacement), start=str(scene.parent))
    changes += 1

if changes:
    bpy.ops.wm.save_as_mainfile(filepath=str(destination), relative_remap=False, copy=True)
    print(f"Relinked {changes} image paths in {destination}")
else:
    print("This scene did not need any of the known texture paths relinked")
