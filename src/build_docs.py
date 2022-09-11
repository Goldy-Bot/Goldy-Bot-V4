from pathlib import Path
import pdoc

GITHUB_RAW = "https://raw.githubusercontent.com/Goldy-Bot/Goldy-Bot-V4/main"

pdoc.render.configure(logo=f"{GITHUB_RAW}/assets/pfp_1.png", logo_link="https://goldybot.devgoldy.me/GoldyBot.html", footer_text="Copyright (C) 2022 - Dev Goldy", 
template_directory=Path("./docs_template"))

pdoc.pdoc("./GoldyBot", output_directory=Path("../docs/"))