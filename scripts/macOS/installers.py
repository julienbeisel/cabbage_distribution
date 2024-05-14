import os

PLUGIN_NAME = "AudioShaper2"
IDENTIFIER = "com.AudioShaper2"
VERSION = "0.1"
DEVELOPER_ID = "replacewithyourdeveloperID"

os.system("sudo chmod u+x Scripts/*")

# Create pkg for VST/VST3/AU
os.system(
    f'pkgbuild --install-location "/Library/Audio/Plug-Ins/VST" --identifier "{IDENTIFIER}vst" --version "{VERSION}" --component "{PLUGIN_NAME}.vst" "{PLUGIN_NAME}_vst.pkg"'
)
os.system(
    f'pkgbuild --install-location "/Library/Audio/Plug-Ins/VST3" --identifier "{IDENTIFIER}vst3" --version "{VERSION}" --component "{PLUGIN_NAME}.vst3" "{PLUGIN_NAME}_vst3.pkg"'
)
os.system(
    f'pkgbuild --install-location "/Library/Audio/Plug-Ins/Components" --identifier "{IDENTIFIER}component" --version "{VERSION}" --component "{PLUGIN_NAME}.component" "{PLUGIN_NAME}_au.pkg"'
)

# Add assets (presets)
os.system(
    f'pkgbuild --root Resources/ --install-location "/tmp/NymanoAudio/" --scripts scripts/macos/install_scripts --identifier "{IDENTIFIER}assets" --version "{VERSION}" "{PLUGIN_NAME}_assets_temp.pkg"'
)

# Set authorizations for the postinstall script
os.system(f'pkgutil --expand "{PLUGIN_NAME}_assets_temp.pkg" {PLUGIN_NAME}_assets_temp')
os.system(f'chmod +x {PLUGIN_NAME}_assets_temp/Scripts/postinstall')
os.system(f'pkgutil --flatten {PLUGIN_NAME}_assets_temp {PLUGIN_NAME}_assets.pkg')

# Synthetize them
os.system(
    f'productbuild --synthesize --package "{PLUGIN_NAME}_au.pkg" --package "{PLUGIN_NAME}_vst.pkg" --package "{PLUGIN_NAME}_vst3.pkg" --package "{PLUGIN_NAME}_assets.pkg" distribution.xml'
)

os.system(
    f'productbuild --distribution distribution.xml --resources Resources "{PLUGIN_NAME}.pkg"'
)

# Sign the installer
os.system(
    f'productsign --sign "Developer ID Installer: {DEVELOPER_ID}" "{PLUGIN_NAME}.pkg" "{PLUGIN_NAME}_installer.pkg"'
)
