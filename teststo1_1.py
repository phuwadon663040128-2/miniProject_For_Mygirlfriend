import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import binom, chi2, t

# -- Mini Project: EN813001 Stochastic Processes and Modeling --
# Student ID: 663040117-7
# No.: 15

# --- 1. การคำนวณพารามิเตอร์เริ่มต้น ---
print("--- 1. การคำนวณพารามิเตอร์เริ่มต้น ---")

# กำหนดค่าจากรหัสนักศึกษา
student_id = '6630401177'
y1 = int(student_id[-3:])  # ตัวเลข 3 หลักสุดท้าย
print(f"รหัสนักศึกษา: {student_id}")
print(f"ค่า y1 ที่ได้คือ: {y1}")

# คำนวณค่าเริ่มต้น x0 (สำหรับกลุ่ม 1 คน)
x0 = y1
print(f"ค่าเริ่มต้น x0: {x0}")

# คำนวณค่าในลำดับ x1 และ x2 ตามสมการ x_{i+1} = ((112*x_i) mod 111) + 2
x1 = ((112 * x0) % 111) + 2
x2 = ((112 * x1) % 111) + 2
print(f"ค่า x1: {x1}")
print(f"ค่า x2: {x2}\n")


# --- 2. การจำลองแบบ (Simulation) ---
print("--- 2. การจำลองแบบ (Simulation) ---")
# กำหนดค่าพารามิเตอร์พื้นฐานสำหรับการจำลอง
N = 10         # จำนวนครั้งในการทดลอง (Number of trials)
n_samples = 10000 # ขนาดของตัวอย่าง (Sample size)

# กำหนด seed สำหรับการทำซ้ำได้ (เฉพาะตัวตามรหัสนักศึกษา)
base_seed = (int(student_id) * 97 + 7919 * 15 + 73) % (2**32)
seed1 = base_seed  # seed สำหรับ Run 1             
seed2 = base_seed + 1  # seed สำหรับ Run 2

# 2.2. การจำลองครั้งที่ 1 (คำถามข้อ 2)
# คำนวณค่าความน่าจะเป็น p ใหม่
p = 0.31 + (x2 / 1000)
print(f"คำถามข้อ 2: ค่าความน่าจะเป็น p ที่ใช้คือ {p:.3f}")

# สร้างข้อมูลสุ่ม X จากการแจกแจงทวินาม (ใช้ seed1)
np.random.seed(seed1)
X1 = np.random.binomial(N, p, n_samples)

# คำนวณค่าทางสถิติ
M_n1 = np.mean(X1)
p_n1 = M_n1 / N
print(f"  - ค่าเฉลี่ยของกลุ่มตัวอย่าง (M_n) ครั้งที่ 1: {M_n1:.4f}")
print(f"  - ค่าความน่าจะเป็นที่ประมาณได้ (p_n) ครั้งที่ 1: {p_n1:.4f}")

# กำหนดขอบ bin เดียวกันสำหรับทั้ง 2 รัน (เฉพาะ 0..N เท่านั้น)
common_bins = np.arange(-0.5, N + 1, 1)

# สร้าง Histogram ครั้งที่ 1
plt.figure(1, figsize=(15, 6))

plt.subplot(1, 2, 1)
counts1, bins_edges, patches = plt.hist(X1, bins=common_bins, density=True, 
                                       edgecolor='black', rwidth=0.8, alpha=0.7)
# วาด PMF ทับ
k_range = np.arange(0, N + 1)
pmf_theoretical = binom.pmf(k_range, N, p)
plt.plot(k_range, pmf_theoretical, 'ro-', label=f'Theoretical PMF (p={p:.3f})', markersize=6)
plt.title(f"Simulation 1 - Density Histogram")
plt.xlabel("Number of Successes")
plt.ylabel("Density")
plt.xticks(range(N + 1))
plt.legend()
plt.grid(axis='y', alpha=0.75)
# 2.3. การจำลองครั้งที่ 2 (คำถามข้อ 3)
print("\nคำถามข้อ 3: ทำการรันโปรแกรมอีกครั้งด้วยค่า p เดิม")
# สร้างข้อมูลสุ่มชุดใหม่ (ใช้ seed2)
np.random.seed(seed2)
X2 = np.random.binomial(N, p, n_samples)

