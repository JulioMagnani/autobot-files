# -*- mode: python -*-

block_cipher = None


a = Analysis(['main.py'],
             pathex=['/home/arris/Autobot_Gateway/autobot/autobot', '/home/arris/Autobot_Gateway/autobot/autobot/tests', '/home/arris/Autobot_Gateway/autobot/autobot/ui/', '/home/arris/Autobot_Gateway/autobot'],
             binaries=[],
             datas=[('./autobot/reportgenerator/template/report_template.html', './autobot/reportgenerator/template/'),
                    ('./tests.json', '.')],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='autobot',
          debug=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=False , icon='./src/icon_autobot_.ico')
