import os

base_dir = r"C:\Users\ASMIT PANDEY\.gemini\antigravity\scratch\cropdrop\frontend"

postcss_content = """export default {
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
  },
}
"""

with open(os.path.join(base_dir, "postcss.config.js"), 'w', encoding='utf-8') as f:
    f.write(postcss_content)
