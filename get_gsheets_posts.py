#!/usr/bin/env python3
import os

print("===== get posts from gsheet ===")
print(os.environ["GSPREAD_TYPE"])


filename = "2021-05-15-hallo.markdown"
f = open(f"_posts/{filename}", "w")
f.write('''---
layout: post
title:  "Welcome to Jekyll!"
---

# Welcome Mens

**Hello world**, this is my first Jekyll blog post.

I hope you like it!
''')
f.close()
