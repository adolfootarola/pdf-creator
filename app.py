import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import os

class PDFCreatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image to PDF Creator")
        self.root.geometry("800x600")

        # Dictionary structure: {'path': str, 'rotation': int}
        self.image_data = [] 
        self.current_preview_image = None
        
        self.a4_mode = tk.BooleanVar() # Control variable for A4 mode

        self.setup_ui()

    def setup_ui(self):
        # Main Container
        main_frame = tk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Left Panel (Controls and List)
        left_panel = tk.Frame(main_frame)
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Instructions
        instruction_label = tk.Label(left_panel, text="Select images, rotate if needed, and create PDF", pady=5)
        instruction_label.pack()

        # Listbox Setup
        list_frame = tk.Frame(left_panel)
        list_frame.pack(fill=tk.BOTH, expand=True, pady=5)

        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.file_listbox = tk.Listbox(list_frame, selectmode=tk.SINGLE, yscrollcommand=scrollbar.set)
        self.file_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.file_listbox.yview)
        
        self.file_listbox.bind('<<ListboxSelect>>', self.show_preview)

        # Buttons Frame
        btn_frame = tk.Frame(left_panel)
        btn_frame.pack(fill=tk.X, pady=10)

        # File Controls
        add_btn = tk.Button(btn_frame, text="Add Images", command=self.add_images, bg="#e1e1e1")
        add_btn.grid(row=0, column=0, padx=5, pady=5)

        remove_btn = tk.Button(btn_frame, text="Remove Selected", command=self.remove_image, bg="#ffcccc")
        remove_btn.grid(row=0, column=1, padx=5, pady=5)

        # Ordering Controls
        up_btn = tk.Button(btn_frame, text="Move Up", command=self.move_up)
        up_btn.grid(row=1, column=0, padx=5, pady=5)

        down_btn = tk.Button(btn_frame, text="Move Down", command=self.move_down)
        down_btn.grid(row=1, column=1, padx=5, pady=5)

        # Generate Button Area
        action_frame = tk.Frame(left_panel)
        action_frame.pack(fill=tk.X, pady=10)

        # A4 Checkbox
        a4_check = tk.Checkbutton(action_frame, text="Fit pages to A4", variable=self.a4_mode)
        a4_check.pack(fill=tk.X, pady=(0, 5))

        generate_btn = tk.Button(action_frame, text="Generate PDF", command=self.generate_pdf, bg="#ccffcc", height=2)
        generate_btn.pack(fill=tk.X)

        # Right Panel (Preview)
        right_panel = tk.Frame(main_frame, width=350, relief=tk.SUNKEN, borderwidth=1)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, padx=(10, 0))
        right_panel.pack_propagate(False)

        tk.Label(right_panel, text="Preview").pack(pady=5)
        
        self.preview_label = tk.Label(right_panel, text="No image selected")
        self.preview_label.pack(expand=True)

        # Rotation Controls
        rotate_frame = tk.Frame(right_panel)
        rotate_frame.pack(side=tk.BOTTOM, pady=20)

        rot_left_btn = tk.Button(rotate_frame, text="⟲ Rotate Left", command=self.rotate_left)
        rot_left_btn.pack(side=tk.LEFT, padx=10)

        rot_right_btn = tk.Button(rotate_frame, text="Rotate Right ⟳", command=self.rotate_right)
        rot_right_btn.pack(side=tk.LEFT, padx=10)

    def add_images(self):
        files = filedialog.askopenfilenames(
            title="Select Images",
            filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp;*.tiff;*.gif")]
        )
        if files:
            for file_path in files:
                self.image_data.append({'path': file_path, 'rotation': 0})
                self.file_listbox.insert(tk.END, os.path.basename(file_path))

    def show_preview(self, event=None):
        selected_indices = self.file_listbox.curselection()
        if not selected_indices:
            self.preview_label.config(image='', text="No image selected")
            return

        index = selected_indices[0]
        if index < len(self.image_data):
            data = self.image_data[index]
            file_path = data['path']
            rotation = data['rotation']

            try:
                img = Image.open(file_path)
                
                if rotation != 0:
                    img = img.rotate(rotation, expand=True)

                img.thumbnail((300, 300))
                
                photo = ImageTk.PhotoImage(img)
                self.preview_label.config(image=photo, text="")
                self.current_preview_image = photo
            except Exception as e:
                self.preview_label.config(image='', text=f"Error loading preview")
                print(f"Preview error: {e}")

    def rotate_left(self):
        self._rotate_image(90)

    def rotate_right(self):
        self._rotate_image(-90)

    def _rotate_image(self, angle):
        selected_indices = self.file_listbox.curselection()
        if not selected_indices:
            return
        
        index = selected_indices[0]
        self.image_data[index]['rotation'] += angle
        self.show_preview()

    def remove_image(self):
        selected_indices = self.file_listbox.curselection()
        if not selected_indices:
            return
        
        index = selected_indices[0]
        self.file_listbox.delete(index)
        del self.image_data[index]
        self.show_preview()

    def move_up(self):
        selected_indices = self.file_listbox.curselection()
        if not selected_indices:
            return

        index = selected_indices[0]
        if index > 0:
            item = self.image_data.pop(index)
            self.image_data.insert(index - 1, item)
            
            text = self.file_listbox.get(index)
            self.file_listbox.delete(index)
            self.file_listbox.insert(index - 1, text)
            
            self.file_listbox.selection_set(index - 1)
            self.show_preview()

    def move_down(self):
        selected_indices = self.file_listbox.curselection()
        if not selected_indices:
            return

        index = selected_indices[0]
        if index < len(self.image_data) - 1:
            item = self.image_data.pop(index)
            self.image_data.insert(index + 1, item)
            
            text = self.file_listbox.get(index)
            self.file_listbox.delete(index)
            self.file_listbox.insert(index + 1, text)
            
            self.file_listbox.selection_set(index + 1)
            self.show_preview()

    def generate_pdf(self):
        if not self.image_data:
            messagebox.showwarning("No Images", "Please add images to generate a PDF.")
            return

        save_path = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf")]
        )

        if not save_path:
            return

        try:
            images = []
            for data in self.image_data:
                img = Image.open(data['path'])
                
                # Apply stored rotation
                if data['rotation'] != 0:
                    img = img.rotate(data['rotation'], expand=True)

                if img.mode != 'RGB':
                    img = img.convert('RGB')

                # A4 Logic
                if self.a4_mode.get():
                    a4_size = (595, 842) # A4 size in points
                    a4_img = Image.new('RGB', a4_size, (255, 255, 255)) # White background
                    
                    # Calculate resize ratio to fit A4
                    img_ratio = img.width / img.height
                    target_ratio = a4_size[0] / a4_size[1]
                    
                    if img_ratio > target_ratio:
                         # Fit to width
                        new_width = a4_size[0]
                        new_height = int(new_width / img_ratio)
                    else:
                        # Fit to height
                        new_height = a4_size[1]
                        new_width = int(new_height * img_ratio)
                        
                    img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
                    
                    # Center image
                    x = (a4_size[0] - new_width) // 2
                    y = (a4_size[1] - new_height) // 2
                    a4_img.paste(img, (x, y))
                    
                    images.append(a4_img)
                else:
                    images.append(img)

            if images:
                first_image = images[0]
                if len(images) > 1:
                    first_image.save(save_path, save_all=True, append_images=images[1:])
                else:
                    first_image.save(save_path)
                
                messagebox.showinfo("Success", f"PDF successfully created at:\n{save_path}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate PDF:\n{str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = PDFCreatorApp(root)
    root.mainloop()
