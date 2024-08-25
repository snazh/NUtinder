from src.interface.menu_texts import menu_options

def format_profile(profile: dict) -> str:
    """
    Format the user's profile in a beautiful way.

    Args:
        profile (dict): A dictionary containing user profile data.

    Returns:
        str: A formatted string representing the user's profile.
    """
    name = profile.get("name", "Unknown")
    nu_id = profile.get("nu_id", "N/A")
    gender = profile["gender"].value
    soulmate_gender = profile["soulmate_gender"].value
    course = profile.get("course", "N/A")
    description = profile.get("description", "No description provided")

    profile_text = (
        f"*👤 Profile:*\n"
        f"*Name:* {name}\n"
        f"*NU ID:* {nu_id}\n"
        f"*Gender:* {gender}\n"
        f"*Looking for:* {soulmate_gender}\n"
        f"*Course:* {course}\n"
        f"*Description:* {description}\n"
    )

    return profile_text


def format_anketa(profile: dict) -> str:
    name = profile.get("name", "Unknown")
    course = profile.get("course", "N/A")
    description = profile.get("description", "No description provided")

    profile_text = (

        f"{name}, {course}\n"
        f"{description}\n"
    )

    return profile_text


print(isinstance(menu_options.actions, str))