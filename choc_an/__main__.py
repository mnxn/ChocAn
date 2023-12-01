from choc_an import system, terminal


def prompt_terminal_mode(
    sys: system.System,
) -> (
    None
    | terminal.ProviderTerminal
    | terminal.ManagerTerminal
    | terminal.InteractiveMode
):
    print("Terminal Modes:")
    print("\t(1) Provider Terminal")
    print("\t(2) Manager Terminal")
    print("\t(3) Interactive Mode")
    choice = input("Enter Mode (1-3): ")
    if choice == "1":
        return terminal.ProviderTerminal(sys)
    elif choice == "2":
        return terminal.ManagerTerminal(sys)
    elif choice == "3":
        return terminal.InteractiveMode(sys)
    else:
        return None


print("ChocAn Simulator Started")
try:
    sys = system.System("data")
except Exception as e:
    print(e)
    exit(1)

print("System Initialized")
print()

term = prompt_terminal_mode(sys)
while term is None:
    print()
    term = prompt_terminal_mode(sys)

should_continue = True
while should_continue:
    print()
    try:
        should_continue = term.run_command_menu()
    except Exception as e:
        print(e)
        should_continue = True

print("ChocAn Simulator Stopped")
