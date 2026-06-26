def split_user_name(full_name: str):
    """
    Cleans up user text input and splits it into first and second names.
    """
    # .strip() removes accidental leading/trailing spaces
    # .split(" ", 1) splits only at the very first space found
    parts = full_name.strip().split(" ", 1)
    
    first_name = parts[0]
    
    # If the user didn't enter a second name, default to an empty string
    second_name = parts[1] if len(parts) > 1 else ""
    
    return first_name, second_name
