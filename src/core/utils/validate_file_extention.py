from typing import List

def validate_file_type(content_type:str, midea_type:List[str], subtype: List[str]) -> bool:
    if content_type.split("/")[0] not in midea_type:
        return False
    
    if content_type.split("/")[1] not in subtype:
        return False

    return True