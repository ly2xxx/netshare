"""
File utility functions for managing background resources
Handles background file discovery from keep/ and gif/ folders
"""

from pathlib import Path
from typing import List, Tuple, Dict


def get_available_backgrounds() -> List[str]:
    """
    Get list of available background files from keep/ folder

    Returns:
        Sorted list of background filenames
    """
    keep_path = Path(__file__).parent.parent / "keep"
    if not keep_path.exists():
        return []

    # Support images and videos
    extensions = {'.png', '.jpg', '.jpeg', '.gif', '.mp4', '.webm'}
    backgrounds = []
    for f in keep_path.iterdir():
        if f.suffix.lower() in extensions:
            backgrounds.append(f.name)
    return sorted(backgrounds)


def get_available_gifs() -> List[str]:
    """
    Get list of available background files (GIF, JPG) from gif/ folder

    Returns:
        Sorted list of GIF and JPG filenames
    """
    gif_path = Path(__file__).parent.parent / "gif"
    if not gif_path.exists():
        return []

    gifs = []
    for f in gif_path.iterdir():
        if f.suffix.lower() in ['.gif', '.jpg', '.jpeg']:
            gifs.append(f.name)
    return sorted(gifs)


def get_all_available_backgrounds() -> Tuple[List[str], Dict[str, str]]:
    """
    Get combined list of backgrounds from both keep/ and gif/ folders

    Returns:
        Tuple of (sorted list of all background filenames, dict mapping filename to folder)
        The dict values are 'keep' or 'gif' indicating source folder
    """
    backgrounds_from_keep = get_available_backgrounds()
    backgrounds_from_gif = get_available_gifs()

    # Create a dictionary to track folder source for each file
    # This helps with file resolution later
    background_map = {}
    for bg in backgrounds_from_keep:
        background_map[bg] = 'keep'
    for bg in backgrounds_from_gif:
        if bg not in background_map:  # Avoid duplicates, keep/ takes priority
            background_map[bg] = 'gif'

    return sorted(background_map.keys()), background_map
