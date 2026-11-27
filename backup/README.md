# Sylva 3D backup · 27 November 2026

[Download the backup assets from GitHub Releases](https://github.com/SAmsonZh0ng/sylva/releases/tag/sylva-3d-backup-2026-11-27).

This snapshot contains 56,569 project files, including 95 Blender files and 31 Blender backup saves. It includes Sylva product and foundation geometry, intro film iterations, assembly and inspection, plant and scaling studies, GLB exports, texture inputs, production scripts, and rendered frames, proofs, and videos. Source files and renders are preserved as saved. Course files, logs, machine configuration, and third-party IWC/Agera review screenshots are outside the snapshot.

## Restore

1. Download all 43 `sylva-*.zip` files, `sylva-file-inventory.json.gz`, and `restore-sylva.py` into one folder. Allow about 56 GiB of free space for the downloaded archives and restored files together.
2. With Python 3.11 or later, run the following command from the download directory. Use a new or empty destination.

   ```powershell
   python restore-sylva.py . C:/Sylva-Restore
   ```

3. The script checks the SHA-256 of each archive before extracting, recreates duplicate files at their original relative paths, and verifies every restored file. A single ZIP works for browsing its contents. Use the restore script and full download set to reconstruct the original layout.

## Scene entry points

| Work | File under the restore root |
| --- | --- |
| Product | `output/product/Sylva Product.blend` |
| Precision cinema | `output/precision/Sylva Precision Cinema.blend` |
| Foundation R02 | `output/foundation-remodel/Sylva Foundation R02 - working.blend` |
| Matched intro | `output/film-r11c/Sylva Film R11C Matched Logo Reveal.blend` |
| Complete film | `output/film-r12/Sylva Complete Film R12.blend` |
| Assembly | `output/film-r13-integration/Sylva R13 Corrected Assembly.blend` |
| Plant R38 desktop and portrait | `output/plant-cycles-r01/web-r38/` |
| Scaling conservatory | `output/scaling-r01/realism-r02/Sylva Scaling Conservatory R02.blend` |

## Reproduce scenes and renders

The source scenes were checked with Blender 5.3.0. Many production scripts record Blender 5.2.3 LTS and use absolute paths to their original workspace, Blender or media encoder. Adjust those paths and follow the script and scene notes in the relevant output folder before rendering. Existing renders and masters can be used directly. Regenerating externally generated video may depend on the original service and model. The rendered outputs and available job inputs are retained.

Some plant scenes reference three dirt textures via `E:/NUS/EE1111A`. The snapshot includes those textures. When restoring elsewhere, download `relink-sylva.py` and run the example below with the current Blender executable. The script saves a separate `*.relinked.blend` alongside the restored original whenever it changes an image path.

```powershell
blender --background --factory-startup --disable-autoexec --python-exit-code 1 --python relink-sylva.py -- C:/Sylva-Restore 'C:/Sylva-Restore/output/plant-cycles-r01/Sylva Cycles Soil r38.blend'
```

The older `output/plant-story-realism-r01/Sylva Calathea Studio.blend1` points to three missing PNGs at a former website path. The relink script offers the retained `web-originals` atlases as replacements. Their identity with those missing files could not be verified. Some imported assets retain historical authoring paths under other machines, and several scenes retain an obsolete Blender 5.2 bundled paint-brush library reference. Blender opened all 126 inspected files. Restoring byte-for-byte and opening a file do not verify every scene’s original rendered appearance.

Keep the included provenance and attribution files with reused assets. The Poly Haven assets are documented as CC0 in the project manifests. The Mokkie Calathea photograph and derivative atlas in `output/plant-story-realism-r01` carry CC BY-SA 3.0 attribution, as recorded in `SOURCES.md`, `pass-4/CREDITS.txt`, and the accompanying provenance.
