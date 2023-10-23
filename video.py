import os
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from tkinter import ttk
from ttkthemes import ThemedStyle
from moviepy.editor import VideoFileClip

# Fonction pour sélectionner le fichier vidéo
def select_file():
    file_path = filedialog.askopenfilename()
    entry.delete(0, END)
    entry.insert(0, file_path)

# Fonction pour découper la vidéo en segments
def cut_video_into_segments():
    input_video = entry.get()
    segment_duration = int(segment_duration_entry.get())
    output_directory = "fragments"

    if not os.path.exists(input_video):
        messagebox.showerror("Erreur", "Veuillez sélectionner une vidéo valide.")
        return

    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    try:
        clip = VideoFileClip(input_video)
    except Exception as e:
        messagebox.showerror("Erreur", f"Impossible d'ouvrir la vidéo: {e}")
        return

    total_duration = clip.duration
    current_time = 0
    progress['maximum'] = total_duration

    while current_time < total_duration:
        if current_time + segment_duration <= total_duration:
            subclip = clip.subclip(current_time, current_time + segment_duration)
        else:
            subclip = clip.subclip(current_time, total_duration)
        output_path = os.path.join(output_directory, f"segment_{current_time}_{current_time + min(segment_duration, total_duration - current_time)}.mp4")
        subclip.write_videofile(output_path, codec="libx264")
        current_time += segment_duration
        progress['value'] = current_time
        percentage = (current_time / total_duration) * 100
        progress_label.config(text=f"{int(percentage)} %")
        root.update_idletasks() # Met à jour l'interface

    clip.close()
    messagebox.showinfo("Succès", f"Votre vidéo a été découpée avec succès. Les segments sont disponibles dans le dossier '{output_directory}'.")

# Création de la fenêtre principale
root = Tk()
root.title("Video Cutter")
root.geometry("1000x500")

# Configuration du thème
style = ThemedStyle(root)
style.set_theme("arc")

# Cadre pour les éléments de l'interface
frame = Frame(root)
frame.pack(padx=50, pady=50)

# Label et champ de saisie pour sélectionner le fichier vidéo
label = Label(frame, text="Sélectionnez la vidéo à découper:", font=('Arial', 14))
label.grid(row=0, column=0, padx=10, pady=10)

entry = Entry(frame, width=40, font=('Arial', 12))
entry.grid(row=0, column=1, padx=10, pady=10)

browse_button = Button(frame, text="Parcourir", command=select_file)
browse_button.grid(row=0, column=2, padx=10, pady=10)

# Label et champ de saisie pour la durée du segment
segment_duration_label = Label(frame, text="Durée du segment en secondes:", font=('Arial', 14))
segment_duration_label.grid(row=1, column=0, padx=10, pady=10)

segment_duration_entry = Entry(frame, width=10, font=('Arial', 12))
segment_duration_entry.grid(row=1, column=1, padx=10, pady=10)

# Bouton pour démarrer le découpage
start_button = Button(frame, text="Démarrer le découpage", command=cut_video_into_segments, font=('Arial', 14))
start_button.grid(row=2, column=1, padx=10, pady=10)

# Cadre pour la barre de progression
progress_frame = Frame(root)
progress_frame.pack(padx=50, pady=50)

# Label pour afficher le pourcentage de progression
progress_label = Label(progress_frame, text="", font=('Arial', 14))
progress_label.pack(pady=10)

# Barre de progression
progress = ttk.Progressbar(progress_frame, orient=HORIZONTAL, length=500, mode='determinate')
progress.pack(pady=10)

root.mainloop()
