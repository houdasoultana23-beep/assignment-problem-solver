import customtkinter as ctk
import numpy as np


def phase1(cout_input):
    
    cout = cout_input.copy()
    
    for line in cout:
        minimum = min(line)
        for i, element in enumerate(line):
            line[i] -= minimum
            
    
    for colonne in cout.T:
        minimum = min(colonne)
        for j, element in enumerate(colonne):
            colonne[j] -= minimum
            
    
    return cout

def phase2(cout_input):
    
    cout = cout_input.copy()
    
    solution_found = False
    
    while np.any(cout == 0):

        zero_mirror = (cout == 0)

        num_zeros_line = zero_mirror.sum(axis=1)
        num_zeros_column = zero_mirror.sum(axis=0)

        valid = np.where(num_zeros_line > 0)[0]
        indices = valid[np.where(num_zeros_line[valid] == min(num_zeros_line[valid]))[0]]

        zero_barr = []
        for i in indices:
            for j in range(cout.shape[1]):
                if zero_mirror[i, j] == True:
                    zero_line = num_zeros_line[i] - 1
                    zero_colomn = num_zeros_column[j] - 1
                    zero_barr.append((zero_line + zero_colomn, i, j))

        _, x, y = min(zero_barr, key=lambda x: x[0])



        for i in range(cout.shape[0]):
            for j in range(cout.shape[1]):
                if cout[i, j] == 0:
                    if i == x and j == y:
                        cout[i, j] = -1
                    elif i == x or j == y:
                        cout[i, j] = -2
    
    if np.all(np.sum(cout == -1, axis=1) == 1) and \
    np.all(np.isin(np.argmax(cout == -1, axis=1), \
                       np.unique(np.argmax(cout == -1, axis=1)))):
        solution_found = True
    
    
    return cout, solution_found

def phase3(cout_input):
    
    cout = cout_input.copy()
    
    marked_lines = []
    marked_cols = []
    
    marked_lines = np.where(np.all(cout != -1, axis=1))[0].tolist()

    possible = True
    
    while possible:
        possible = False
        for line in cout[marked_lines]:
            for j, element in enumerate(line):
                if element == -2 and j not in marked_cols:
                    marked_cols.append(j)
                    possible = True
        for column in cout.T[marked_cols]:
            for i, element in enumerate(column):
                if element == -1 and i not in marked_lines:
                    marked_lines.append(i)
                    possible = True
    
                    

    return cout, marked_lines, marked_cols

def phase4(cout_input, marked_lines, marked_cols):
    
    cout = cout_input.copy()
    
    cout[cout == -1] = 0
    cout[cout == -2] = 0
    
    dashed_lines = [i for i in range(cout.shape[0]) if i not in marked_lines]
    dashed_cols = sorted(marked_cols)
    
    non_dashed_lines = sorted(marked_lines)
    non_dashed_cols = [j for j in range(cout.shape[1]) if j not in marked_cols]
    
    if not non_dashed_lines or not non_dashed_cols:
        minimum = 0
    else:
        minimum = np.min(cout[np.ix_(non_dashed_lines, non_dashed_cols)])
    
    for i in range(cout.shape[0]):
        for j in range(cout.shape[1]):
            if i in non_dashed_lines and j in non_dashed_cols:
                cout[i][j] -= minimum
            elif i in dashed_lines and j in dashed_cols:
                cout[i][j] += minimum
    
    return cout

def phase5(cout_input, cout_initial):
    
    cout = cout_input.copy()
    
    cout_verification, solution_found = phase2(cout)
    
    if solution_found:
        solution = np.vstack(np.where(cout_verification == -1)) + 1
        solution_sum = np.sum(cout_initial[(cout_verification == -1)])
    
    else:
        solution = np.empty(0)
        solution_sum = None
    
    return cout, solution, solution_sum


def konig(init):
    
    cout_initial = np.array(init)
    cout = cout_initial.copy()
    
    solution = np.empty(0)
    solution_sum = 0
    
    cout = phase1(cout)
    cout, solution_found = phase2(cout)
    
    if solution_found:
        cout, solution, solution_sum = phase5(cout, cout_initial)
    else:
        while not solution.any():
            cout, solution_found = phase2(cout)
            cout, marked_lines, marked_cols = phase3(cout)
            cout = phase4(cout, marked_lines, marked_cols)
            cout, solution, solution_sum = phase5(cout, cout_initial)
    
    return cout, solution, solution_sum



