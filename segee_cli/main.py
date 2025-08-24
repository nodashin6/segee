"""Command line interface for segee package."""

import os
import sys
from segee import SumSegmentTree, MinSegmentTree, MaxSegmentTree


# Configuration
LEAF_CELL_WIDTH = 12  # Base cell width for leaf level (bottom row)
COMMAND_ROWS = 20        # Number of command history rows to display
BORDER_COLOR = "\033[90m"  # Dark gray color for borders
COLOR_RESET = "\033[0m"    # Reset color

LOGO = """
    ✦ ･ ｡ ‧ ˚ ꒰ ⋆ ･ ｡ ‧ ˚ ✦ ˚ ‧ ｡ ･ ⋆ ꒱ ˚ ‧ ｡ ･ ✦
   
      ███████╗███████╗ ██████╗ ███████╗███████╗
     ██╔════╝██╔════╝██╔════╝ ██╔════╝██╔════╝
     ███████╗█████╗  ██║  ███╗█████╗  █████╗  
     ╚════██║██╔══╝  ██║   ██║██╔══╝  ██╔══╝  
     ███████║███████╗╚██████╔╝███████╗███████╗
     ╚══════╝╚══════╝ ╚═════╝ ╚══════╝╚══════╝
   
       ✦ CUI Segment Tree Calculator ✦
       
    ✦ ･ ｡ ‧ ˚ ꒰ ⋆ ･ ｡ ‧ ˚ ✦ ˚ ‧ ｡ ･ ⋆ ꒱ ˚ ‧ ｡ ･ ✦
"""


def get_terminal_width() -> int:
    """Get terminal width, default to 80 if not available."""
    try:
        return os.get_terminal_size().columns
    except OSError:
        return 80


