from .system import System
from .terminal import ManagerTerminal, ProviderTerminal, InteractiveMode


def prompt_terminal_mode(
    system: System,
) -> ProviderTerminal | ManagerTerminal | InteractiveMode | None:
    print("Terminal Modes:")
    print("\t(1) Provider Terminal")
    print("\t(2) Manager Terminal")
    print("\t(3) Interactive Mode")
    choice = input("Enter Mode (1-3): ")
    if choice == "1":
        return ProviderTerminal(system)
    elif choice == "2":
        return ManagerTerminal(system)
    elif choice == "3":
        return InteractiveMode(system)
    else:
        return None


print("ChocAn Simulator Started")
try:
    system = System("data")
except Exception as e:
    print(e)
    exit(1)

print("System Initialized")
print()

terminal = prompt_terminal_mode(system)
while terminal is None:
    print()
    terminal = prompt_terminal_mode(system)

should_continue = True
while should_continue:
    print()
    try:
        should_continue = terminal.run_command_menu()
    except Exception as e:
        print(e)
        should_continue = True

print("ChocAn Simulator Stopped")
