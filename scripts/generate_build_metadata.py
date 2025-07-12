from pathlib import Path
import json

metadata = {
    'name': 'KeydropBot',
    'version': '0.1.0'
}
Path('build/windows/build_metadata.json').write_text(json.dumps(metadata, indent=2))
print('Metadata generated')
