from lib2to3.pgen2.token import NEWLINE
import math
import random
from itertools import product
from re import A
from time import sleep


GRID_START = 0
GRID_STOP = 2


class Room:
    def __init__(self) -> None:
        self.dirty = 0

    def clean(self):
        self.dirty = 0


class Grid:
    def __init__(self, dirty_rooms) -> None:
        self.grid = [[], [], []]
        self.dirty_room_count = dirty_rooms
        self.fill_grid()

    def fill_grid(self):
        for column in self.grid:
            while len(column) < GRID_STOP + 1:
                column.append(Room())

        points = [0, 1, 2]
        coordinates = list(product(points, points))
        dirty_coordinates = random.sample(range(0, 9), self.dirty_room_count)

        for coordinate in dirty_coordinates:
            x, y = coordinates[coordinate][0], coordinates[coordinate][1]
            self.grid[x][y].dirty = 1

    def print_grid(self):
        for row in self.grid:
            for column in row:
                print(column.dirty, end=" ")
            print("\n")


class Robot:
    def __init__(self) -> None:
        self.current_room_x = random.randint(0, 2)
        self.current_room_y = random.randint(0, 2)
        self.total_moves = 0

    def get_room(self, grid):
        return grid.grid[self.current_room_x][self.current_room_y]

    def choose_action(self, grid):
        room = self.get_room(grid)
        if room.dirty:
            room.clean()
            grid.dirty_room_count -= 1

        else:
            self.move()
        self.total_moves += 1

    def random_action(self, grid):
        action = random.randint(0, 1)
        room = self.get_room(grid)
        if action == 1:
            self.random_move()

        elif room.dirty:
            room.clean()
            grid.dirty_room_count -= 1

        self.total_moves += 1

    def choose_action_murphy(self, grid):
        room = self.get_room(grid)
        fail = random.randint(0, 4)
        malfunction = random.randint(0, 9)

        if room.dirty:
            if malfunction:
                self.move()
            elif not fail:
                room.clean()
                grid.dirty_room_count -= 1
        else:
            if malfunction:
               if fail:
                   room.dirty = 1
                   grid.dirty_room_count += 1 
            else:
                self.move()

        self.total_moves += 1

    def random_action_murphy(self, grid):
        room = self.get_room(grid)
        action = random.randint(0, 1)
        fail = random.randint(0, 4)
        malfunction = random.randint(0, 9)
        if action == 1:
            if room.dirty:
                if malfunction == 0:
                    pass
                elif not fail:
                    room.clean()
                    grid.dirty_room_count -= 1
            else:
                if malfunction:
                    if fail:
                        room.dirty = 1
                        grid.dirty_room_count += 1
        else:
            self.random_move()

        self.total_moves += 1

    def move(self):
        if self.current_room_y == 0:
            if (self.current_room_x - 1) >= 0:
                self.go_left()
            else:
                self.go_down()

        elif self.current_room_y == 1:
            if self.current_room_x == 2:
                switch = random.randint(0, 1)
                if switch:
                    self.go_left()
                else:
                    self.go_up()
            else:
                self.go_down()
        else:
            if (self.current_room_x + 1) <= GRID_STOP:
                self.go_right()
            else:
                self.go_up()

    def random_move(self):
        switch = random.randint(0, 1)
        if self.current_room_y == 0:
            if (self.current_room_x - 1) >= 0:
                if switch:
                    self.go_left()
                else:
                    self.go_down()
            else:
                self.go_down()

        elif self.current_room_y == 1:
            if self.current_room_x == 2:
                if switch:
                    self.go_left()
                else:
                    switch = random.randint(0, 1)
                    if switch:
                        self.go_up()
                    else:
                        self.go_down()
            else:
                self.go_down()
        else:
            if (self.current_room_x + 1) <= GRID_STOP:
                if switch:
                    self.go_right()
                else:
                    self.go_up()
            else:
                self.go_up()

    def go_up(self):
        self.current_room_y -= 1

    def go_down(self):
        self.current_room_y += 1

    def go_right(self):
        self.current_room_x += 1

    def go_left(self):
        self.current_room_x -= 1

    # def dirt_detected(room):
    #     return room.dirty

    # def clean_room(self):
    #     return [self.current_room_x, self.current_room_y]

    # def current_room(self):
    #     return [self.current_room_x, self.current_room_y]


