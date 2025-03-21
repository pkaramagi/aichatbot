import nltk


class NLTKResourceManager:
    def __init__(self):
        self.resource_name = self._determine_resource()

    def _determine_resource(self)->str:
        nltk_version = tuple(map(int, nltk.__version__.split('.')))
        return 'punkt_tab' if nltk_version >= (3,8,2) else 'punkt'
    
    def resource_exists(self) -> bool:
        try:
            nltk.data.find(f"tokenizers/{self.resource_name}")
            return True
        except LookupError:
            return False
        
    def download_resource(self):
        if not self.resource_exists():
            print(f"Downloading NLTK Resource: {self.resource_name}.....")
        else:
            print(f" NLTK Resource: {self.resource_name} is already installed")

    
