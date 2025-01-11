# Module to manage shared global states across different modules.
#
# This module defines a class for managing global states and creates a single shared instance
# of this class to allow consistent state sharing across modules.
#
# Classes:
# - GlobalState: Encapsulates shared states such as error flags.
#
# Global Variables:
# - global_state: A singleton instance of the GlobalState class, shared across all modules.
#
# Logic:
# 1. The `GlobalState` class provides a simple structure for storing global states.
# 2. An instance of `GlobalState` is created at the module level to act as a shared global state manager.
# 3. Other modules can import and interact with the `global_state` instance to check or modify shared states.
#
# Notes:
# - This design centralizes the management of global states, reducing duplication and ensuring consistency.
# - The `has_errors` flag is initialized as `False` and can be updated based on application logic.
#
# Example Usage:
# # Accessing the shared global state
# if global_state.has_errors:
#     print("An error occurred in the application.")
class GlobalState:
    def __init__(self):
        self.has_errors = False

# Create a unique instance of GlobalState to be shared across modules.
global_state = GlobalState()