# คำนวณค่าทางสถิติ
M_n2 = np.mean(X2)
p_n2 = M_n2 / N
print(f"  - ค่าเฉลี่ยของกลุ่มตัวอย่าง (M_n) ครั้งที่ 2: {M_n2:.4f}")
print(f"  - ค่าความน่าจะเป็นที่ประมาณได้ (p_n) ครั้งที่ 2: {p_n2:.4f}")

# สร้าง Histogram ครั้งที่ 2
plt.subplot(1, 2, 2)
counts2, bins_edges, patches = plt.hist(X2, bins=common_bins, density=True, 
                                       edgecolor='blue', rwidth=0.8, color='skyblue', alpha=0.7)
# วาด PMF ทับ
plt.plot(k_range, pmf_theoretical, 'ro-', label=f'Theoretical PMF (p={p:.3f})', markersize=6)
plt.title(f"Simulation 2 - Density Histogram")
plt.xlabel("Number of Successes")
plt.ylabel("Density")
plt.xticks(range(N + 1))
plt.legend()
plt.grid(axis='y', alpha=0.75)
plt.tight_layout()

# 2.4. เปรียบเทียบผล (คำถามข้อ 4)
print("\nคำถามข้อ 4: เปรียบเทียบผลจากการทดลอง 2 ครั้ง")

# คำนวณ empirical pmf โดยตรง (แนะนำให้ใช้วิธีนี้)
emp_prob1 = np.bincount(X1, minlength=N+1) / n_samples
emp_prob2 = np.bincount(X2, minlength=N+1) / n_samples

# L1 distance บน empirical pmf
l1_distance = np.sum(np.abs(emp_prob1 - emp_prob2))
print(f"  - L1 Distance ระหว่าง empirical pmf ของสองรัน: {l1_distance:.6f}")

# เปรียบเทียบค่าเฉลี่ย
mean_diff = abs(M_n1 - M_n2)
print(f"  - ความแตกต่างของค่าเฉลี่ย: |{M_n1:.4f} - {M_n2:.4f}| = {mean_diff:.4f}")

# เปรียบเทียบค่า p ที่ประมาณได้
p_diff = abs(p_n1 - p_n2)
print(f"  - ความแตกต่างของ p ที่ประมาณได้: |{p_n1:.4f} - {p_n2:.4f}| = {p_diff:.4f}")

print("  - สรุป:")
print("    • ผลลัพธ์ที่ได้จากการรัน 2 ครั้งมีความใกล้เคียงกัน แต่ไม่เท่ากันเป๊ะ")
print("    • ค่าเฉลี่ยและการกระจายแตกต่างกันเล็กน้อยตามธรรมชาติของการสุ่ม (Sampling Variability)")
print("    • L1 distance (empirical pmf) เป็นตัวชี้วัดความต่างของการกระจายที่ตรงไปตรงมาที่สุด")


# --- 3. การตรวจสอบด้วย Chi-Squared Test ---
print("\n--- 3. การตรวจสอบด้วย Chi-Squared Test (Goodness of Fit) ---")
# ใช้ข้อมูลจากการจำลองครั้งที่ 1 (X1)
alpha = 0.05 # ระดับนัยสำคัญ

# 3.1. คำนวณค่าสถิติ Z (Chi-Squared statistic) with pooling (คำถามข้อ 5)
# H คือความถี่ที่สังเกตได้ (Observed Frequencies)
H, _ = np.histogram(X1, bins=np.arange(N + 2) - 0.5)