#interface 




import customtkinter as ctk

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

root = ctk.CTk()
root.title("Méthode Hongroise - Solveur")
root.geometry("1100x650")

header_frame = ctk.CTkFrame(root, corner_radius=20, fg_color="#263238")
header_frame.pack(fill="x", pady=10)

header_label = ctk.CTkLabel(
    header_frame,
    text="✨ Méthode Hongroise – Solveur d’Affectation ✨",
    font=("Roboto", 28, "bold"),
    text_color="#4DD0E1"
)
header_label.pack(pady=10)

main_frame = ctk.CTkFrame(root, fg_color="#0F0F0F", corner_radius=20)
main_frame.pack(expand=True, fill="both", padx=20, pady=10)

left_frame = ctk.CTkFrame(main_frame, corner_radius=15, fg_color="#263238", width=450)
left_frame.pack(side="left", fill="y", padx=15, pady=15)

lbl_matrice = ctk.CTkLabel(
    left_frame,
    text="📌 Taille de la matrice (n × n)",
    font=("Roboto", 20, "bold"),
    text_color="#4DD0E1"
)
lbl_matrice.pack(pady=15)

matrix_size_entry = ctk.CTkEntry(left_frame, width=150, placeholder_text="Ex : 4")
matrix_size_entry.pack(pady=5)

entries = []
input_matrix_frame = ctk.CTkFrame(left_frame, fg_color="#37474F", corner_radius=10)
input_matrix_frame.pack(pady=20)

def saisie_matrice():
    try:
        size = int(matrix_size_entry.get())
        if size <= 0:
            raise ValueError("La taille doit être un entier positif.")

        for w in input_matrix_frame.winfo_children():
            w.destroy()
        entries.clear()

        for i in range(size):
            row_entries = []
            for j in range(size):
                entry = ctk.CTkEntry(input_matrix_frame, width=60, placeholder_text=f"{i+1},{j+1}")
                entry.grid(row=i, column=j, padx=5, pady=5)
                row_entries.append(entry)
            entries.append(row_entries)
    except Exception as e:
        error_label.configure(text=f"❌ {str(e)}")

btn_generate = ctk.CTkButton(left_frame, text="Générer la matrice",
                             fg_color="#4DD0E1", text_color="black",
                             command=saisie_matrice)
btn_generate.pack(pady=10)

right_frame = ctk.CTkFrame(main_frame, corner_radius=15, fg_color="#263238")
right_frame.pack(side="right", expand=True, fill="both", padx=15, pady=15)

result_title = ctk.CTkLabel(
    right_frame,
    text="📘 Résultat de la Méthode Hongroise",
    font=("Roboto", 22, "bold"),
    text_color="#4DD0E1"
)
result_title.pack(pady=15)

solution_box = ctk.CTkTextbox(right_frame, height=300, width=400, font=("Roboto", 32 , "bold"))
solution_box.pack(pady=10)

sum_box = ctk.CTkTextbox(right_frame, height=70, width=400, font=("Roboto", 18))
sum_box.pack(pady=10)

error_label = ctk.CTkLabel(right_frame, text="", text_color="red", font=("Roboto", 16))
error_label.pack(pady=10)

def recuperer_matrice():
    try:
        matrix = []
        for i, row_entries in enumerate(entries):
            row = []
            for j, entry in enumerate(row_entries):
                value = entry.get().strip()
                if not value:
                    raise ValueError(f"Cellule vide en ({i+1},{j+1})")
                row.append(float(value))
            matrix.append(row)

        _, solution, solution_sum = konig(matrix)

        solution_box.delete("1.0", "end")
        sum_box.delete("1.0", "end")

        solution_box.insert("end", f"Solution trouvée :\n\n{solution}")
        solution_box.tag_config("center", justify='center')
        solution_box.tag_add("center", "1.0", "end")
        sum_box.insert("end", f"🔹 Somme optimale : {solution_sum}")

    except Exception as e:
        error_label.configure(text=f"❌ {str(e)}")

btn_submit = ctk.CTkButton(left_frame, text="Résoudre",
                           fg_color="#00C853", text_color="white",
                           height=40, command=recuperer_matrice)
btn_submit.pack(pady=15)

root.mainloop()
