# Fastchat

This is a fork of [lm-sys/FastChat](https://github.com/lm-sys/FastChat), a handy tool for locally running Large Language Models. Into the inference I've hacked internet access. This was not intended for real use, but as a tech demo that was slapped together on a wednesday night.

Changes compared to the original repo:

- Vicuna model system prompt specifies how to use the internet
- inference.py chat_loop is heavily modified to interupt excecution and fetch internet information
- find_website.py was added for retrieving information from web.

Start guide and more can be found in FASTCHAT_README.md
