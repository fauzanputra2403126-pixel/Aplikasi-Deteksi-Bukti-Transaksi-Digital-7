import numpy as np
from PIL import Image, ImageOps, ImageFilter

def extract_roi_and_binarize(uploaded_image, target_size=(280, 80)):
    """
    1. Isolasi ROI Teks & Auto-Centering
    2. Binarisasi Piksel (0 & 1)
    3. Ekstraksi Kerapatan Derau Tepi (Tampering Edge Noise Density)
    """
    # A. Buka Gambar Uji & Convert Grayscale
    raw_img = Image.open(uploaded_image).convert('L')
    contrast_img = ImageOps.autocontrast(raw_img)
    
    # B. Binarisasi Thresholding
    np_img = np.array(contrast_img)
    mean_val = np.mean(np_img)
    threshold = int(mean_val * 0.85)
    
    binary_np = np.where(np_img < threshold, 0, 255).astype(np.uint8)
    binary_pil = Image.fromarray(binary_np)
    
    # C. Cari Bounding Box Teks Nominal & Crop
    inverted = ImageOps.invert(binary_pil)
    bbox = inverted.getbbox()
    
    if bbox:
        cropped_text = binary_pil.crop(bbox)
    else:
        cropped_text = binary_pil
        
    # D. Fitting & Centering ke Kanvas Target (280x80 px)
    canvas = Image.new('L', target_size, color=255)
    cw, ch = cropped_text.size
    tw, th = target_size
    
    scale = min((tw - 20) / max(cw, 1), (th - 20) / max(ch, 1), 1.0)
    new_w = max(int(cw * scale), 1)
    new_h = max(int(ch * scale), 1)
    
    resized_text = cropped_text.resize((new_w, new_h), Image.Resampling.LANCZOS)
    
    paste_x = (tw - new_w) // 2
    paste_y = (th - new_h) // 2
    canvas.paste(resized_text, (paste_x, paste_y))
    
    # E. Konversi Kanvas ROI ke Vektor Biner (Bit 1 = Teks, Bit 0 = Latar)
    np_canvas = np.array(canvas)
    binary_matrix = np.where(np_canvas < 128, 1, 0).astype(np.uint8)
    binary_vector = binary_matrix.flatten()
    
    # F. Deteksi Derau Tepi Manipulasi (Tampering Edge Noise Analysis)
    edge_img = canvas.filter(ImageFilter.FIND_EDGES)
    np_edge = np.array(edge_img)
    edge_noise_pixels = np.count_nonzero(np_edge > 100)
    edge_noise_ratio = (edge_noise_pixels / (tw * th)) * 100.0
    
    return canvas, binary_vector, edge_noise_ratio

def convert_template_to_vector(template_pil_image):
    """Mengonversi Gambar Acuan Backend (x) ke Vektor Biner 1D."""
    np_canvas = np.array(template_pil_image)
    binary_matrix = np.where(np_canvas < 128, 1, 0).astype(np.uint8)
    return binary_matrix.flatten()