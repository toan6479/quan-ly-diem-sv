import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# 1. Tiêu đề ứng dụng
st.title("QUẢN LÝ ĐIỂM SINH VIÊN")

# 2. Dữ liệu và xử lý điểm
data = {
    'Họ tên': [
        'Huy', 'Bình', 'Pháp', 'Dũng', 'Hà',
        'Nhi', 'Minh', 'Nam', 'Phúc', 'Trinh'
    ],
    'Chuyên cần': [10, 8, 9, 7, 7, 6, 8, 9, 5, 9],
    'Giữa kỳ':    [5.5, 7.0, 6.5, 8.0, 9.0, 5.5, 4.5, 8.5, 6.0, 7.0],
    'Cuối kỳ':     [6.0, 6.5, 7.5, 8.5, 9.5, 6.0, 5.0, 9.0, 6.5, 8.0]
}

df = pd.DataFrame(data)

# Tính điểm tổng kết
df['Tổng kết'] = (
    0.2 * df['Chuyên cần'] +
    0.3 * df['Giữa kỳ'] +
    0.5 * df['Cuối kỳ']
)

# Hàm xếp loại
def xep_loai(diem):
    if diem >= 8.5:
        return 'Giỏi'
    elif diem >= 7.0:
        return 'Khá'
    elif diem >= 5.0:
        return 'Trung bình'
    else:
        return 'Yếu'

df['Xếp loại'] = df['Tổng kết'].apply(xep_loai)

# Hiển thị bảng điểm
st.subheader("Bảng điểm chi tiết của 10 sinh viên")
st.dataframe(df, use_container_width=True)

# 3. Thống kê chung
dtk_tb = df['Tổng kết'].mean()
sv_max = df.loc[df['Tổng kết'].idxmax()]
sv_min = df.loc[df['Tổng kết'].idxmin()]
so_sv_dat = (df['Tổng kết'] >= 5).sum()

st.subheader("Kết quả thống kê chung")
col1, col2 = st.columns(2)
with col1:
    st.metric(label="Điểm trung bình của lớp", value=f"{dtk_tb:.2f}")
    st.metric(label="Số sinh viên đạt (>= 5 điểm)", value=so_sv_dat)

with col2:
    st.markdown(f"**Sinh viên điểm cao nhất:** {sv_max['Họ tên']} ({sv_max['Tổng kết']:.2f} điểm)")
    st.markdown(f"**Sinh viên điểm thấp nhất:** {sv_min['Họ tên']} ({sv_min['Tổng kết']:.2f} điểm)")

st.markdown("---")

# 4. Tra cứu thông tin từng sinh viên qua Selectbox
st.subheader("Tra cứu thông tin sinh viên")
selected_student = st.selectbox("Chọn tên sinh viên:", df['Họ tên'])

# Lọc thông tin sinh viên được chọn
student_info = df[df['Họ tên'] == selected_student].iloc[0]

c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("Chuyên cần", student_info['Chuyên cần'])
c2.metric("Giữa kỳ", student_info['Giữa kỳ'])
c3.metric("Cuối kỳ", student_info['Cuối kỳ'])
c4.metric("Tổng kết", f"{student_info['Tổng kết']:.2f}")
c5.metric("Xếp loại", student_info['Xếp loại'])

st.markdown("---")

# 5. Biểu đồ cột điểm tổng kết
st.subheader("Biểu đồ điểm tổng kết của 10 sinh viên")
fig, ax = plt.subplots(figsize=(10, 5))
ax.barh(df['Họ tên'], df['Tổng kết'], color='skyblue')
ax.set_xlabel('Điểm tổng kết', fontsize=12)
ax.set_ylabel('Tên sinh viên', fontsize=12)
ax.set_xlim(0, 10)
ax.grid(axis='x', linestyle='--', alpha=0.7)

for index, value in enumerate(df['Tổng kết']):
    ax.text(value + 0.1, index, f"{value:.2f}", va='center')

st.pyplot(fig)

st.markdown("---")

# 6. Thông tin người tạo ở cuối trang (chữ nhỏ)
st.markdown("<p style='text-align: center; font-size: small; color: gray;'>Họ và tên: Nguyễn Nhật Toàn - MSSV: 051208003905</p>", unsafe_allow_html=True)
