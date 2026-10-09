# ComfyUI Save Original Image

A lightweight custom node for [ComfyUI](https://github.com/comfyanonymous/ComfyUI) that saves images as **JPG or PNG** while preserving the original input filename, with an image preview in the node.

Originally developed for the [RTX Batch Upscaler – Image & Video workflow on Civitai](https://civitai.com/models/2990614/rtx-batch-upscaler-image-and-video), in collaboration with ChatGPT.

## Features

- JPG output with configurable quality (default: 95) and optimization
- Lossless PNG output with configurable compression level (0–9)
- Preserves the source filename stem for a **single image** per queue item
- Preview of saved images directly in ComfyUI
- Existing-file handling: `skip`, `overwrite`, or `error`
- Optional output subfolder within `ComfyUI/output`
- Works with the `base_name` string output from **FolderBatch Sync Queue**

## Installation (manual)

1. Download this repository as a ZIP using **Code → Download ZIP**, or clone it.
2. Place the folder containing `__init__.py` and `nodes.py` in `ComfyUI/custom_nodes/ComfyUI-SaveOriginalImage`.
3. Restart ComfyUI.

The node uses Pillow and NumPy, which are normally included in ComfyUI. If either is missing, install it in **ComfyUI's own Python environment**.

## How to use

Find **Save Image Original Name (JPG / PNG)** in the `image/save` category.

| Input | Description |
| --- | --- |
| `images` | Image tensor(s) to save, e.g. `RTXVideoSuperResolution.upscaled_images` |
| `base_name` | Source name, e.g. `FolderBatch Sync Queue.base_name` |
| `subfolder` | Relative folder under `ComfyUI/output` (default: `RTX_Upscaled`) |
| `quality` | JPG quality, 1–100 (default: 95) |
| `on_existing` | `skip`, `overwrite`, or `error` |
| `format` | `JPG` or `PNG` |
| `png_compress_level` | PNG compression 0–9 (default: 6) |

### Example

`Morrigan_001.png` → `RTX_Upscaled/Morrigan_001.jpg` (JPG mode) or `RTX_Upscaled/Morrigan_001.png` (PNG mode).

**Important:** Exact original names are retained when the incoming batch has **one image**. If multiple images arrive in one call, numbered suffixes (`_0001`, `_0002`, etc.) are added to avoid collisions. `base_name` should be a filename, not a path.

### Notes

- JPG does not preserve transparency. For lossless output, use PNG.
- With `on_existing=skip`, existing output files are left untouched and may be shown in the preview.
- Do not run a second image-saving node simultaneously unless you intentionally want duplicate exports.
- This node does not change RTX upscaling or video processing; it only saves images.

## Compatibility


## Issues and contributions

Please use the repository's **Issues** tab to report problems. Include your ComfyUI version, steps to reproduce, and the relevant error message (without private file paths).

## License

MIT. See [LICENSE](LICENSE).
