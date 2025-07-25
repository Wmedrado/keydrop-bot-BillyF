import sys
import os
import types

os.environ["IS_TEST_ENV"] = "true"

# Provide a lightweight stub for customtkinter if not installed
if "customtkinter" not in sys.modules:
    ctk = types.ModuleType("customtkinter")

    class Dummy:
        def __init__(self, *args, **kwargs):
            self.image = None

        def __getattr__(self, name):
            def method(*a, **k):
                return None

            return method

        def __call__(self, *args, **kwargs):
            return Dummy()

    class DummyStringVar:
        def __init__(self, value=""):
            self._value = value

        def set(self, value):
            self._value = value

        def get(self):
            return self._value

    ctk.CTk = Dummy
    ctk.CTkFrame = Dummy
    ctk.CTkButton = Dummy
    ctk.CTkLabel = Dummy
    ctk.CTkToplevel = Dummy
    ctk.CTkScrollableFrame = Dummy
    ctk.StringVar = DummyStringVar
    ctk.set_appearance_mode = lambda *a, **k: None
    sys.modules["customtkinter"] = ctk

# Stub minimal tkinter GUI elements
if "tkinter" not in sys.modules:
    tk = types.ModuleType("tkinter")

    class DummyTk:
        def title(self, *a, **k):
            pass

        def geometry(self, *a, **k):
            pass

        def protocol(self, *a, **k):
            pass

        def iconbitmap(self, *a, **k):
            pass

        def update_idletasks(self):
            pass

        def winfo_screenwidth(self):
            return 800

        def winfo_screenheight(self):
            return 600

        def winfo_exists(self):
            return True

        def destroy(self):
            pass

    class DummyFrame:
        def __init__(self, *a, **k):
            pass

        def pack(self, *a, **k):
            pass

        def pack_propagate(self, *a, **k):
            pass

    tk.Tk = DummyTk
    tk.Frame = DummyFrame
    tk.Label = Dummy
    tk.Button = Dummy
    tk.Text = Dummy
    tk.StringVar = DummyStringVar
    tk.Entry = Dummy
    tk.TclError = Exception
    tk.BooleanVar = DummyStringVar
    tk.Checkbutton = Dummy
    tk.font = types.SimpleNamespace(Font=lambda *a, **k: None)
    ttk = types.ModuleType("tkinter.ttk")
    ttk.Label = Dummy
    ttk.Button = Dummy
    ttk.Progressbar = Dummy
    ttk.Notebook = Dummy
    ttk.Frame = DummyFrame
    ttk.LabelFrame = DummyFrame

    class DummyTreeview(DummyFrame):
        def heading(self, *a, **k):
            pass

        def insert(self, *a, **k):
            pass

        def yview(self, *a, **k):
            pass

        def configure(self, *a, **k):
            pass

    class DummyScrollbar(DummyFrame):
        def set(self, *a, **k):
            pass

    ttk.Scrollbar = DummyScrollbar
    ttk.Treeview = DummyTreeview

    ttk.Treeview = DummyTreeview
    ttk.LabelFrame = DummyFrame
    tk.ttk = ttk
    tk.scrolledtext = types.SimpleNamespace(ScrolledText=Dummy)
    tk.messagebox = types.SimpleNamespace(
        showinfo=lambda *a, **k: None,
        showwarning=lambda *a, **k: None,
        showerror=lambda *a, **k: None,
    )
    tk.filedialog = types.SimpleNamespace(askopenfilename=lambda *a, **k: "")
    sys.modules["tkinter"] = tk
    sys.modules["tkinter.ttk"] = ttk

# Stub PIL ImageTk PhotoImage to avoid Tcl errors
try:
    from PIL import ImageTk  # type: ignore

    class DummyPhotoImage:
        def __init__(self, *a, **k):
            pass

    ImageTk.PhotoImage = DummyPhotoImage
except Exception:
    pass

# Stub pystray to avoid display errors during tests
if "pystray" not in sys.modules:
    pystray = types.ModuleType("pystray")

    class DummyIcon:
        def __init__(self, *a, **k):
            self.visible = False

        def run(self):
            self.visible = True

        def stop(self):
            self.visible = False

    pystray.Icon = DummyIcon
    pystray.MenuItem = lambda *a, **k: None
    pystray.Menu = lambda *a, **k: None
    sys.modules["pystray"] = pystray
