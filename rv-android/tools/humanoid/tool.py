import constants
import utils
from app import App
from commands.command import Command

from ..tool_spec import AbstractTool


# TODO run humanoid container before using this tool
# docker run -d -p 50405:50405 phtcosta/humanoid:1.0

class ToolSpec(AbstractTool):
    def __init__(self):
        super(ToolSpec, self).__init__("humanoid", """Humanoid explores Android apps like human. 
                It uses deep learning techniques to borrow experiences from app usage traces generated by human. 
                Currently Humanoid works with DroidBot. When DroidBot explores an Android app in model-based policy, 
                it will generate several possible input events according to current UI state. 
                Humanoid than sort the events such that events that will be performed by human most likely will be fired first.
                (https://github.com/yzygitzh/Humanoid)""", "com.android.commands.humanoid")

    def execute_tool_specific_logic(self, app: App, timeout: int, log_file: str):
        humanoid_url = utils.get_env_or_default(constants.ENV_HUMANOID_URL, "127.0.0.1:50405")
        with open(log_file, "wb") as trace:
            exec_cmd = Command("droidbot", [
                "-d",
                "emulator-5554",
                "-a",
                app.path,
                "-humanoid",
                humanoid_url,
                "-policy",
                "dfs_greedy",
                "-is_emulator",
            ], timeout)
            exec_cmd.invoke(stdout=trace)