# class Simulation:
#     def __init__(self) -> None:

pile_counts = [1, 3, 5]
trial_count = 1000
# grid = Grid()
# bot = Robot()
# rando_bot = Robot()
# murphy_bot = Robot()
# murphy_rando_bot = Robot()

# dirty_rooms = grid.dirty_room_count
# grid.print_grid()
# print("-------------")


# while grid.dirty_room_count:
#     bot.choose_action(grid)
# grid.print_grid()
# print("-------------")
# sleep(.1)
flex_bot_stats = {1: 0, 3: 0, 5: 0}
flex_bot_m_stats = {1: 0, 3: 0, 5: 0}
rando_bot_stats = {1: 0, 3: 0, 5: 0}
rando_bot_m_stats = {1: 0, 3: 0, 5: 0}

MAX_MOVES = 3000 

for count in pile_counts:
    trial_counter = trial_count
    while trial_counter:
        fb_grid = Grid(count)
        fbm_grid = Grid(count)
        rb_grid = Grid(count)
        rbm_grid = Grid(count)

        flex_bot = Robot()
        flex_bot_m = Robot()
        rando_bot = Robot()
        rando_bot_m = Robot()

        while fb_grid.dirty_room_count and not flex_bot.total_moves >= MAX_MOVES:
            flex_bot.choose_action(fb_grid)
            # print(
            #     f"room count: {fb_grid.dirty_room_count}, trial: {trial_counter}, pile_count: {count}, total actions: {flex_bot.total_moves}"
            # )

        flex_bot_stats[count] += flex_bot.total_moves

        while fbm_grid.dirty_room_count and not flex_bot_m.total_moves >= MAX_MOVES:
            flex_bot_m.choose_action_murphy(fbm_grid)
        #     # print(
        #     #     f"room count: {fbm_grid.dirty_room_count}, trial: {trial_counter}, pile_count: {count}, total actions: {flex_bot_m.total_moves}"
        #     # )

        flex_bot_m_stats[count] += flex_bot_m.total_moves

        while rb_grid.dirty_room_count and not rando_bot.total_moves >= MAX_MOVES:
            rando_bot.random_action(rb_grid)
            # print(
            #     f"room count: {rb_grid.dirty_room_count}, trial: {trial_counter}, pile_count: {count}, total actions: {rando_bot.total_moves}"
            # )

        rando_bot_stats[count] += rando_bot.total_moves

        while rbm_grid.dirty_room_count and not rando_bot_m.total_moves >= MAX_MOVES:
            rando_bot_m.random_action_murphy(rbm_grid)
        #     # print(
        #     #     f"room count: {rbm_grid.dirty_room_count}, trial: {trial_counter}, pile_count: {count}, total actions: {flex_bot.total_moves}"
        #     # )

        rando_bot_m_stats[count] += rando_bot_m.total_moves

        trial_counter -= 1

for key in flex_bot_stats:
    flex_bot_stats[key] = flex_bot_stats[key] / trial_count
    flex_bot_m_stats[key] = flex_bot_m_stats[key] / trial_count
    rando_bot_stats[key] = rando_bot_stats[key] / trial_count
    rando_bot_m_stats[key] = rando_bot_m_stats[key] / trial_count

print("fb bot: ", flex_bot_stats)
print("fbm bot: ", flex_bot_m_stats)
print("rb bot: ", rando_bot_stats)
print("rbm bot: ", rando_bot_m_stats)