# p_j คือความน่าจะเป็นที่คาดหวัง (Expected Probabilities) จาก PMF ของ Binomial(N, p)
# ใช้ p (theoretical) แทน p_n1 เพื่อทดสอบกับการแจกแจงที่แท้จริง
k = np.arange(0, N + 1)
pmf = binom.pmf(k, N, p)  # ใช้ p ตามทฤษฎี
np_j = n_samples * pmf  # Expected frequencies

print(f"  - ทดสอบกับ Binomial(N={N}, p={p:.3f}) theoretical distribution")

print("  - ความถี่ก่อน pooling:")
for i in range(len(H)):
    print(f"    k={i}: Observed={H[i]}, Expected={np_j[i]:.2f}")

# Pooling: รวมหมวดหมู่ที่มี expected frequency < 5
min_expected = 5  # ค่ามาตรฐานสำหรับ Chi-squared test
H_pooled = []
np_j_pooled = []
categories = []

print(f"  - เกณฑ์การ pooling: expected frequency ≥ {min_expected}")

i = 0
while i < len(H):
    if np_j[i] >= min_expected:
        # ไม่ต้อง pool
        H_pooled.append(H[i])
        np_j_pooled.append(np_j[i])
        categories.append(f"{i}")
        i += 1
    else:
        # Pool หมวดหมู่ที่ติดกัน
        pooled_H = H[i]
        pooled_np_j = np_j[i]
        start_cat = i
        i += 1
        
        # รวมหมวดหมู่ติดกันจนกว่า expected frequency >= min_expected
        while i < len(H) and pooled_np_j < min_expected:
            pooled_H += H[i]
            pooled_np_j += np_j[i]
            i += 1
        
        H_pooled.append(pooled_H)
        np_j_pooled.append(pooled_np_j)
        if i-1 == start_cat:
            categories.append(f"{start_cat}")
        else:
            categories.append(f"{start_cat}-{i-1}")

H_pooled = np.array(H_pooled)
np_j_pooled = np.array(np_j_pooled)

print("\n  - ความถี่หลัง pooling:")
for i, cat in enumerate(categories):
    print(f"    k={cat}: Observed={H_pooled[i]}, Expected={np_j_pooled[i]:.2f}")

# คำนวณค่าสถิติ Z หลัง pooling
Z = np.sum((H_pooled - np_j_pooled)**2 / np_j_pooled)
print(f"\nคำถามข้อ 5: ค่าสถิติ Z (Chi-Squared) หลัง pooling: {Z:.4f}")

# คำนวณ Effect Size (Cramér's V)
cramers_v = np.sqrt(Z / (n_samples * (len(H_pooled) - 1)))
print(f"  - Effect Size (Cramér's V): {cramers_v:.4f}")

# แปลผล Effect Size
if cramers_v < 0.1:
    effect_interpretation = "negligible (ไม่มีผลเชิงปฏิบัติ)"
elif cramers_v < 0.3:
    effect_interpretation = "small (ผลขนาดเล็ก)"
elif cramers_v < 0.5:
    effect_interpretation = "medium (ผลขนาดกลาง)"
else:
    effect_interpretation = "large (ผลขนาดใหญ่)"

print(f"  - การแปลผล Effect Size: {effect_interpretation}")
print("    📌 Cramér's V วัดขนาดของความแตกต่างระหว่างข้อมูลสังเกตและทฤษฎี")

# 3.2. วิเคราะห์ผลและองศาอิสระ (คำถามข้อ 6)
k_bins_pooled = len(H_pooled)  # จำนวนหมวดหมู่หลัง pooling
m = 1  # จำนวนพารามิเตอร์ที่ประมาณค่าจากข้อมูล (คือ p_n)
df = max(k_bins_pooled - 1 - m, 1)  # องศาอิสระ (ป้องกัน extreme case)

print(f"คำถามข้อ 6: การวิเคราะห์ผล")
print(f"  - จำนวนหมวดหมู่หลัง pooling: {k_bins_pooled}")
print(f"  - Degrees of Freedom (df) = (k - 1 - m) = {k_bins_pooled} - 1 - {m} = {df}")

