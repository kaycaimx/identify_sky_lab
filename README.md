# Sky Pixel Identification in Images using Traditional Computer Vision Techniques

CS5330 Spring 2024 Lab 1 - Kay (Mengxian) Cai

This Python project is a computer vision application to identify sky pixels in an image using traditional image processing techniques. Once identified, the application will replace sky pixels with The Starry Night of Vincent van Gogh. Gradio is utilized to provide a user-friendly demo where users can upload their images and see the sky detection results.

## Table of Contents

- [Requirements](#requirements)
- [Usage](#usage)
- [Demo](#demo)
- [Assumptions and Limitations](#assumptions-and-limitations)

## Requirements

```bash
gradio==4.16.0
numpy==1.25.2
opencv-python==4.9.0.80
Pillow==10.0.0
requests==2.31.0
```

## Usage

1. Run the main Python script:

   ```bash
   python gradio_demo.py
   ```

2. Open your web browser and navigate to [http://localhost:7860](http://localhost:7860).

3. Use the provided interface to upload images and see the sky detection results.

## Demo

A deployed Gradio interface is also available at [Hugging Face](https://huggingface.co/spaces/kaycaimx/5330_Lab1).

[![Gradio Demo](/images/sample.png)](http://localhost:7860)

The demo interface allows users to interactively upload images and visualize the sky detection results.

## Assumptions and Limitations

This application relies on colour thresholding and assumes the sky is clear and either in bluish or grayish colour. It has two primary limitations that it may fail to identify:

1. pixels of non-sky with similar colour: for example, distant mountains which are shown in bluish colour, especially snow mountains, and reflection of the sky in the water; and

2. pixels of sky with different colours: for example, clouds and bright objects such as sun, moon, stars, morning or sunset glow.
