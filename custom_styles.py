from questionary import Style

question_style = Style([
    ("question", "fg:yellow bold"),
    ("pointer", "fg:blue"),
    ("highlighted", "fg:aqua"),
    ("answer", "fg:aqua"),
])

autocomplete_style = Style([
    ("question", "fg:yellow bold"),
    ("pointer", "fg:blue"),
    ("highlighted", "fg:aqua"),
    ("answer", "fg:aqua bg:black"),
])