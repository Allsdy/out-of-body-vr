# Soumatou: An Embodied Approach to Mortality (VR/WebXR)

**Soumatou** (or *The Revolving Lantern*) is a Mixed Reality (MR) installation that simulates the phenomenon of a "Life Review" experienced during a Near-Death Experience (NDE). 

By combining physiological simulation, custom particle shaders, and spatial audio, this project explores the boundary between physical reality and digital memory. It is designed to run on **Meta Quest 2/3** via WebXR, powered by a **Python/Flask** backend for complex audio orchestration.

## 📖 Theoretical Framework

This project is not merely a visual simulation but is grounded in phenomenological research into NDEs. The narrative structure is based on **Dr. [cite_start]Kenneth Ring's 5-stage model**[cite: 3, 5]:

1.  [cite_start]**Peace & Separation:** The cessation of physical pain and the onset of weightlessness[cite: 25, 26].
2.  [cite_start]**The Passage (The Tunnel):** The visual transition from the physical world to the void[cite: 8].
3.  [cite_start]**The Revelation (The Light):** Encountering hyper-vivid colors and illumination[cite: 9, 49].
4.  [cite_start]**The Reflection (Life Review):** A panoramic, holographic relive of one's memories[cite: 10, 16].
5.  [cite_start]**The Return:** The forced return to the physical body[cite: 11].

## ✨ Key Features

### 🧠 The Phenomenological Translation
[cite_start]We translated abstract NDE reports into specific VR sensory language[cite: 41]:
* **Visuals:** Implemented "360-degree spherical vision" using high FOV and reflective surfaces[cite: 43, 44].
* [cite_start]**Time:** Simulated "non-linear time" by freezing physical world animations (dust, people) while consciousness continues to move[cite: 52, 53].
* [cite_start]**Audio:** Modeled the "Auditory Shift" by transitioning from chaotic real-world sounds to a non-directional, telepathic buzzing/ringing[cite: 27, 46].

### 🛠 Technical Implementation
* **Hybrid Architecture:** * **Frontend:** WebXR (A-Frame / Three.js) for the visual experience.
    * **Backend:** Python (Flask + Pygame) for low-latency, 32-channel audio mixing that browsers cannot handle natively.
* **Custom Particle System (GLSL):**
    * Photos and videos are rendered not as flat textures but as **particle clouds**.
    * Custom shaders handle the morphing from "Flat Photos" to "Chaotic Vortex" (The Tunnel) using vertex displacement.
    * **Performance Optimization:** Implements dynamic `drawRange` manipulation to reduce particle count by 70% during high-speed transitions to maintain 60 FPS on mobile hardware.
* **Interaction Loop:**
    * **Trigger:** User initiates the experience via a simulated "Injection" gesture[cite: 36].
    * **Gaze-Based Focus:** "Spotlight" effect on memories triggered by looking at specific particle clusters.
    * **Return Mechanism:** An interactive CPR mechanic pulls the user back to reality[cite: 38].

## 📦 Tech Stack

* **Frontend:** HTML5, JavaScript, A-Frame (WebXR), Three.js, GLSL (Shaders)
* **Backend:** Python 3.x, Flask, Pygame (Mixer)
* **Hardware:** Meta Quest 2 or 3 (Passthrough API required for AR stage)

## 📂 Project Structure

```text
├── app.py                 # Flask server & Pygame audio engine
├── templates
│   └── index.html         # Main WebXR application (A-Frame & Three.js logic)
├── static
│   ├── img                # Memory photos (1.jpg - 10.jpg)
│   ├── mem                # Voice-over audio files (1.mp3 - 10.mp3)
│   ├── doctor.glb         # 3D assets
│   ├── injection.mp4      # Particle video source
│   ├── *.mp3              # SFX (heartbeat, flatline, footstep, etc.)
└── README.md
