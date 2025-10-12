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

# กำหนด seed สำหรับการทำซ้ำได้
seed1 = int(student_id[-3:]) + 1  # seed สำหรับ Run 1             
seed2 = int(student_id[-3:]) + 2  # seed สำหรับ Run 2

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

# สร้าง Histogram
plt.figure(1)
min_val1 = X1.min()
max_val1 = X1.max()
bins1 = np.arange(min_val1 - 0.5, max_val1 + 1.5, 1)
plt.hist(X1, bins=bins1, edgecolor='black', rwidth=0.8)
plt.title(f"Histogram of Simulation 1 (p={p:.3f})")         
plt.xlabel("Number of Successes")
plt.ylabel("Frequency")
plt.xticks(range(N + 1))
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

# สร้าง Histogram
plt.figure(2)
min_val2 = X2.min()
max_val2 = X2.max()
bins2 = np.arange(min_val2 - 0.5, max_val2 + 1.5, 1)
plt.hist(X2, bins=bins2, edgecolor='blue', rwidth=0.8, color='skyblue')
plt.title(f"Histogram of Simulation 2 (p={p:.3f})")
plt.xlabel("Number of Successes")
plt.ylabel("Frequency")
plt.xticks(range(N + 1))
plt.grid(axis='y', alpha=0.75)

# 2.4. เปรียบเทียบผล (คำถามข้อ 4)
print("\nคำถามข้อ 4: เปรียบเทียบผลจากการทดลอง 2 ครั้ง")
print("  - ผลลัพธ์ที่ได้จากการรัน 2 ครั้งมีความใกล้เคียงกัน แต่ไม่เท่ากันเป๊ะ")
print("  - ค่าเฉลี่ยและฮิสโทแกรมแตกต่างกันเล็กน้อยเนื่องจากธรรมชาติของการสุ่ม (Sampling Variability)")


# --- 3. การตรวจสอบด้วย Chi-Squared Test ---
print("\n--- 3. การตรวจสอบด้วย Chi-Squared Test (Goodness of Fit) ---")
# ใช้ข้อมูลจากการจำลองครั้งที่ 1 (X1)
alpha = 0.05 # ระดับนัยสำคัญ

# 3.1. คำนวณค่าสถิติ Z (Chi-Squared statistic) (คำถามข้อ 5)
# H คือความถี่ที่สังเกตได้ (Observed Frequencies)
H, _ = np.histogram(X1, bins=np.arange(N + 2) - 0.5)

# p_j คือความน่าจะเป็นที่คาดหวัง (Expected Probabilities) จาก PMF ของ Binomial(N, p_n1)
k = np.arange(0, N + 1)
pmf = binom.pmf(k, N, p_n1)

# คำนวณค่าสถิติ Z
# np_j คือความถี่ที่คาดหวัง (Expected Frequencies)
np_j = n_samples * pmf
# หลีกเลี่ยงการหารด้วยศูนย์ หากมีความถี่คาดหวังเป็น 0
Z = np.sum(np.divide((H - np_j)**2, np_j, out=np.zeros_like(H, dtype=float), where=np_j!=0))

print(f"คำถามข้อ 5: ค่าสถิติ Z (Chi-Squared) ที่คำนวณได้คือ: {Z:.4f}")

# 3.2. วิเคราะห์ผลและองศาอิสระ (คำถามข้อ 6)
# k_bins คือจำนวนช่อง (categories) ที่เป็นไปได้
k_bins = N + 1
# m คือจำนวนพารามิเตอร์ที่ประมาณค่าจากข้อมูล (คือ p_n)
m = 1
# องศาอิสระ (degrees of freedom)
df = k_bins - 1 - m
print(f"คำถามข้อ 6: การวิเคราะห์ผล")
print(f"  - Degrees of Freedom (df) = (k - 1 - m) = {k_bins} - 1 - {m} = {df}")

# หาค่าวิกฤต (critical value) หรือ z_alpha
z_alpha = chi2.ppf(1 - alpha, df)
print(f"  - ค่าวิกฤต (z_alpha) ที่ระดับนัยสำคัญ {alpha*100}% คือ: {z_alpha:.4f}")

# สรุปผลการทดสอบ
print("  - สรุปผล:")
if Z < z_alpha:
    print(f"    เนื่องจาก Z ({Z:.4f}) < z_alpha ({z_alpha:.4f}), เราจึงไม่ปฏิเสธสมมติฐานหลัก")
    print("    ดังนั้น การแจกแจง Binomial(N, p_n) ถือว่าเป็น 'a good fit' สำหรับข้อมูลชุดนี้")
else:
    print(f"    เนื่องจาก Z ({Z:.4f}) >= z_alpha ({z_alpha:.4f}), เราจึงปฏิเสธสมมติฐานหลัก")
    print("    ดังนั้น การแจกแจง Binomial(N, p_n) 'ไม่เป็น a good fit' สำหรับข้อมูลชุดนี้")


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
print("  - อภิปรายผล: เรามีความเชื่อมั่น 95% ว่าค่าเฉลี่ยที่แท้จริงของประชากร (μ) อยู่ในช่วงนี้")
if ci_lower <= theoretical_mean <= ci_upper:
    print(f"    ซึ่งช่วงความเชื่อมั่นนี้ครอบคลุมค่าเฉลี่ยตามทฤษฎี (μ = N*p = {theoretical_mean:.2f})")
else:
    print(f"    ซึ่งช่วงความเชื่อมั่นนี้ไม่ครอบคลุมค่าเฉลี่ยตามทฤษฎี (μ = N*p = {theoretical_mean:.2f})")

# แสดงผลกราฟทั้งหมด
plt.tight_layout()
plt.show()