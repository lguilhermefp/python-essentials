from enum import Enum

class MapSite:
    def Enter(self):
        raise NotImplementedError('Abstract Base Class Method')

class Direction(Enum):
    North = 0
    East  = 1
    South = 2
    West  = 3

class Room(MapSite):
    def __init__(self, roomNo):
        self._sides = [MapSite] * 4
        self._roomNumber = int(roomNo)

    def GetSide(self, Direction):
        return self._sides[Direction]

    def SetSide(self, Direction, MapSite):
        self._sides[Direction] = MapSite

    def Enter(self):
        print('     You\'ve entered the room: ', str(self._roomNumber))

class Wall(MapSite):
    def Enter(self):
        print('     you just ran into a wall!')

class Door(MapSite):
    def __init__(self, Room1=None, Room2=None):
        self._room1 = Room1
        self._room2 = Room2
        self._isOpen = False

    def OtherSideFrom(self, Room):
        print('\tDoor obj: This door is a side of Room: {}'.format(Room._roomNumber))
        if 1 == Room._roomNumber:
            other_room = self._room2
        else:
            other_room = self._room1
        return other_room

    def Enter(self):
        if self._isOpen: print('    * You\'ve passes through this door')
        else: print('   * This door needs to be opened before you can pass through')

class Maze:
    def __init__(self):
        self._rooms = {}

    def AddRoom(self, room):
        self._rooms[room._roomNumber] = room

    def RoomNo(self, room_number):
        return self._rooms[room_number]

class MazeGame:
    def CreateMaze(self):
        aMaze = Maze()
        r1 = Room(1)
        r2 = Room(2)
        theDoor = Door(r1, r2)

        aMaze.AddRoom(r1)
        aMaze.AddRoom(r2)

        r1.SetSide(Direction.North.value, Wall())
        r1.SetSide(Direction.East.value, theDoor)
        r1.SetSide(Direction.South.value, Wall())
        r1.SetSide(Direction.West.value, Wall())

        r2.SetSide(Direction(0).value, Wall())
        r2.SetSide(Direction(1).value, Wall())
        r2.SetSide(Direction(2).value, Wall())
        r2.SetSide(Direction(3).value, theDoor)

        return aMaze

if __name__ == '__main__':
    # map_site_inst = MapSite()
    # map_site_inst.Enter()

    print('*' * 21)
    print('*** The maze game ***')
    print('*' * 21)

    maze_obj = MazeGame().CreateMaze()

    maze_rooms = []
    for room_number in range(5):
        try:
            room = maze_obj.RoomNo(room_number)
            print('\n^^^ Maze has room: {}'.format(room_number, room))
            print('     Entering the room')
            room.Enter()
            maze_rooms.append(room)
            for idx in range(4):
                side = room.GetSide(idx)
                side_str = str(side.__class__).replace("<class '__main__.", "").replace("'>", "")
                print('     Room: {}, {:<15s}, Type: {}'.format(room_number, Direction(idx), side_str))
                print('     Trying to enter: ', Direction(idx))
                side.Enter()
                if 'Door' in side_str:
                    door = side
                    if not door._isOpen:
                        print('     * Opening the door!')
                        door.isOpen = True
                        door.Enter()
                    print('\t', door)
                    other_room = door.OtherSideFrom(room)
                    print('\tOn the other side of the door is room: {})\n'.format(other_room._roomNumber))

        except KeyError:
            print('No room:', room_number)

    num_of_rooms = len(maze_rooms)
    print('\There are {} rooms in the Maze'.format(num_of_rooms))

    print('Both doors are the same object and they are on the East and West side of the two rooms')