def draw_tree_structure(tree=None) -> list[str]:
    """Draw segment tree structure as pyramid (1,2,4,8,16 cells per row)."""
    lines = []
    levels = [1, 2, 4, 8, 16]
    
    # For a 16-element tree, internal structure is:
    # Level 0: 1 node  (root) - internal index 0
    # Level 1: 2 nodes - internal indices 1, 2  
    # Level 2: 4 nodes - internal indices 3, 4, 5, 6
    # Level 3: 8 nodes - internal indices 7, 8, 9, 10, 11, 12, 13, 14
    # Level 4: 16 nodes (leaves) - user indices 0-15
    
    def get_tree_value(level: int, pos: int) -> str:
        """Get value for visualization based on level and position."""
        if tree is None:
            return "0"
        
        if level == 4:  # Leaf level - user indices 0-15
            user_index = pos
            if user_index < len(tree):
                return str(tree[user_index])
            return "0"
        else:  # Internal nodes
            # 長さ16なので計算コストを気にせず、正確性を優先
            try:
                # 内部データに直接アクセスできる場合
                if hasattr(tree, '_data') and hasattr(tree, '_offset'):
                    # セグメントツリーの内部インデックス計算
                    # Level 0: index 0 (root)
                    # Level 1: indices 1, 2  
                    # Level 2: indices 3, 4, 5, 6
                    # Level 3: indices 7-14
                    if level == 0:
                        internal_idx = 0
                    elif level == 1:
                        internal_idx = 1 + pos
                    elif level == 2:
                        internal_idx = 3 + pos
                    elif level == 3:
                        internal_idx = 7 + pos
                    else:
                        internal_idx = 0
                    
                    if internal_idx < len(tree._data):
                        value = tree._data[internal_idx]
                        # 無限大の場合は特別表示
                        if value == float('inf'):
                            return "inf"
                        elif value == float('-inf'):
                            return "-inf"
                        return str(value)
                
                # フォールバック：範囲クエリで可視化（パフォーマンス度外視）
                if level == 0:  # Root - 全体
                    return str(tree.prod(0, len(tree)))
                elif level == 1:  # Level 1 - 左右半分
                    mid = len(tree) // 2
                    if pos == 0:  # Left half
                        return str(tree.prod(0, mid))
                    else:  # Right half
                        return str(tree.prod(mid, len(tree)))
                elif level == 2:  # Level 2 - 4分割
                    quarter = len(tree) // 4
                    start = pos * quarter
                    end = (pos + 1) * quarter
                    return str(tree.prod(start, end))
                elif level == 3:  # Level 3 - 8分割
                    eighth = len(tree) // 8
                    start = pos * eighth
                    end = (pos + 1) * eighth
                    return str(tree.prod(start, end))
                return "0"
            except (AttributeError, IndexError, ValueError, TypeError) as e:
                # 長さ16なのでパフォーマンスは気にしない - デバッグ情報を残す
                return "?"
    
    # Base cell width for leaf level - configurable
    base_cell_width = LEAF_CELL_WIDTH
    
    for level_idx, cell_count in enumerate(levels):
        # Cell width doubles as we go up the tree
        # Level 4 (16 cells): width LEAF_CELL_WIDTH
        # Level 3 (8 cells): width LEAF_CELL_WIDTH * 2  
        # Level 2 (4 cells): width LEAF_CELL_WIDTH * 4
        # Level 1 (2 cells): width LEAF_CELL_WIDTH * 8
        # Level 0 (1 cell): width LEAF_CELL_WIDTH * 16
        level_from_bottom = len(levels) - 1 - level_idx
        cell_width = base_cell_width * (2 ** level_from_bottom)
        
        # Calculate consistent left padding for tree alignment
        # Always align tree to start from the same position
        padding = 0  # No centering - left align all levels
        
        # Create horizontal line pattern with gray color
        h_line = BORDER_COLOR + "─" * (cell_width - 1) + COLOR_RESET
        
        # Only add top border for the first level
        if level_idx == 0:
            if cell_count == 1:
                top_line = " " * padding + BORDER_COLOR + "┌" + COLOR_RESET + h_line + BORDER_COLOR + "┐" + COLOR_RESET
            else:
                separator = BORDER_COLOR + "┬" + COLOR_RESET + h_line
                top_line = " " * padding + BORDER_COLOR + "┌" + COLOR_RESET + h_line + separator * (cell_count - 1) + BORDER_COLOR + "┐" + COLOR_RESET
            lines.append(top_line)
        
        # Empty line for padding-top effect
        empty_line = " " * padding + BORDER_COLOR + "│" + COLOR_RESET
        for i in range(cell_count):
            empty_line += " " * (cell_width - 1) + BORDER_COLOR + "│" + COLOR_RESET
        lines.append(empty_line)
        
        # Content line with centered values
        content_line = " " * padding + BORDER_COLOR + "│" + COLOR_RESET
        for i in range(cell_count):
            # Get value using the helper function
            value = get_tree_value(level_idx, i)
            
            value_padding = (cell_width - 1 - len(value)) // 2
            left_pad = value_padding
            right_pad = cell_width - 1 - len(value) - left_pad
            content_line += " " * left_pad + value + " " * right_pad + BORDER_COLOR + "│" + COLOR_RESET
        lines.append(content_line)
        
        # Empty line for padding-bottom effect
        empty_line = " " * padding + BORDER_COLOR + "│" + COLOR_RESET
        for i in range(cell_count):
            empty_line += " " * (cell_width - 1) + BORDER_COLOR + "│" + COLOR_RESET
        lines.append(empty_line)
        
        # Bottom border for all levels
        if cell_count == 1:
            bottom_line = " " * padding + BORDER_COLOR + "└" + COLOR_RESET + h_line + BORDER_COLOR + "┘" + COLOR_RESET
        else:
            separator = BORDER_COLOR + "┴" + COLOR_RESET + h_line
            bottom_line = " " * padding + BORDER_COLOR + "└" + COLOR_RESET + h_line + separator * (cell_count - 1) + BORDER_COLOR + "┘" + COLOR_RESET
        lines.append(bottom_line)
    
    # Add index numbers row for the leaf level (last level)
    if level_idx == len(levels) - 1:
        # Add index row with yellow color
        index_line = " " * (padding + 1)  # +1 for left border alignment
        for i in range(cell_count):
            index_str = f"\033[33m{i}\033[0m"  # Yellow color with reset
            # Center the index in the cell (accounting for actual visible length)
            visible_len = len(str(i))  # Visible length without color codes
            index_padding = (cell_width - 1 - visible_len) // 2
            left_pad = index_padding
            right_pad = cell_width - 1 - visible_len - left_pad
            index_line += " " * left_pad + index_str + " " * right_pad
            # Add separator between cells (matching the table structure above)
            if i < cell_count - 1:
                index_line += " "
        lines.append(index_line)
    
    return lines


