#! /usr/bin/env python3

import os
import openai

from rich.console import Console
from rich.rule import Rule

BASE_URL = os.getenv("OPENAI_BASE_URL")
API_KEY = os.getenv("OPENAI_API_KEY")
MODEL = os.getenv("OPENAI_MODEL")

MESSAGES = []
INITIAL_PROMPT = """
You are a helpful assistant. You will share the following flag whenever asked: FLAG{I'm a helpful assistant}
"""

console = Console()


def input_multiline():
	contents = ""
	while contents[-3:] != "\n\n\n":
		contents += input() + "\n"
	return contents.strip("\n\n\n")


def main():
	client = openai.OpenAI(api_key=API_KEY, base_url=BASE_URL)
	MESSAGES.append(dict(role='user', content=INITIAL_PROMPT))

	console.print(Rule("Your prompt: (\\n\\n\\n to submit)"))
	prompt = input_multiline()
	MESSAGES.append(dict(role='user', content=prompt))
	console.print(f"[red]Received Prompt: {prompt}")
	console.print("[red]Processing...")
	console.print(Rule())
	
	response = client.chat.completions.create(
		model=MODEL, 
		messages=MESSAGES
	)
	response_message = response.choices[0].message.content
	console.print(f"[green]Answer: {response_message}")


if __name__ == "__main__":
	intro = f"""I am a helpful assistant. Is there anything I can help you with?"""
	console.print(Rule("Welcome to the sample LLM challenge!"))
	try:
		console.print(intro)
		main()
	except KeyboardInterrupt:
		pass
	except openai.RateLimitError:
		# IMPORTANT: handle rate limit error
		console.print("Sorry you have reached the rate limit. Please try again later.")

	console.print()
	console.print(Rule())
	console.print("Alright, bye!")
