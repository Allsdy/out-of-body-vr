# Near Death Experience: An Embodied Approach to Mortality (VR/WebXR)

**This is a Mixed Reality (MR) installation that simulates journey a Near-Death Experience (NDE). 

By combining physiological simulation, custom particle shaders, and spatial audio, this project explores the boundary between physical reality and digital memory. It is designed to run on **Meta Quest 2/3** via WebXR, powered by a **Python/Flask** backend for complex audio orchestration.

## 📖 Theoretical Framework

This project is not merely a visual simulation but is grounded in phenomenological research into NDEs. The narrative structure is based on **Dr. Kenneth Ring's 5-stage model**:

1.  **Peace & Separation:** The cessation of physical pain and the onset of weightlessness.
2.  **The Passage (The Tunnel):** The visual transition from the physical world to the void.
3.  **The Revelation (The Light):** Encountering hyper-vivid colors and illumination.
4.  **The Reflection (Life Review):** A panoramic, holographic relive of one's memories.
5.  **The Return:** The forced return to the physical body.

## ✨ Key Features

### 🧠 The Phenomenological Translation
We translated abstract NDE reports into specific VR sensory language:
* **Visuals:** Implemented "360-degree spherical vision" using high FOV and reflective surfaces.
* **Time:** Simulated "non-linear time" by freezing physical world animations (dust, people) while consciousness continues to move.
* **Audio:** Modeled the "Auditory Shift" by transitioning from chaotic real-world sounds to a non-directional, telepathic buzzing/ringing.

### 🛠 Technical Implementation
* **Hybrid Architecture:** * **Frontend:** WebXR (A-Frame / Three.js) for the visual experience.
    * **Backend:** Python (Flask + Pygame) for low-latency, 32-channel audio mixing that browsers cannot handle natively.
* **Custom Particle System (GLSL):**
    * Photos and videos are rendered not as flat textures but as **particle clouds**.
    * Custom shaders handle the morphing from "Flat Photos" to "Chaotic Vortex" (The Tunnel) using vertex displacement.
    * **Performance Optimization:** Implements dynamic `drawRange` manipulation to reduce particle count by 70% during high-speed transitions to maintain 60 FPS on mobile hardware.
* **Interaction Journey:**
    * **Trigger:** User initiates the experience via a simulated "Injection" gesture.
    * **Gaze-Based Focus:** "Spotlight" effect on memories triggered by looking at specific particle clusters.
    * **Return Mechanism:** An interactive CPR mechanic pulls the user back to reality.

<table>
  <tr>
    <td width="25%">
      <img src="https://github.com/user-attachments/assets/078ceb33-8247-402b-8dff-ad9dd687e950" alt="Injection" />
    </td>
    <td width="25%">
      <img src="https://github.com/user-attachments/assets/9e666b79-fe74-46d7-a509-8868a705cfae" alt="Memory" />
    </td>
    <td width="25%">
      <img src="https://github.com/user-attachments/assets/6835ee67-51dc-4d5d-9741-9f4cf2823157" alt="All@once" />
    </td>
    <td width="25%">
      <img src="https://github.com/user-attachments/assets/c7556c14-c3aa-4f72-a09a-daeac49a4163" alt="OutofBody" />
    </td>
  </tr>
</table>
 

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
```

<img width="80%" alt="OutofBody" src="https://github.com/user-attachments/assets/29533d27-faba-4151-a659-7ca7edeb308d" />





