import sys
import glob
import os

developer_id = "replacewithyourdeveloperid"
apple_id = "replacewithyourappleid"
app_pass = "replacewithyourapppass"

extensions = ["vst", "vst3", "component"]

plugin_name = "AudioShaper2"
plugin_path = ""
plugin_name_subfolder = "AudioShaper2"

for extension in extensions:
    plugin_path = plugin_name+"."+extension

    if extension == "component":
        # Please note this line will change after the AU export bug is be fixed
        plugin_name_subfolder = "CabbagePluginEffect"

    files_a = glob.glob(plugin_path + "/**/*.a", recursive=True)
    files_dylib = glob.glob(plugin_path + "/**/*.dylib", recursive=True)
    files_jnilib = glob.glob(plugin_path + "/**/*.jnilib", recursive=True)
    

    for file_ in files_a + files_dylib +files_jnilib + [f"{plugin_name}.{extension}/Contents/Resources/CsoundLib64.framework/Versions/6.0/CsoundLib64"]:
        newcmd = f'codesign -s "{developer_id}" "{file_}" --timestamp --deep --force '
        os.system(f"sudo {newcmd}")

    os.system(
        f'sudo codesign -s "{developer_id}" "{plugin_name}.{extension}/Contents/MacOS/{plugin_name_subfolder}" --timestamp --deep --force'
    )
