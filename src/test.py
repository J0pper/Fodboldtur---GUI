import customtkinter

customtkinter.set_default_color_theme("dark-blue")


app = customtkinter.CTk()
app.grid_columnconfigure(2, weight=1)
app.grid_rowconfigure(1, weight=1)

toplevel = customtkinter.CTkToplevel()


frame_2 = customtkinter.CTkScrollableFrame(app, orientation="vertical", label_text="CTkScrollableFrame")
frame_2.grid(row=1, column=0, padx=20, pady=20)

somthing = {"0": "0", "1": "1", "2": "2", "3": "3"}

for i, j in somthing.items():
    customtkinter.CTkLabel(frame_2, text=f"{i}: {j}").grid(row=i, padx=10, pady=2)


app.mainloop()