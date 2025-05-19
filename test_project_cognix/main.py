from cognix.session import COGNIXSession

def main():
    session = COGNIXSession(model="llama3", system_prompt="You are a helpful assistant.")

    print("Welcome to COGNIX test chat. Type 'exit' to quit.\n")

    while True:
        user_input = input("You: ")
        if user_input.strip().lower() == "exit":
            print("Exiting...")
            break

        response = session.chat(user_input)
        print(f"Assistant: {response}\n")

if __name__ == "__main__":
    main()
