[![Open in Visual Studio Code](https://classroom.github.com/assets/open-in-vscode-c66648af7eb3fe8bc4f294546bfd86ef473780cde1dea487d3c4ff354943c9ae.svg)](https://classroom.github.com/online_ide?assignment_repo_id=10264207&assignment_repo_type=AssignmentRepo)


# KB-F_02_TugasKelompok

## Anggota
### Nama Kelompok : Cucur Adabi
|     | Nama                              | NRP        | 
| --- | --------------------------------- | ---------- | 
| 1   | Rizky Alifiyah Rahma              | 5025211208 | 
| 2   | Salsabila Fatma Aripa             | 5025211057 | 
| 3   | Tsabita Putri Ramadhany           | 5025211130 |

# Tugas 3 : 8-Queen using Local Search
![image](https://user-images.githubusercontent.com/90395116/224132757-806a3ae8-929e-4d9a-9051-07a0ec8ef4d0.png)

8 Queens Puzzle merupakan sebuah problem di mana 8 queens yang diletakkan di papan catur tidak mengancam satu sama lain , baik itu  secara vertikal, horizontal, dan diagonal. Dalam tugas ini, ada 2 pendekatan yang kami lakukan:

## Hill Climbing Algorithm
![image](https://user-images.githubusercontent.com/90395116/224133612-875ce5c6-38ed-46df-9b13-a0ff5db8cc6c.png)
![image](https://user-images.githubusercontent.com/90395116/224133761-e4a45a80-409f-4b24-9d18-9d8a7913cc5f.png)

Pendekatan pertama yang akan kami lakukan adalah Local Search menggunakan Algoritma Hill Climbing. Hill Climbing Algorithm merupakan sebuah Heuristic Search yang digunakan untuk mengoptimasi sebuah masalah secara sistematis di lingkup Kecerdasan Buatan.
Diberikan sebuah input yang besar dengan heuristic function yang bagus, program ini akan berjalan untuk mencari solusi yang terbaik

- Local Maximum = State yang lebih baik dari state sekitar, namun bukan yang terbaik
- Global Maximum = State terbaik yang memiliki objective value tertinggi
- Current State = State dalam diagram dimana agent saat ini
- Flat Local Maximum = State dimana state sekitar memiliki nilai yang sama
- Shoulder  = space dengan area datar yang membuat algoritma pencarian tidak punya arah

Pada kasus 8-Queen Puzzle, pergerakan Queen diasumsikan sama halnya dengan mereka dapat berjalan hanya dengan kolom yang dimilikinya demi membatasi pergerakan. Oleh karena itu, perhitungan collapse sederhana dan lebih struktural. Berikut adalah kodenya:
```python
import random

# Inisialisasi papan catur dan posisi awal queen
board_size = 8
current_state = start_state = [1, 3, 0, 6, 4, 7, 5, 2]

# Definisi fungsi untuk menghitung jumlah konflik pada papan catur
def count_conflicts(state):
    conflicts = 0
    for i in range(len(state)):
        for j in range(i+1, len(state)):
            if state[i] == state[j] or abs(state[i]-state[j]) == j-i:
                conflicts += 1
    return conflicts

# Definisi fungsi untuk mencari posisi queen yang dapat dipindahkan untuk meminimalkan konflik
def find_best_move(state):
    best_move = None
    min_conflicts = board_size
    for i in range(len(state)):
        for j in range(board_size):
            if j != state[i]:
                new_state = state.copy()
                new_state[i] = j
                new_conflicts = count_conflicts(new_state)
                if new_conflicts < min_conflicts:
                    best_move = (i, j)
                    min_conflicts = new_conflicts
    return best_move

# Definisi fungsi utama untuk menyelesaikan 8 queen tidak 
# saling menyerang dengan hill climbing
def hill_climbing(state):
    while True:
        best_move = find_best_move(state)
        if best_move is None:
            break
        i, j = best_move
        state[i] = j
        if count_conflicts(state) == 0:
            return state
    return None

# Menyelesaikan 8 queen tidak saling menyerang dengan hill climbing 
# dan mencetak hasilnya
print("Posisi awal:", start_state)
solution = hill_climbing(current_state)
if solution is not None:
    print("Solusi ditemukan:", solution)
else:
    print("Tidak ada solusi yang ditemukan.")
```
Berikut adalah hasilnya:<br>
![image](https://user-images.githubusercontent.com/90395116/224135090-172c177e-98db-4692-b67f-cfc88b4dd53d.png)

## Simulated Annealing
![image](https://user-images.githubusercontent.com/90395116/224133272-1113ae39-95f9-472d-b40f-1baf53d799ad.png)
![image](https://user-images.githubusercontent.com/90395116/224133367-71b30553-9ae5-45c6-959b-1a7f4a346785.png)
<br>Pendekatan kedua yang akan kami lakukan adalah Local Search menggunakan Algoritma Simulated Annealing. Simulated Annealing (SA) merupakan suatu pendekatan algoritma untuk memecahkan masalah optimasi kombinatorial. Algoritma SA mengeluarkan Local Minimum dengan menggunakan bilangan acak dalam pemilihan perpindahan.

Graph partition yang dimiliki oleh SA kurang lebih sama dengan Hill Climbing. Algoritma Hill Climbing menunjukkan grafik yang cenderung memuncak, sehingga yang dimiliki oleh SA adalah Local Minimum dan Global Minimum alih-alih Local Maximum dan Global Maximum. Berikut ini adalah kodenya:
```python
import random
import math

# fungsi untuk menghitung jumlah queen yang saling menyerang pada papan catur
def calculate_conflicts(state):
    conflicts = 0
    for i in range(len(state)):
        for j in range(i + 1, len(state)):
            if state[i] == state[j] or abs(state[i] - state[j]) == j - i:
                conflicts += 1
    return conflicts

# fungsi untuk menghasilkan kemungkinan solusi baru dengan mengganti 
# posisi dua queen
def generate_neighbor(state):
    new_state = state.copy()
    i, j = random.sample(range(len(state)), 2)
    new_state[i], new_state[j] = new_state[j], new_state[i]
    return new_state

# fungsi untuk menentukan apakah solusi baru diterima atau tidak
def accept_solution(current_conflicts, new_conflicts, temperature):
    if new_conflicts < current_conflicts:
        return True
    delta = new_conflicts - current_conflicts
    probability = math.exp(-delta / temperature)
    return random.random() < probability

# inisialisasi posisi awal queen secara acak
start_state = [1, 3, 0, 6, 4, 7, 5, 2]
current_state = start_state

# konfigurasi parameter algoritma simulated annealing
initial_temperature = 1000
temperature_factor = 0.95
iterations_per_temperature = 100

# iterasi algoritma simulated annealing
temperature = initial_temperature
current_conflicts = calculate_conflicts(current_state)
while current_conflicts > 0 and temperature > 0.1:
    for i in range(iterations_per_temperature):
        new_state = generate_neighbor(current_state)
        new_conflicts = calculate_conflicts(new_state)
        if accept_solution(current_conflicts, new_conflicts, temperature):
            current_state = new_state
            current_conflicts = new_conflicts
    temperature *= temperature_factor

# output hasil solusi yang ditemukan
if current_conflicts == 0:
    print("posisi awal:", start_state)
    print("Solusi ditemukan:", current_state)
else:
    print("posisi awal:", start_state)
    print("Tidak ada solusi yang ditemukan.")
```
Berikut ini adalah hasilnya: <br>
![image](https://user-images.githubusercontent.com/90395116/224135676-89734a93-0497-47b1-b00a-99ca7aa69791.png)
