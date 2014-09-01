import cubes

workspace = cubes.Workspace(config='etc/slicer.ini')
c = workspace.cube('history')
b = workspace.browser()

cuts = [
    # cubes.SetCut('history', 'command_date')
    PointCut("history", ["sk"])
    PointCut("date", [2010, 6], [2012, 6]),
]
cell = Cell(cube, cuts)
result = browser.aggregate(cell)
