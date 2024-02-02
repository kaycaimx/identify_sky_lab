import gradio as gr
from identify_sky import identify_sky_pixels

def main():
  demo = gr.Interface(identify_sky_pixels, gr.Image(), "image")
  demo.launch()

if __name__ == "__main__":
  main()

