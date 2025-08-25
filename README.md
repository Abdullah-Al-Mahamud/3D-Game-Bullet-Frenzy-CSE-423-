# 🎮 Bullet Frenzy

**Bullet Frenzy** is a 3D arcade-style shooter built with **Python + PyOpenGL + GLUT**.  
You’re dropped into a colorful arena where enemies chase you nonstop — survive by shooting them down while dodging attacks and avoiding wasted bullets!  

It’s a fast-paced survival challenge with arcade mechanics, cheat features, and multiple camera views.  

---

## 🚀 Features
- 🕹️ **3D gameplay** with OpenGL rendering  
- 👾 **Chasing enemies** with pulsing scale effect  
- 🔫 **Bullet mechanics** (miss too many and it’s Game Over)  
- ❤️ **Life system** (start with 5 lives)  
- 🎯 **Cheat mode** with auto-aim + lock-on vision  
- 🎥 **First-person and third-person cameras**  
- 🎨 **Colorful arena** with quadrants and grid design  

---

## 🛠️ Installation

Clone this repository:
```bash

git clone https://github.com/your-username/bullet-frenzy.git
cd bullet-frenzy

Install dependencies:

pip install PyOpenGL PyOpenGL_accelerate

**Run the game:**

python main.py

🎮 **How to Play**

🕹️ **Controls**

| Key / Mouse     | Action                                                      |
| --------------- | ----------------------------------------------------------- |
| **W**           | Move forward                                                |
| **S**           | Move backward                                               |
| **A**           | Rotate left                                                 |
| **D**           | Rotate right                                                |
| **Left Mouse**  | Fire bullet                                                 |
| **Arrow Keys**  | Move/rotate the camera                                      |
| **C**           | Toggle cheat mode (auto-aim + auto-fire)                    |
| **V**           | Toggle cheat vision (lock-on nearest enemy in first-person) |
| **Right Mouse** | Switch between 1st/3rd person (only in cheat vision)        |
| **R**           | Restart after Game Over                                     |

⚔️** Gameplay Rules**

Start with 5 lives

If an enemy touches you → lose 1 life

Lives reach 0 → Game Over

Miss 10 bullets (bullets leaving arena without a hit) → Game Over

Defeat enemies to increase your score

After each kill → a new enemy spawns

Enemies chase you relentlessly

Cheat mode lets you auto-aim & auto-fire (optional)


🏆 **Objectives**

Survive as long as possible

Rack up the highest score before dying or running out of bullets


⚡ **Future Improvements**

🔋 Power-ups (extra life, faster bullets, shields)

👹 More enemy types with unique behaviors

🏅 Scoreboard / high score system

🌐 Multiplayer mode

📜 License

This project is licensed under the MIT License — feel free to use, modify, and share.
