from agents import run_agent

print("🌦️ Weather Agent Ready! Ask anything.\n")

while True:
    user_input = input("You: ")
    if user_input.lower() in ["exit", "quit"]:
        break

    answer = run_agent(user_input)
    print(f"\nAgent: {answer}\n")