# หาค่าวิกฤต (critical value) และ p-value
z_alpha = chi2.ppf(1 - alpha, df)
p_value = 1 - chi2.cdf(Z, df)

print(f"  - ค่าวิกฤต (z_alpha) ที่ระดับนัยสำคัญ {alpha*100}% คือ: {z_alpha:.4f}")
print(f"  - p-value: {p_value:.6f}")

# สรุปผลการทดสอบ
print("  - สรุปผล:")
if Z < z_alpha:
    print(f"    เนื่องจาก Z ({Z:.4f}) < z_alpha ({z_alpha:.4f}) และ p-value ({p_value:.6f}) > α ({alpha})")
    print("    เราจึงไม่ปฏิเสธสมมติฐานหลัก (H₀)")
    print("    ดังนั้น การแจกแจง Binomial(N, p) ถือว่าเป็น 'a good fit' สำหรับข้อมูลชุดนี้")
    print("    📊 ความหมาย: ข้อมูลที่เราสังเกตไม่แตกต่างจากการแจกแจงทวินามอย่างมีนัยสำคัญ")
    print("    📈 การจำลองของเราสอดคล้องกับทฤษฎี")
else:
    print(f"    เนื่องจาก Z ({Z:.4f}) >= z_alpha ({z_alpha:.4f}) และ p-value ({p_value:.6f}) <= α ({alpha})")
    print("    เราจึงปฏิเสธสมมติฐานหลัก (H₀)")
    print("    ดังนั้น การแจกแจง Binomial(N, p) 'ไม่เป็น a good fit' สำหรับข้อมูลชุดนี้")
    print("    📊 ความหมาย: ข้อมูลที่เราสังเกตแตกต่างจากการแจกแจงทวินามอย่างมีนัยสำคัญ")
    print("    📉 อาจมีปัจจัยอื่นที่ส่งผลต่อการจำลอง")


# --- 4. ช่วงความเชื่อมั่นสำหรับค่าเฉลี่ย ---
print("\n--- 4. ช่วงความเชื่อมั่นสำหรับค่าเฉลี่ย (Confidence Interval for the Mean) ---")
# ใช้ข้อมูลจากการจำลองครั้งที่ 1 (X1)

# 4.1. คำนวณค่าเบี่ยงเบนมาตรฐานของกลุ่มตัวอย่าง (Sn) (คำถามข้อ 7)
S_n = np.std(X1, ddof=1) # ddof=1 เพื่อให้เป็นการประมาณค่าที่ไม่เอนเอียง
print(f"คำถามข้อ 7: ค่าเบี่ยงเบนมาตรฐานของกลุ่มตัวอย่าง (S_n): {S_n:.4f}")

# 4.2. หาช่วงความเชื่อมั่น (คำถามข้อ 8)
df_t = n_samples - 1
# หาค่าวิกฤต y_alpha/2 จาก t-distribution
y_alpha_2 = t.ppf(1 - alpha / 2, df=df_t)
print(f"คำถามข้อ 8: การหาช่วงความเชื่อมั่น 95%")
print(f"  - ค่าวิกฤต y_alpha/2 (จาก t-distribution ที่ df={df_t}) คือ: {y_alpha_2:.4f}")

# คำนวณ Margin of Error
margin_of_error = y_alpha_2 * (S_n / np.sqrt(n_samples))
# คำนวณช่วงความเชื่อมั่น
ci_lower = M_n1 - margin_of_error
ci_upper = M_n1 + margin_of_error

print(f"  - ช่วงความเชื่อมั่น 95% สำหรับค่าเฉลี่ยของประชากรคือ: ({ci_lower:.4f}, {ci_upper:.4f})")

