import inspect
import logging
from threading import Lock
from time import sleep

from src.model.demonstrator_mirobot import RoutineNotFoundException

allowed_routines = ["put_from_conveyor_belt_output", "store_item", "put_from_store"]


class MockDemonstratorMirobot:
    """Does not actually run the routines, just tells if the real Demonstrator would have started them."""

    def __init__(self, _):
        self._logger = logging.getLogger(__name__)
        self.mutex = Lock()
        self.action_queue = 0
        self.sanity = 0
        self.stored_items = 42

    def put_from_conveyor_belt_output(self):
        print(f"ENTERING {inspect.stack()[0][3]}")
        self.sanity += 1
        if self.sanity > 1:
            raise RuntimeError()
        sleep(4)
        self.sanity -= 1
        print(f"EXITING {inspect.stack()[0][3]}")

    def store_item(self):
        print(f"ENTERING {inspect.stack()[0][3]}")
        self.sanity += 1
        if self.sanity > 1:
            raise RuntimeError()
        sleep(4)
        self.sanity -= 1
        print(f"EXITING {inspect.stack()[0][3]}")

    def put_from_store(self):
        print(f"ENTERING {inspect.stack()[0][3]}")
        self.sanity += 1
        if self.sanity > 1:
            raise RuntimeError()
        sleep(4)
        self.sanity -= 1
        print(f"EXITING {inspect.stack()[0][3]}")

    def execute_routine(self, routine_name: str):
        """Run a routine if it exists.
        Only one routine is allowed at a time.
        The robot always returns to the zero location at the end of a routine.

        Args:
            routine_name (str): Name of the routine to be executed

        Raises:
            RoutineNotFoundError: Routine with the given name not found
        """
        if routine_name not in allowed_routines:
            print(routine_name, "not in", allowed_routines)
            raise RoutineNotFoundException()

        self.action_queue += 1
        print(f"Actions in queue: {self.action_queue}")
        # Mutex to ensure no concurrent moves being made
        with self.mutex:
            getattr(self, routine_name)()

        self.action_queue -= 1
