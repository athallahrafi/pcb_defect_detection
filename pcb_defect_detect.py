import cv2
import numpy as np
import matplotlib.pyplot as plt

# ==========================================
# BAGIAN 2: FUNGSI PENYAMAAN POSISI (REGISTRATION)
# ==========================================
def align_images(img_test, img_ref):
    # Ubah ke grayscale
    gray_test = cv2.cvtColor(img_test, cv2.COLOR_BGR2GRAY)
    gray_ref = cv2.cvtColor(img_ref, cv2.COLOR_BGR2GRAY)
    
    # Deteksi fitur menggunakan ORB (gratis, tidak berbayar seperti SIFT)
    orb = cv2.ORB_create(500)
    kp1, des1 = orb.detectAndCompute(gray_test, None)
    kp2, des2 = orb.detectAndCompute(gray_ref, None)
    
    # Mencocokkan fitur
    matcher = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    matches = matcher.match(des1, des2)
    matches = sorted(matches, key=lambda x: x.distance)
    
    # Ambil top 15% kecocokan terbaik
    good_matches = matches[:int(len(matches) * 0.15)]
    
    # Ekstrak lokasi titik
    src_pts = np.float32([kp1[m.queryIdx].pt for m in good_matches]).reshape(-1, 1, 2)
    dst_pts = np.float32([kp2[m.trainIdx].pt for m in good_matches]).reshape(-1, 1, 2)
    
    # Cari matriks Homography
    H, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)
    
    # Lakukan Warp (Transformasi Geometri) agar posisi sama persis
    height, width, channels = img_ref.shape
    aligned_img = cv2.warpPerspective(img_test, H, (width, height))
    
    return aligned_img

# ==========================================
# BAGIAN 3: PIPELINE UTAMA (SESUAI FLOWCHART)
# ==========================================

# 1. INPUT CITRA
img_ref = cv2.imread('PCB_DATASET/PCB_USED/01.jpg')
# img_test = cv2.imread('PCB_DATASET/PCB_USED/01.jpg')
# img_test = cv2.imread('PCB_DATASET/rotation/Open_circuit_rotation/01_open_circuit_01.jpg') #Rorated image
img_test = cv2.imread('PCB_DATASET/images/Open_circuit/01_open_circuit_01.jpg')

# 2. IMAGE REGISTRATION (Penyamaan Posisi)
# Sesuai flowchart, sebelum diproses/dikurangi, posisi harus sama
img_test_aligned = align_images(img_test, img_ref)

# 3. PREPROCESSING (Grayscale & Gaussian Blur)
gray_ref = cv2.cvtColor(img_ref, cv2.COLOR_BGR2GRAY)
gray_test = cv2.cvtColor(img_test_aligned, cv2.COLOR_BGR2GRAY)

gray_ref = cv2.GaussianBlur(gray_ref, (5, 5), 0)
gray_test = cv2.GaussianBlur(gray_test, (5, 5), 0)

# 4. OPERASI PENGURANGAN (SUBTRACTION)
# Menghitung selisih absolut: |Ref - Uji|
diff_img = cv2.absdiff(gray_ref, gray_test)

# 5. THRESHOLDING (Citra Biner)
# Jika selisih > 30, jadikan putih (255), sisanya hitam (0)
_, thresh_img = cv2.threshold(diff_img, 30, 255, cv2.THRESH_BINARY)

# 6. FILTER MORFOLOGI OPENING
# Menghapus noise bintik putih kecil
kernel = np.ones((3,3), np.uint8)
opening_img = cv2.morphologyEx(thresh_img, cv2.MORPH_OPEN, kernel, iterations=1)

# 7. HITUNG AREA PUTIH (DEFECT)
defect_area = cv2.countNonZero(opening_img)

# 8. KEPUTUSAN (DECISION)
status = ""
color_status = (0, 255, 0) # Hijau jika OK

if defect_area > 0: # Threshold toleransi (bisa diubah, misal > 10 piksel)
    status = f"REJECT (Defect Area: {defect_area} px)"
    color_status = (255, 0, 0) # Merah jika Reject
    print("LOGIKA: Area > 0 -> YA -> PCB Defect / Reject")
else:
    status = "PASS / OK"
    print("LOGIKA: Area = 0 -> TIDAK -> PCB OK")

# ==========================================
# VISUALISASI HASIL
# ==========================================
plt.figure(figsize=(15, 8))

# titles = [ '4. Difference (Pengurangan)']
# images = [diff_img, thresh_img]
titles = ['1. Referensi (Golden)', '2. Uji (Sebelum Align)', '3. Uji (Setelah Align)', 
          '4. Difference (Pengurangan)', '5. Threshold', '6. Morfologi (Final Result)']
images = [img_ref, img_test, img_test_aligned, 
          diff_img, thresh_img, opening_img]

for i in range(6):
    plt.subplot(2, 3, i+1)
    if i < 3:
        plt.imshow(cv2.cvtColor(images[i], cv2.COLOR_BGR2RGB))
    else:
        plt.imshow(images[i], cmap='gray')
    plt.title(titles[i])
    plt.axis('off')

plt.suptitle(f"Hasil Inspeksi: {status}", fontsize=20, color='blue', fontweight='bold')
plt.tight_layout()
plt.show()