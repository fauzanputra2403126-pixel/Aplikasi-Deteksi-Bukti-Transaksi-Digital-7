import numpy as np

def compute_forensic_hamming(vector_x, vector_y, edge_noise_ratio, similarity_threshold=88.0, max_noise_threshold=6.5):
    """
    Menghitung Operasi XOR, Hamming Weight, Hamming Distance, 
    dan menetapkan vonis keaslian berbasis Dual-Indikator:
    1. Kemiripan Biner Piksel (Similarity Ratio >= 88.0%)
    2. Kerapatan Derau Tepi Manipulasi (Edge Noise Ratio <= 6.5%)
    """
    n = len(vector_x)
    if len(vector_y) != n:
        raise ValueError("Dimensi vektor biner acuan dan uji tidak sepadan!")
        
    # 1. Operasi Bitwise XOR: e = x XOR y
    error_vector = np.bitwise_xor(vector_x, vector_y)
    
    # 2. Hitung Hamming Weight wt(e) & Hamming Distance d(x,y)
    hamming_weight = int(np.sum(error_vector))
    hamming_distance = int(np.count_nonzero(vector_x != vector_y))
    
    # 3. Hitung Persentase Kemiripan Biner Piksel
    similarity_ratio = (1.0 - (hamming_distance / n)) * 100.0
    bit_change_ratio = (hamming_distance / n) * 100.0
    
    # 4. Verifikasi Teorema: d(x,y) == wt(e)
    is_verified = (hamming_distance == hamming_weight)
    
    # 5. KONDISI FORENSIK GANDA (Dual-Condition Verification):
    # A. Kemiripan Biner Piksel HARUS >= 88.0%
    # B. Kerapatan Derau Tepi Manipulasi HARUS <= 6.5% (Tidak terdeteksi artefak editan HP/Photoshop)
    
    is_shape_valid = (similarity_ratio >= similarity_threshold)
    is_noise_clean = (edge_noise_ratio <= max_noise_threshold)
    
    if is_shape_valid and is_noise_clean:
        verdict = "VALID_ASLI"
        title_output = "🟢 BUKTI TRANSAKSI INI ASLI"
        description = (
            f"Dokumen terverifikasi 100% VALID & ASLI. Kemiripan biner piksel mencapai {similarity_ratio:.2f}% "
            f"dan tingkat derau tepi biner sangat rendah ({edge_noise_ratio:.2f}%). "
            f"Bebas dari artefak manipulasi citra."
        )
    else:
        verdict = "MANIPULASI_PALSU"
        title_output = "🔴 BUKTI TRANSAKSI INI PALSU"
        
        reasons = []
        if not is_shape_valid:
            reasons.append(f"Ketidakcocokan biner nominal (Kemiripan = {similarity_ratio:.2f}% < {similarity_threshold}%)")
        if not is_noise_clean:
            reasons.append(f"Terdeteksi artefak derau tepi editan (Edge Noise = {edge_noise_ratio:.2f}% > {max_noise_threshold}%)")
            
        description = "TERINDIKASI MANIPULASI / PALSU! Alasan: " + " & ".join(reasons) + "."

    return {
        'total_bits': n,
        'hamming_distance': hamming_distance,
        'hamming_weight': hamming_weight,
        'similarity_ratio': similarity_ratio,
        'edge_noise_ratio': edge_noise_ratio,
        'bit_change_ratio': bit_change_ratio,
        'is_verified': is_verified,
        'verdict': verdict,
        'title_output': title_output,
        'description': description
    }
