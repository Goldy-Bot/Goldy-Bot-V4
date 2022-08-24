from pathlib import Path
import pdoc

pdoc.render.configure(logo="../assets/pfp_1.png", logo_link="https://github.com/Goldy-Bot/Goldy-Bot-V4", footer_text="Copyright (C) 2022 - Dev Goldy")

pdoc.pdoc("./GoldyBot", output_directory=Path("../docs/"))