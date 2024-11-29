from pathlib import Path
import json

class ConfigManager:
    config_path = Path('./config.json')

    class WriteConfig:
        def __init__(self, config_path: Path = None) -> None:
            self.config_path = config_path if config_path else ConfigManager.config_path

            self.default_config_dict = {
                'capture': {
                    'left': 0,
                    'top': 0,
                    'right': 0,
                    'bottom': 0,
                    'image_path': str(Path('./capture.png'))
                },
                'ocr': {
                    'language': 'khm',
                    'tesseract_path': str(Path('C:/Program Files/Tesseract-OCR/tesseract.exe'))
                }
            }

        def default(self) -> None:
            with open(self.config_path, 'w') as out_file:
                json.dump(self.default_config_dict, out_file)

        def capture(self, 
                    left: int = 0, 
                    top: int = 0, 
                    right: int = 0, 
                    bottom: int = 0, 
                    image_path: Path = Path('./capture.png')
                    ) -> None:
            try:
                with open(self.config_path, 'r') as file:
                    data = json.load(file)
                    data['capture']['left'] = left
                    data['capture']['top'] = top
                    data['capture']['right'] = right
                    data['capture']['bottom'] = bottom
                    data['capture']['image_path'] = str(image_path)
                
                with open(self.config_path, 'w') as out_file:
                    json.dump(data, out_file)
            except:
                self.default()

        def ocr(self, 
                language: str = 'khm', 
                tesseract_path: Path = Path('C:/Program Files/Tesseract-OCR/tesseract.exe')
                ) -> None:
            try:
                with open(self.config_path, 'r') as file:
                    data = json.load(file)
                    data['ocr']['language'] = language
                    data['ocr']['tesseract_path'] = str(tesseract_path)
                
                with open(self.config_path, 'w') as out_file:
                    json.dump(data, out_file)
            except:
                self.default()