# อภิปรายผล
theoretical_mean = N * p
print("  - อภิปรายผล:")
print("    📊 ความหมายของ Confidence Interval:")
print("    • หากเราทำการทดลองแบบเดียวกัน 100 ครั้ง")
print("    • ประมาณ 95 ครั้ง จะได้ช่วงความเชื่อมั่นที่ครอบคลุมค่าเฉลี่ยที่แท้จริง")
print(f"    • ช่วงกว้าง = {ci_upper - ci_lower:.4f}, แสดงความแม่นยำของการประมาณ")

if ci_lower <= theoretical_mean <= ci_upper:
    print(f"    ✅ ช่วงความเชื่อมั่นครอบคลุมค่าเฉลี่ยตามทฤษฎี (μ = N×p = {theoretical_mean:.4f})")
    print("    📈 นี่เป็นสัญญาณที่ดีว่าการจำลองของเราถูกต้อง")
else:
    print(f"    ❌ ช่วงความเชื่อมั่นไม่ครอบคลุมค่าเฉลี่ยตามทฤษฎี (μ = N×p = {theoretical_mean:.4f})")
    print("    📉 อาจจำเป็นต้องตรวจสอบการจำลองหรือเพิ่มขนาดตัวอย่าง")

# --- 4.3. Bootstrap Confidence Interval (เปรียบเทียบ) ---
print("\n  📊 เพิ่มเติม: Bootstrap Confidence Interval (95%)")
print("    (เปรียบเทียบกับ t-based CI)")

# Bootstrap sampling
n_bootstrap = 1000
np.random.seed(seed1)  # ใช้ seed เดียวกันเพื่อ reproducibility
bootstrap_means = []

for _ in range(n_bootstrap):
    # สุ่มตัวอย่างจาก X1 (with replacement)
    bootstrap_sample = np.random.choice(X1, size=len(X1), replace=True)
    bootstrap_means.append(np.mean(bootstrap_sample))

bootstrap_means = np.array(bootstrap_means)

# คำนวณช่วงความเชื่อมั่น Bootstrap (percentile method)
bootstrap_ci_lower = np.percentile(bootstrap_means, 2.5)
bootstrap_ci_upper = np.percentile(bootstrap_means, 97.5)

print(f"    • Bootstrap CI (95%): ({bootstrap_ci_lower:.4f}, {bootstrap_ci_upper:.4f})")
print(f"    • t-based CI (95%):   ({ci_lower:.4f}, {ci_upper:.4f})")

# เปรียบเทียบ
bootstrap_width = bootstrap_ci_upper - bootstrap_ci_lower
t_width = ci_upper - ci_lower
print(f"    • ความกว้างของช่วง: Bootstrap = {bootstrap_width:.4f}, t-based = {t_width:.4f}")

if abs(bootstrap_width - t_width) < 0.01:
    print("    📊 ช่วงความเชื่อมั่นทั้งสองวิธีใกล้เคียงกัน → การกระจายใกล้ normal")
else:
    print("    📊 ช่วงความเชื่อมั่นแตกต่างกัน → อาจต้องพิจารณา distribution shape")

# เพิ่มกราฟเปรียบเทียบ PMF และ Empirical Distribution
plt.figure(2, figsize=(12, 8))
x_pos = np.arange(N + 1)

plt.plot(x_pos, pmf_theoretical, 'ro-', label='Theoretical PMF', markersize=8, linewidth=2)
plt.plot(x_pos, emp_prob1, 'bs-', label='Empirical Run 1', markersize=6, alpha=0.7)
plt.plot(x_pos, emp_prob2, 'g^-', label='Empirical Run 2', markersize=6, alpha=0.7)

plt.title('Comparison: Theoretical PMF vs Empirical Distributions')
plt.xlabel('Number of Successes (k)')
plt.ylabel('Probability')
plt.xticks(range(N + 1))
plt.legend()
plt.grid(True, alpha=0.3)

# แสดงผลกราฟทั้งหมด
plt.tight_layout()
plt.show()

