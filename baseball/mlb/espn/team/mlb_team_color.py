def get_team_color(team_abbreviation):
    if team_abbreviation == 'CHC':
        colors = [
            "#0004FF",  # Blue
            "#FFFFFF",  # White
            "#FF0000",  # Red
        ]

    elif team_abbreviation == 'NYY':
        colors = [
            "#FFFFFF",  # White
            "#000000",  # Black
        ]
    elif team_abbreviation == 'HOU':
        colors = [
            "#0000FF",  # Blue
            "#FFa500",  # Orange
        ]
    elif team_abbreviation == 'SEA':
        colors = [
            "#005C5C",  # Dark Teal
            "#00FF00",  # Bright Green
        ]

    else:
        colors = [
            "#FFFFFF",  # White
            "#FF0000",  # Red
        ]

    return colors