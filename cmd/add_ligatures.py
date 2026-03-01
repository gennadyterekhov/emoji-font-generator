import subprocess
import tempfile
import os

from lirbantu.config.config import get_ai_dictionary, get_lirbantu_font_filename
from lirbantu.project import get_project_dir


def add_ligatures_practical(input_font, ligature_dict, output_font):
    """
    Use fonttools with feature file approach
    """

    # Create a feature file for OpenType ligatures
    feature_content = "languagesystem DFLT dflt;\n"
    feature_content += "languagesystem latn dflt;\n\n"
    feature_content += "feature liga {\n"

    for ligature, svg_file in ligature_dict.items():
        # Convert ligature string to feature syntax
        # e.g., "f_i" -> "f i" by ligature
        components = ' '.join(ligature)
        feature_content += f"    sub {components} by {ligature};\n"

    feature_content += "} liga;\n"

    # Write feature file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.fea', delete=False) as f:
        f.write(feature_content)
        feature_file = f.name

    # Use fonttools to add features
    cmd = [
        'fonttools', 'feaLib', '-o', output_font,
        feature_file, input_font
    ]

    try:
        subprocess.run(cmd, check=True)
        print(f"Font saved to {output_font}")
    except subprocess.CalledProcessError as e:
        print(f"Error adding features: {e}")
    finally:
        os.unlink(feature_file)


def get_ligatures_map():
    rootdir = get_project_dir()
    dct = get_ai_dictionary()
    liga = {}
    for wf_info in dct:
        liga[wf_info["lirbantu"]] = f'{rootdir}/emojis/combined/{wf_info["wordform"]}.svg'
    return liga

# Usage
ligatures = {
    "fi": "path/to/fi.svg",
    "fl": "path/to/fl.svg",
    "ffi": "path/to/ffi.svg",
    # ... 383 more ligatures
}

rootdir = get_project_dir()

ligatures=get_ligatures_map()
output_filename=f'{rootdir}/output/nu_lirbantu_w_ligatures.ttf'
add_ligatures_practical(get_lirbantu_font_filename(), ligatures, output_filename)
