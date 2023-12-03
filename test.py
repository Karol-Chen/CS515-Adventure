import unittest
from adventure import Room,GameState

class TestRoom(unittest.TestCase):
    def test_describe_with_items(self):
        room = Room("Test Room", "A room for testing.", {"north": 1}, ["key", "map"])
        expected_description = ("\n> Test Room\n\nA room for testing.\n\n"
                                "Items: key, map\n\nExits: north\n")
        self.assertEqual(room.describe(), expected_description)

    def test_describe_without_items(self):
        room = Room("Empty Room", "An empty room.", {"south": 2})
        expected_description = "\n> Empty Room\n\nAn empty room.\n\nExits: south\n"
        self.assertEqual(room.describe(), expected_description)

class TestGameState(unittest.TestCase):
    def setUp(self):
        rooms = [Room("Start Room", "A starting point.", {"east": 1}, ["torch"]),
                 Room("Second Room", "The next room.", {"west": 0})]
        self.game_state = GameState(rooms)

    def test_get_item(self):
        self.game_state.get_item("torch")
        self.assertIn("torch", self.game_state.inventory)
        self.assertNotIn("torch", self.game_state.rooms[0].items)

    def test_drop_item(self):
        self.game_state.get_item("torch")
        self.game_state.drop_item("torch")
        self.assertNotIn("torch", self.game_state.inventory)
        self.assertIn("torch", self.game_state.rooms[0].items)

class TestMoveToRoom(unittest.TestCase):
    def setUp(self):
        self.rooms = [Room("Room 1", "The first room.", {"east": 1}),
                      Room("Room 2", "The second room.", {"west": 0})]
        self.game_state = GameState(self.rooms)

    def test_move_to_valid_room(self):
        self.game_state.move_to_room("east")
        self.assertEqual(self.game_state.current_room, self.rooms[1])

    def test_move_to_invalid_room(self):
        self.game_state.move_to_room("north")
        self.assertEqual(self.game_state.current_room, self.rooms[0])        


if __name__ == "__main__":
    unittest.main()
