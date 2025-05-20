from cognix.session import COGNIXSession
from colorama import Fore, Style
def main():
    session = COGNIXSession()

    print("Welcome to COGNIX test chat. Type 'exit' to quit.")
    stream_mode = True

    # Example extra parameters to test
    extra_params = {
        "raw": True,
    }

    # input in green method
    def input_in_green(prompt):
        return input(f"{Fore.GREEN}{prompt}{Style.RESET_ALL}")
    while True:
        user_input = input_in_green("\nhuman input on test app : ")
        if user_input.strip().lower() == "exit":
            print("Exiting...")
            break

        if stream_mode:
            # Pass extra params to chat_stream
            for chunk in session.chat_stream(user_input, **extra_params):
                print(chunk, end="", flush=True)
        else:
            # Pass extra params to chat
            response = session.chat(user_input, **extra_params)
            print(f"{response}")
            print("\n")  # New line after response

if __name__ == "__main__":
    main()