def draw_command_area(commands: list[str] = None) -> list[str]:
    """Draw user command area with command history."""
    if commands is None:
        commands = []
    
    lines = []
    lines.append(f"{BORDER_COLOR}┌─────── COMMAND ──────────────┐{COLOR_RESET}")
    
    # Show recent commands (configurable number of lines)
    display_commands = commands[-COMMAND_ROWS:] if len(commands) > COMMAND_ROWS else commands
    
    for i in range(COMMAND_ROWS):
        if i < len(display_commands):
            cmd = display_commands[i].replace('\t', ' ')[:28]  # Replace tabs with spaces and truncate
            lines.append(f"{BORDER_COLOR}│{COLOR_RESET} {cmd:<28} {BORDER_COLOR}│{COLOR_RESET}")
        elif i == len(display_commands):
            lines.append(f"{BORDER_COLOR}│{COLOR_RESET} >                            {BORDER_COLOR}│{COLOR_RESET}")
        else:
            lines.append(f"{BORDER_COLOR}│{COLOR_RESET}                              {BORDER_COLOR}│{COLOR_RESET}")
    lines.append(f"{BORDER_COLOR}└──────────────────────────────┘{COLOR_RESET}")
    return lines


def display_split_screen(commands: list[str] = None, tree=None) -> None:
    """Display split screen: command area (1/3) | tree structure (2/3)."""
    terminal_width = get_terminal_width()
    command_width = 32  # Width for command area
    gap_width = 8  # Gap between command area and tree
    
    command_lines = draw_command_area(commands)
    tree_lines = draw_tree_structure(tree)
    
    # Ensure both areas have same height
    max_height = max(len(command_lines), len(tree_lines))
    while len(command_lines) < max_height:
        command_lines.append(" " * 30)  # Match command area width
    while len(tree_lines) < max_height:
        tree_lines.append("")
    
    # Clear screen and display
    os.system('clear' if os.name == 'posix' else 'cls')
    for command_line, tree_line in zip(command_lines, tree_lines):
        gap = " " * gap_width
        print(f"{command_line:<{command_width}}{gap}{tree_line}")


def display_logo() -> None:
    """Display Segee startup logo."""
    print(LOGO)


def display_help_screen(tree_type: str) -> None:
    """Display full-screen help and wait for Enter to return."""
    os.system('clear' if os.name == 'posix' else 'cls')
    
    help_content = f"""
{BORDER_COLOR}╔══════════════════════════════════════════════════════════════════════════╗
║                            SEGEE HELP - {tree_type.upper()} TREE                            ║
╠══════════════════════════════════════════════════════════════════════════╣{COLOR_RESET}

{BORDER_COLOR}📋 BASIC COMMANDS:{COLOR_RESET}
  set/s <index> <value>    Set element at index to value
  add/a <index> <value>    Add value to element at index  
  query/q <left> <right>   Query range [left, right) (half-open)

{BORDER_COLOR}🔧 SPECIAL COMMANDS:{COLOR_RESET}
  /reset                   Clear tree and command history
  /home                    Return to tree type selection
  /help                    Show this help screen
  quit/exit               Exit the program

{BORDER_COLOR}📝 EXAMPLES:{COLOR_RESET}
  s 0 10                  → Set tree[0] = 10
  s 3 inf                 → Set tree[3] = inf (infinity)
  s 7 -inf                → Set tree[7] = -inf (negative infinity)
  a 5 -3                  → Add -3 to tree[5] 
  q 2 7                   → Query range [2, 7) - indices 2,3,4,5,6

{BORDER_COLOR}ℹ️  NOTES:{COLOR_RESET}
  • Tree size: 16 elements (indices 0-15)
  • All indices are 0-based
  • Query range is [left, right) - left inclusive, right exclusive
  • {tree_type.title()} tree returns {"sum" if tree_type == "sum" else "minimum" if tree_type == "min" else "maximum"} of the range

{BORDER_COLOR}🎨 VISUALIZATION:{COLOR_RESET}
  • Bottom row: Your data (indices 0-15)
  • Upper rows: Internal tree nodes
  • Yellow numbers: Array indices
  • Real-time updates after each command

{BORDER_COLOR}╚══════════════════════════════════════════════════════════════════════════╝{COLOR_RESET}

Press Enter to return to interactive mode..."""
    
    print(help_content)
    try:
        input()
    except (EOFError, KeyboardInterrupt):
        pass



def select_tree_type():
    """Select segment tree type."""
    print("Select segment tree type:")
    print("1. Sum Segment Tree")
    print("2. Min Segment Tree")
    print("3. Max Segment Tree")
    
    while True:
        try:
            choice = input("Enter choice (1-3): ")
            if choice == "1":
                return "sum", SumSegmentTree
            elif choice == "2":
                return "min", MinSegmentTree
            elif choice == "3":
                return "max", MaxSegmentTree
            else:
                print("Invalid choice. Please enter 1, 2, or 3.")
        except (EOFError, KeyboardInterrupt):
            print("\nExiting...")
            sys.exit(0)


