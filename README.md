https://github.com/user-attachments/assets/c04c43d8-b3db-414f-8418-bc19e8e3db0f




Zero‑Shot Colour Attribution with Multilingual Text Embeddings

Project status : proof‑of‑concept – stable API, research ongoing

TL;DR

Given any word or short phrase in more than 50 languages, the service returns the most likely basic colour term (“red”, “green”, …).No (object → colour) training pairs are required: the classifier exploits the semantic structure of a pre‑trained language model and a tiny set of colour tokens.The task is therefore zero‑shot with respect to the classification labels.
![photo_2024-06-05_09-52-37ыаыа](https://github.com/user-attachments/assets/b16b2267-4402-44e4-9e50-042723019b9d)

Why this repo might interest you

Engineering demo – full end‑to‑end pipeline: data → embeddings → ANN index → API.

Multilingual – works with any language supported by the encoder (tested on 50+).

Lightweight – ≤ 100 MB index, single‑GPU optional, CPU‑only fine for demo.

Reproducible – deterministic build via Docker / Poetry, unit & integration tests, CI.

Extensible – plug‑in architecture: swap encoder, index, or distance learner with a few lines.




**How to run the program**


The program is launched from the interface_main script. Training is started using the > button.

**Buttons**

o+ - add a new node. For correct operation, you need to add the openai key to the get_embedding.py module

o- - delete node

/+ - add edge

/- - delete edge

'>' start training

// - connect node with all others

-- - disconnect node from all others

dtt - connect all nodes with all others
