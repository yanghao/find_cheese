import sys

UP = 0
LEFT = 1
RIGHT = 2
DOWN = 3

DIR_NAME_MAP = {
    UP: "UP",
    LEFT: "LEFT",
    RIGHT: "RIGHT",
    DOWN: "DOWN",
}

DIR_LIST = [UP, DOWN, LEFT, RIGHT]

class a_map:
    def __init__(self, name):
        self._map = []
        with open(name) as fd:
            lines = fd.readlines()
        # arbitary shapes are possible
        lines = [line.strip() for line in lines]
        self._map = [list(line) for line in lines]
        self._mouse, self._cheese = self._scan_for_mouse_and_cheese()
        self._current = list(self._mouse)
        print("mouse @: %s, cheese @: %s" % (str(self._mouse), str(self._cheese)))

    def _scan_for_mouse_and_cheese(self):
        mouse = None
        cheese = []
        for line_idx, line in enumerate(self._map):
            for col_idx, c in enumerate(line):
                if c == '@':
                    cheese.append((line_idx, col_idx))
                if c == '<':
                    if mouse:
                        raise Exception("more than one mouse found")
                    else:
                        mouse = (line_idx, col_idx)
        return (mouse, cheese)

    def found(self, xx, yy):
        x = self._current[0] + xx
        y = self._current[1] + yy
        if (x,y) in self._cheese:
            return True
        else:
            return False

    def _valid(self, point):
        x = point[0]
        y = point[1]
        if (x < 0) or (y < 0):
            return False
        if x >= len(self._map):
            return False
        if y >= len(self._map[x]):
            return False
        if self._map[x][y] == '#':
            return False
        return True

    def move(self, xx, yy, d):
        x = self._current[0] + xx
        y = self._current[1] + yy
        if d == UP:
            x -= 1
        elif d == DOWN:
            x += 1
        elif d == LEFT:
            y -= 1
        elif d == RIGHT:
            y += 1
        else:
            raise Exception("invalid direction: %d" % d)
        if self._valid([x,y]):
            print("Moving to: %d, %d" % (x, y))
            return True
        else:
            return False
            
class cheese_finder:
    def __init__(self, a_map):
        self.m = a_map
        self.history = [(0,0)]

    def _new_xy(self, x, y, d):
        if d == UP:
            return (x-1, y)
        if d == DOWN:
            return (x+1, y)
        if d == LEFT:
            return (x, y-1)
        if d == RIGHT:
            return (x, y+1)
        raise Exception("wrong direction: %d" % d)

    def find_cheese(self, x, y):
        if self.m.found(x, y):
            xx = self.m._current[0] + x
            yy = self.m._current[1] + y
            print("found cheese at: %s" % str((xx, yy)))
            sys.exit(0)
            return True
        else:
            for d in DIR_LIST:
                r = self.m.move(x, y, d)
                print("move from (%d, %d) to dir %s: %s" % (x, y, DIR_NAME_MAP[d], r))
                new_x, new_y = self._new_xy(x, y, d)
                if (new_x, new_y) in self.history:
                    continue
                else:
                    self.history.append((new_x, new_y))
                if r: # successful
                    self.find_cheese(new_x, new_y)
                else:
                    continue
            return False

if __name__ == '__main__':
    m = a_map(sys.argv[1])
    f = cheese_finder(m)
    f.find_cheese(0, 0)
