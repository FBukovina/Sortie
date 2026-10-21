from pathlib import Path
import shutil
import tkinter as tk
from tkinter import filedialog, ttk, messagebox
from sorter import get_category
folder = Path("test_files")


for file in folder.iterdir():
    if file.is_file():
        extension = file.suffix.lower()

        if extension in [".jpg", ".jpeg", ".png"]:
            category = "Images"
        elif extension in [".pdf", ".docx", ".txt"]:
            category = "Documents"
        elif extension in [".mp3", ".wav"]:
            category = "Audio"
        else:
            category = "Others"

        print(f"{file.name} -> {category}")


root = tk.Tk()
root.last_moves = []

def choose_folder():
    selected_folder = filedialog.askdirectory()

    if selected_folder:
        root.selected_folder = Path(selected_folder)
        folder_label.config(
            text=f"Selected: {Path(selected_folder).name}"
        )
        file_list.delete(0, tk.END)

        for file in Path(selected_folder).iterdir():
            if file.is_file():
                file_list.insert(tk.END, f"{file.name} -> {get_category(file)}")

def preview_sort():
    if not hasattr(root, "selected_folder"):
        return

    file_list.delete(0, tk.END)

    for file in root.selected_folder.iterdir():
        if file.is_file():
            category = get_category(file)
            destination = Path(category) / file.name

            file_list.insert(
                tk.END,
                f"{file.name} -> {destination}"
            )

def organize_files():
    if not hasattr(root, "selected_folder"):
        messagebox.showwarning("Sortie", "Choose a folder first.")
        return

    folder = root.selected_folder
    files = [
        file for file in folder.iterdir()
        if file.is_file() and not file.name.startswith(".")
    ]

    if not messagebox.askyesno(
        "Organize Files",
        f"Move{len(files)} files into category folders?"
    ):
        return

    moved = 0
    skipped = 0
    moved_files = []

    for file in files:
        category = get_category(file)
        destination = folder / category / file.name

        if destination.exists():
            skipped += 1
            continue

        destination.parent.mkdir(exist_ok=True)
        shutil.move(str(file), str(destination))
        moved_files.append((destination, file))
        moved += 1

    if moved_files:
        root.last_moves = moved_files

    messagebox.showinfo(
        "Sortie",
        f"Moved: {moved}\nSkipped: {skipped}"
        )
preview_sort()

def undo_sort():
    if not root.last_moves:
        messagebox.showinfo("Sortie", "No moves to undo.")
        return

    if not messagebox.askyesno(
        "Undo Sort",
        f"Restore {len(root.last_moves)} moved files?"
    ):
        return

    restored = 0
    remaining = []

    for destination, original in reversed(root.last_moves):
        if not destination.is_file() or original.exists():
            remaining.append((destination, original))
            continue

        try:
            shutil.move(str(destination), str(original))
            restored += 1
        except OSError:
            remaining.append((destination, original))

        root.last_moves = remaining

        messagebox.showinfo(
            "Sortie",
            f"Restored: {restored}\nSkipped: {len(remaining)}"
            )
        
preview_sort()

root.title("Sortie")
root.geometry("600x450")
root.configure(bg="#2d2929")

title = tk.Label(root, text="Sortie",font=("Helvetica", 26, "bold"), fg="white", bg="#2d2929")
title.pack(pady=25)

test_button = tk.Button(root, text="Choose Folder", command=choose_folder)
test_button.pack(pady=10)

preview_button = tk.Button(
    root,
    text="Preview Sort",
    command=preview_sort
)
preview_button.pack(pady=5)

organize_button = tk.Button(
    root,
    text="Organize Files",
    command=organize_files
)
organize_button.pack(pady=5)

undo_button = tk.Button(
    root,
    text="Undo Last Sort",
    command=undo_sort
)
undo_button.pack(pady=5)

folder_label = tk.Label(
    root,
    text="No folder selected",
    fg="white",
    bg="#2d2929"
)
folder_label.pack(pady=10)

file_list = tk.Listbox(
    root,
    font=("Helvetica", 13),
    bg="#383333",
    fg="white",
    selectbackground="#555555",
    borderwidth=0,
    highlightthickness=0
)

file_list.pack(fill="both", expand=True, padx=20, pady=15)

root.mainloop()