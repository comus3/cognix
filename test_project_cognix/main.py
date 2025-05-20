from cognix.session import COGNIXSession

def main():
    session = COGNIXSession()

    print("Welcome to COGNIX test chat. Type 'exit' to quit.")
    stream_mode = True

    # Example extra parameters to test
    extra_params = {
        "raw": True,
    }

    print()

    while True:
        user_input = input("#######################\n human input on test app : ")
        if user_input.strip().lower() == "exit":
            print("Exiting...")
            break

        if stream_mode:
            # Pass extra params to chat_stream
            for chunk in session.chat_stream(user_input, **extra_params):
                print(chunk, end="", flush=True)
            print("\n#######################\n")  # New line after stream
        else:
            # Pass extra params to chat
            response = session.chat(user_input, **extra_params)
            print(f"{response}")
            print("\n")  # New line after response

if __name__ == "__main__":
    main()
