from pathlib import Path

import folder_paths
import numpy as np
from PIL import Image


class SaveOriginalJPG:
    @classmethod
    def INPUT_TYPES(cls):
        return {"required": {
            "images": ("IMAGE",),
            "base_name": ("STRING", {"forceInput": True}),
            "subfolder": ("STRING", {"default": "RTX_Upscaled"}),
            "quality": ("INT", {"default": 95, "min": 1, "max": 100}),
            "on_existing": (["skip", "overwrite", "error"], {"default": "skip"}),
            "format": (["JPG", "PNG"], {"default": "JPG"}),
            "png_compress_level": ("INT", {"default": 6, "min": 0, "max": 9}),
        }}

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("saved_paths",)
    FUNCTION = "save"
    OUTPUT_NODE = True
    CATEGORY = "image/save"

    def save(self, images, base_name, subfolder, quality, on_existing,
             format="JPG", png_compress_level=6):
        root = Path(folder_paths.get_output_directory()).resolve()
        relative = Path(subfolder.strip().replace("\\", "/"))
        if relative.is_absolute() or ".." in relative.parts or ":" in subfolder:
            raise ValueError("subfolder must be relative to ComfyUI/output")
        dest = (root / relative).resolve()
        if not dest.is_relative_to(root):
            raise ValueError("Output folder must stay inside ComfyUI/output")
        dest.mkdir(parents=True, exist_ok=True)

        original = str(base_name).strip()
        if not original or original in (".", "..") or "/" in original or "\\" in original or ":" in original:
            raise ValueError("Invalid base_name")
        stem = Path(original).stem
        if not stem or stem in (".", ".."):
            raise ValueError("Invalid base_name")

        fmt = format.upper()
        if fmt not in ("JPG", "PNG"):
            raise ValueError("format must be JPG or PNG")
        extension = ".jpg" if fmt == "JPG" else ".png"
        saved = []
        previews = []
        for index, tensor in enumerate(images):
            name = stem if len(images) == 1 else f"{stem}_{index + 1:04d}"
            target = dest / f"{name}{extension}"
            if target.exists():
                if on_existing == "skip":
                    saved.append(f"SKIPPED: {target}")
                    previews.append({"filename": target.name, "subfolder": relative.as_posix() if str(relative) != "." else "", "type": "output"})
                    continue
                if on_existing == "error":
                    raise FileExistsError(f"File already exists: {target}")
            array = (tensor.detach().cpu().clamp(0, 1).numpy() * 255).round().astype(np.uint8)
            image = Image.fromarray(array)
            if fmt == "JPG":
                if image.mode != "RGB":
                    image = image.convert("RGB")
                image.save(target, format="JPEG", quality=quality, optimize=True)
            else:
                image.save(target, format="PNG", compress_level=png_compress_level)
            saved.append(str(target))
            previews.append({"filename": target.name, "subfolder": relative.as_posix() if str(relative) != "." else "", "type": "output"})
        return {"ui": {"images": previews}, "result": ("\n".join(saved),)}


# Keep the original class ID so existing workflows can resolve this node.
NODE_CLASS_MAPPINGS = {"SaveOriginalJPG": SaveOriginalJPG}
NODE_DISPLAY_NAME_MAPPINGS = {"SaveOriginalJPG": "Save Image Original Name (JPG / PNG)"}
