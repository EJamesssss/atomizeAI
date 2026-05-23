def detect_file_type(file) -> str:
    """
    Detect the type of the uploaded file based on its MIME type.
    
    Args:
        file: An object representing the uploaded file, expected to have a 'type' attribute.
        
    Returns:
        A string indicating the type of the file: 'image', 'pdf', or 'unknown'.
    """
    if not hasattr(file, 'type'):
        return 'unknown'
    
    mime_type = file.type
    if mime_type.startswith('image/'):
        return 'image'
    elif mime_type == 'application/pdf':
        return 'pdf'
    else:
        return 'unknown'