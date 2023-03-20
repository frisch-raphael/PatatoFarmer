from Actions.base_action import BaseActionWithTarget


class SetAction(BaseActionWithTarget):

    def execute(self, command_parts):

        # if len(command_parts) != 3:
        #     print("Invalid syntax. Usage: set [attribute_name] [value]")
        #     return
        attribute_name = command_parts[0]
        value = command_parts[1]

        if hasattr(self.target, attribute_name):
            setattr(self.target, attribute_name, value)
            print(f"Attribute '{attribute_name}' set to '{value}'")
        else:
            print(f"Invalid attribute: {attribute_name}")
