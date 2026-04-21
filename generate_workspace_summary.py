import os
from pathlib import Path
from datetime import datetime

def generate_workspace_summary(workspace_path, output_file):
    """
    Generate a comprehensive summary of the workspace and save to a text file.
    
    Args:
        workspace_path: Path to the workspace directory
        output_file: Output file path for the summary
    """
    workspace_path = Path(workspace_path)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        # Header
        f.write("=" * 80 + "\n")
        f.write("WORKSPACE SUMMARY\n")
        f.write("=" * 80 + "\n\n")
        
        # Basic Info
        f.write(f"Workspace Path: {workspace_path.absolute()}\n")
        f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        # Directory Structure
        f.write("-" * 80 + "\n")
        f.write("DIRECTORY STRUCTURE\n")
        f.write("-" * 80 + "\n\n")
        
        def walk_directory(path, prefix="", is_last=True):
            """Recursively walk directory and write to file."""
            try:
                items = sorted(path.iterdir(), key=lambda x: (x.is_file(), x.name))
                dirs = [item for item in items if item.is_dir()]
                files = [item for item in items if item.is_file()]
                
                # Process directories first
                for i, item in enumerate(dirs):
                    is_last_item = (i == len(dirs) - 1) and len(files) == 0
                    current_prefix = "└── " if is_last_item else "├── "
                    f.write(prefix + current_prefix + item.name + "/\n")
                    
                    next_prefix = prefix + ("    " if is_last_item else "│   ")
                    walk_directory(item, next_prefix, is_last_item)
                
                # Process files
                for i, item in enumerate(files):
                    is_last_item = (i == len(files) - 1)
                    current_prefix = "└── " if is_last_item else "├── "
                    size_kb = item.stat().st_size / 1024
                    f.write(f"{prefix}{current_prefix}{item.name} ({size_kb:.2f} KB)\n")
                    
            except PermissionError:
                f.write(prefix + "[Permission Denied]\n")
        
        f.write(f"{workspace_path.name}/\n")
        walk_directory(workspace_path)
        
        # File Statistics
        f.write("\n" + "-" * 80 + "\n")
        f.write("FILE STATISTICS\n")
        f.write("-" * 80 + "\n\n")
        
        total_files = 0
        total_dirs = 0
        total_size = 0
        file_types = {}
        
        for root, dirs, files in os.walk(workspace_path):
            total_dirs += len(dirs)
            total_files += len(files)
            
            for file in files:
                file_path = Path(root) / file
                file_ext = file_path.suffix or "[No Extension]"
                file_size = file_path.stat().st_size
                total_size += file_size
                
                if file_ext not in file_types:
                    file_types[file_ext] = {"count": 0, "size": 0}
                
                file_types[file_ext]["count"] += 1
                file_types[file_ext]["size"] += file_size
        
        f.write(f"Total Directories: {total_dirs}\n")
        f.write(f"Total Files: {total_files}\n")
        f.write(f"Total Size: {total_size / (1024*1024):.2f} MB\n\n")
        
        f.write("File Types Breakdown:\n")
        f.write("-" * 40 + "\n")
        for ext in sorted(file_types.keys()):
            count = file_types[ext]["count"]
            size = file_types[ext]["size"] / 1024
            f.write(f"{ext:20} {count:5} files  {size:10.2f} KB\n")
        
        # Detailed File Listing
        f.write("\n" + "-" * 80 + "\n")
        f.write("DETAILED FILE LISTING\n")
        f.write("-" * 80 + "\n\n")
        
        for root, dirs, files in os.walk(workspace_path):
            if files:
                rel_root = Path(root).relative_to(workspace_path)
                if rel_root != Path("."):
                    f.write(f"\n{rel_root}/\n")
                else:
                    f.write("\n[Root]\n")
                
                for file in sorted(files):
                    file_path = Path(root) / file
                    size_kb = file_path.stat().st_size / 1024
                    f.write(f"  {file:<40} {size_kb:>10.2f} KB\n")
        
        # Footer
        f.write("\n" + "=" * 80 + "\n")
        f.write("End of Workspace Summary\n")
        f.write("=" * 80 + "\n")
    
    print(f"Workspace summary generated: {output_file}")

if __name__ == "__main__":
    # Set workspace path to current directory
    workspace_path = os.getcwd()
    output_file = os.path.join(workspace_path, "workspace_summary.txt")
    
    generate_workspace_summary(workspace_path, output_file)
