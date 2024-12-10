import subprocess

from rich.console import Console

from magnascale_automation.command.interactive.action.cluster import cluster_power_off
from magnascale_automation.command.interactive.action.cluster import enter_maintenance_mode
from magnascale_automation.command.interactive.action.cluster import exit_maintenance_mode
from magnascale_automation.command.interactive.action.cluster import refresh_cluster
from magnascale_automation.command.interactive.action.node import node_discover
from magnascale_automation.command.interactive.action.node import node_power_off


class Menu:
    """Class representing a single menu."""

    def __init__(self, name: str, action=None, is_dynamic: bool = False):
        """
        Initialize a menu.

        Args:
            name (str): The name of the menu.
            action (callable, optional): The action associated with the menu.
                If None, the menu has submenus.
        """
        self.name = name
        self.action = action
        self.is_dynamic = is_dynamic

        self.submenus = []
        self.parent = None  # To track the parent menu

    def add_submenu(self, submenu):
        """
        Add a submenu to the current menu.

        Args:
            submenu (Menu): The submenu object to be added.

        Raises:
            ValueError: If the current menu has an action, submenus cannot be added.
        """
        if self.action:
            raise ValueError(f"Menu '{self.name}' is an action and cannot have submenus.")
        submenu.parent = self  # Set the parent of the submenu
        self.submenus.append(submenu)

    def get_full_path(self):
        """
        Recursively build the full menu path.

        Returns:
            str: Full path of the menu.
        """
        if self.parent is None:
            return self.name
        return f"{self.parent.get_full_path()} > {self.name}"

    def run(self):
        """Run the current menu."""
        console = Console()

        while True:
            if self.action:
                # If the menu is an action, execute it directly.
                if self.is_dynamic:
                    self.action(self.name)
                else:
                    self.action()
                break

            # Display submenus with numbered choices.
            console.print(f"\n[bold blue]You are in the menu path: [cyan]{self.get_full_path()}[/cyan][bold blue].")
            for index, submenu in enumerate(self.submenus, start=1):
                console.print(f"{index}. {submenu.name}")
            console.print(f"{len(self.submenus) + 1}. Back")

            # Get user input.
            try:
                choice = int(input("Please enter your choice: "))
                if choice == len(self.submenus) + 1:
                    break
                if choice == 99 and self.parent is None:
                    enter_bash_command()
                elif 1 <= choice <= len(self.submenus):
                    self.submenus[choice - 1].run()
                else:
                    console.print("[red]Invalid choice. Please try again.[/red]")
            except ValueError:
                console.print("[red]Invalid input. Please enter a number.[/red]")


class MenuManager:
    """Class for managing multi-level menus."""

    def __init__(self):
        """Initialize the menu manager."""
        self.root_menu = Menu("Main")

    def add_menu(self, path: list, action=None):
        """
        Dynamically add menus.

        Args:
            path (list): The menu path represented as a list (e.g., ['Main', 'Submenu1', 'Submenu1-1']).
            action (callable, optional): The action associated with the menu. Defaults to None for menus with submenus.
        """
        current_menu = self.root_menu
        for menu_name in path:
            for submenu in current_menu.submenus:
                if submenu.name == menu_name:
                    current_menu = submenu
                    break
            else:
                new_menu = Menu(menu_name)
                current_menu.add_submenu(new_menu)
                current_menu = new_menu

        # Set the action for the last menu in the path.
        if action:
            current_menu.action = action

    def add_dynamic_submenus(self, path: list, submenu_names: list, action):
        """
        Dynamically add submenus under a specific path.

        Args:
            path (list): The menu path represented as a list.
            submenu_names (list): A list of submenu names to be added.
            action (callable): A function that generates actions for each submenu.
        """
        current_menu = self.root_menu
        for menu_name in path:
            for submenu in current_menu.submenus:
                if submenu.name == menu_name:
                    current_menu = submenu
                    break
            else:
                new_menu = Menu(menu_name)
                current_menu.add_submenu(new_menu)
                current_menu = new_menu

        for name in submenu_names:
            # Generate action using the action_generator with dynamic parameters.
            current_menu.add_submenu(Menu(name, action=action, is_dynamic=True))

    def run(self):
        """Run the root menu."""
        self.root_menu.run()


def enter_bash_command():
    """Execute a special hidden command."""
    console = Console()
    console.print(
        "[bold magenta]Entering Bash command environment. Type 'exit' to return to the main menu.[/bold magenta]"
    )

    while True:
        # Display a bash-like prompt
        command = input("[bash]$ ")
        if command.strip().lower() == "exit":
            console.print("[bold green]Exiting Bash environment and returning to the main menu.[/bold green]")
            break

        try:
            # Execute the command and capture the output
            result = subprocess.run(command, shell=True, text=True, capture_output=True)
            if result.stdout:
                console.print(f"[green]{result.stdout}[/green]")
            if result.stderr:
                console.print(f"[red]{result.stderr}[/red]")
        except Exception as e:
            console.print(f"[red]Error executing command: {e}[/red]")


# Build the menu structure.
def build_menu() -> MenuManager:
    """
    Build and return the menu manager with predefined menus.

    Returns:
        MenuManager: The menu manager with configured menus.
    """
    manager = MenuManager()

    # Add menus for cluster operations.
    manager.add_menu(["cluster", "maintenance-mode", "enter"], action=enter_maintenance_mode)
    manager.add_menu(["cluster", "maintenance-mode", "exit"], action=exit_maintenance_mode)
    manager.add_menu(["cluster", "refresh"], action=refresh_cluster)
    manager.add_menu(["cluster", "power-off"], action=cluster_power_off)

    nodes = ["node1", "node2", "node3"]
    manager.add_dynamic_submenus(["node", "power-off"], nodes, action=node_power_off)
    manager.add_menu(["node", "discover"], action=node_discover)

    return manager