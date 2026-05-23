import json
import re

from openai import OpenAI

from prompts import SYSTEM_PROMPT
from tools import TOOLS


class Agent:

    def __init__(self, client: OpenAI, model: str):
        self.client = client
        self.model = model

    def extract_json(self, text: str):
        """
        Extract JSON from markdown block.
        """

        pattern = r"```json(.*?)```"

        match = re.search(pattern, text, re.DOTALL)

        if not match:
            return None

        json_text = match.group(1).strip()

        try:
            return json.loads(json_text)
        except json.JSONDecodeError:
            return None

    def run(self, question: str):

        messages = [
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": question
            }
        ]

        max_steps = 5

        for step in range(max_steps):

            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0,
                max_tokens=500,
                stop=["Observation:"]
            )

            assistant_message = response.choices[0].message.content

            print("\n========================")
            print(f"STEP {step + 1}")
            print("========================\n")

            print(assistant_message)

            # Check if final answer exists
            if "Final Answer:" in assistant_message:
                print("\nAgent finished successfully.")
                return

            tool_call = self.extract_json(assistant_message)

            if not tool_call:
                print("\nERROR: Could not parse tool JSON")
                return

            action = tool_call.get("action")
            action_input = tool_call.get("action_input", {})

            if action not in TOOLS:
                print(f"\nERROR: Unknown tool '{action}'")
                return

            try:
                tool_function = TOOLS[action]

                tool_result = tool_function(**action_input)

            except Exception as e:
                tool_result = f"Tool execution failed: {str(e)}"

            # Append assistant reasoning + observation
            messages.append({
                "role": "assistant",
                "content": assistant_message + "\nObservation:\n" + tool_result
            })

        print("\nERROR: Max steps reached.")