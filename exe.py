import cx_Freeze

executables = [cx_Freeze.Executable("quietgame.py")]

cx_Freeze.setup(name = "the quiet game", options={"build_exe": {"packages":["pygame"], "include_files":["ball.png", "marker.png", "1.png", "2.png", "3.png", "ComicSansMS3.ttf"]}}, executables = executables )
