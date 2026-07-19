# 🏮 UPDATED 🏮 - AI Multiverse Chatbot 🚀

Welcome to the UPDATED AI Multiverse Chatbot, a stateful Streamlit application built for the Virtual Summer Internship 2026: AI Builder Track at MirAI School of Technology. 

This project upgrades a basic stateless chatbot into a fully capable conversational AI that remembers past messages and maintains its context during active sessions.

---

## 📺 Project Demonstration

HERE IS THE VIDEO DEMONSTRATION 👉👉
https://youtu.be/ZthcLfVJ_hA?si=PJk375WqP6xEtDPq. 👈👈


---

## 🛠️ What I Did In This Assignment

In this update, we systematically re-engineered the application flow to implement **Stateful UI Memory** and **API Context Tracking**:

*   **Initialized the Memory Vault:** Implemented a persistent state validator using `st.session_state` to create a dedicated data storage array that survives Streamlit's structural top-to-bottom page reruns.
*   **Upgraded the Chat Interface:** Replaced outdated static inputs with Streamlit's native `st.chat_input` loop, utilizing the Python **Walrus Operator (`:=`)** to dynamically evaluate and capture user text in a single line.
*   **Chronological UI Rendering:** Constructed a dynamic rendering loop that pulls history directly from session memory to paint past messages clearly on-screen using `st.chat_message`.
*   **Connected Full Multi-Turn Context:** Upgraded the backend connection architectures for both **Gemini 2.5 Flash** and **Cohere Command R+**. Instead of sending isolated text inputs, the app now maps and structures the entire historical dialogue timeline into a payload the APIs can read, allowing the AI to naturally recall your name and past context.

---

## 🧰 Tech Stack & Tools Used
*   **Frontend UI Framework:** Streamlit
*   **Core Logic:** Python 3.12 (with Session State management & Assignment Expressions)
*   **AI Models Architecture:** Google GenAI SDK & Cohere V2 Client
*   **Environment Management:** Python `python-dotenv`
## 📄 License

This project was created for educational purposes as part of the **MirAI School of Technology AI Builder Internship 2026**.
---
*Developed with ❤️ by Faizan for MirAI School of Technology Internship 2026.*