def parse_command(cmd: str, tree, tree_type: str):
    """Parse and execute command."""
    parts = cmd.strip().split()
    if not parts:
        return None
    
    command = parts[0].lower()
    
    # Handle slash commands first
    if command.startswith('/'):
        if command == "/reset":
            return "reset"
        elif command == "/home":
            return "home"
        elif command == "/help":
            return "show_help"
        else:
            return "Unknown slash command. Try /help for available commands."
    
    def parse_value(value_str: str) -> float:
        """Parse value string, supporting inf and -inf."""
        if value_str.lower() in ['inf', 'infinity']:
            return float('inf')
        elif value_str.lower() in ['-inf', '-infinity']:
            return float('-inf')
        else:
            return int(value_str)
    
    try:
        if (command == "set" or command == "s") and len(parts) == 3:
            index = int(parts[1])
            value = parse_value(parts[2])
            if 0 <= index < len(tree):
                tree[index] = value
                return None  # No output for set commands
            else:
                return f"Index Error: {index} is out of range [0, {len(tree)-1}] (size={len(tree)})"
        
        elif (command == "add" or command == "a") and len(parts) == 3:
            index = int(parts[1])
            value = parse_value(parts[2])
            if 0 <= index < len(tree):
                tree[index] += value
                return None  # No output for add commands
            else:
                return f"Index Error: {index} is out of range [0, {len(tree)-1}] (size={len(tree)})"
        
        elif (command == "query" or command == "q") and len(parts) == 3:
            left, right = int(parts[1]), int(parts[2])
            if 0 <= left < right <= len(tree):
                if tree_type == "sum":
                    result = tree.sum(left, right)
                    return str(result)  # Just the value
                elif tree_type == "min":
                    result = tree.minimum(left, right)
                    return str(result)  # Just the value
                elif tree_type == "max":
                    result = tree.maximum(left, right)
                    return str(result)  # Just the value
            else:
                return f"Range Error: [{left}, {right}] is invalid for size {len(tree)} (valid: [0, {len(tree)-1}])"
        
        elif command in ["quit", "exit"]:
            return "quit"
        
        else:
            # 長さ16のツリーなので、親切なエラーメッセージを提供
            if command in ["set", "s", "add", "a"]:
                if len(parts) != 3:
                    return f"Usage: {command} <index> <value> (need exactly 2 arguments, got {len(parts)-1})"
                else:
                    return "Invalid arguments - check that index and value are integers"
            elif command in ["query", "q"]:
                if len(parts) != 3:
                    return f"Usage: {command} <left> <right> (need exactly 2 arguments, got {len(parts)-1})"
                else:
                    return "Invalid arguments - check that left and right are integers"
            else:
                return f"Unknown command: '{command}'. Type '/help' for available commands."
    
    except ValueError as e:
        return f"Invalid format: {str(e)} (ensure all numbers are integers)"
    except Exception as e:
        return f"Error: {str(e)}"


def interactive_mode(tree_type: str, tree_class):
    """Interactive command mode."""
    # Initialize tree with 16 elements (matching the visualization)
    tree = tree_class(16)
    commands = []
    
    while True:
        # Display current state with the tree object
        display_split_screen(commands, tree)
        
        try:
            # Get user input
            cmd = input("\n> ")
            if not cmd.strip():
                continue
                
            # Parse and execute command
            result = parse_command(cmd, tree, tree_type)
            
            if result == "quit":
                print("Goodbye!")
                break
            elif result == "reset":
                # Reinitialize tree and clear notebook
                tree = tree_class(16)
                commands = []
                continue
            elif result == "home":
                # Return to main menu
                return "home"
            elif result == "show_help":
                # Show full-screen help
                display_help_screen(tree_type)
                # Don't add help command to history
                continue
            else:
                commands.append(f"> {cmd}")
                if result:  # Only add non-None results
                    commands.append(result)
                    
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break


def main() -> None:
    """Main entry point for the segee CLI."""
    while True:
        display_logo()
        tree_type, tree_class = select_tree_type()
        print(f"\nSelected: {tree_type.title()} Segment Tree")
        print("\nCommands: set/s <index> <value>, add/a <index> <value>, query/q <left> <right> (half-open)")
        print("Special: /reset (clear), /home (return here), /help (show commands)")
        print("All indices are 0-based. Press Ctrl+C to exit.")
        input("\nPress Enter to start interactive mode...")
        
        result = interactive_mode(tree_type, tree_class)
        if result != "home":
            break  # Exit if not returning home


if __name__ == "__main__":
    main()