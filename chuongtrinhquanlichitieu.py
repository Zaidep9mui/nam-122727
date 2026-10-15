"""Chương trình quản lý chi tiêu cá nhân đơn giản."""

import json
import sys
from datetime import date
from pathlib import Path

TEP_DU_LIEU = Path("chi_tieu.json")

# Giúp Terminal trên Windows hiển thị tiếng Việt có dấu.
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


def doc_du_lieu():
    """Đọc dữ liệu thu chi từ tệp; trả về dữ liệu trống nếu chưa có."""
    if not TEP_DU_LIEU.exists():
        return {"thu": [], "chi": []}

    try:
        with TEP_DU_LIEU.open("r", encoding="utf-8") as tep:
            du_lieu = json.load(tep)
            return {
                "thu": du_lieu.get("thu", []),
                "chi": du_lieu.get("chi", []),
            }
    except (json.JSONDecodeError, OSError):
        print("Không thể đọc tệp dữ liệu. Chương trình sẽ dùng dữ liệu trống.")
        return {"thu": [], "chi": []}


def luu_du_lieu(du_lieu):
    """Lưu dữ liệu thu chi vào tệp JSON."""
    with TEP_DU_LIEU.open("w", encoding="utf-8") as tep:
        json.dump(du_lieu, tep, ensure_ascii=False, indent=2)


def nhap_so_tien():
    while True:
        try:
            so_tien = float(input("Nhập số tiền (đồng): "))
            if so_tien <= 0:
                print("Số tiền phải lớn hơn 0.")
                continue
            return so_tien
        except ValueError:
            print("Vui lòng nhập một số hợp lệ.")


def tinh_tong(danh_sach):
    return sum(khoan["so_tien"] for khoan in danh_sach)


def tinh_so_du(du_lieu):
    return tinh_tong(du_lieu["thu"]) - tinh_tong(du_lieu["chi"])


def them_khoan_thu(du_lieu):
    print("\n--- Thêm tiền vào ---")
    noi_dung = input("Nguồn tiền (ví dụ: Vốn ban đầu, Lương): ").strip()
    if not noi_dung:
        print("Nguồn tiền không được để trống.")
        return

    so_tien = nhap_so_tien()
    du_lieu["thu"].append(
        {"ngay": str(date.today()), "noi_dung": noi_dung, "so_tien": so_tien}
    )
    luu_du_lieu(du_lieu)
    print(f"Đã thêm {so_tien:,.0f} đ. Số dư hiện tại: {tinh_so_du(du_lieu):,.0f} đ")


def them_khoan_chi(du_lieu):
    print("\n--- Thêm khoản chi ---")
    so_du = tinh_so_du(du_lieu)
    print(f"Số dư hiện tại: {so_du:,.0f} đ")
    if so_du <= 0:
        print("Bạn chưa có tiền vào. Hãy chọn chức năng 1 để thêm vốn hoặc thu nhập.")
        return

    noi_dung = input("Nội dung chi: ").strip()
    if not noi_dung:
        print("Nội dung không được để trống.")
        return

    danh_muc = input("Danh mục (ví dụ: Ăn uống, Đi lại): ").strip() or "Khác"
    so_tien = nhap_so_tien()
    if so_tien > so_du:
        print("Số tiền chi lớn hơn số dư hiện có, nên không thể lưu.")
        return

    du_lieu["chi"].append(
        {
            "ngay": str(date.today()),
            "noi_dung": noi_dung,
            "danh_muc": danh_muc,
            "so_tien": so_tien,
        }
    )
    luu_du_lieu(du_lieu)
    print(f"Đã lưu khoản chi. Số dư còn lại: {tinh_so_du(du_lieu):,.0f} đ")


def xem_khoan_chi(du_lieu):
    print("\n--- Danh sách khoản chi ---")
    if not du_lieu["chi"]:
        print("Chưa có khoản chi nào.")
        return

    print(f"{'STT':<5}{'Ngày':<12}{'Nội dung':<25}{'Danh mục':<18}{'Số tiền':>15}")
    print("-" * 75)
    for stt, khoan_chi in enumerate(du_lieu["chi"], start=1):
        print(
            f"{stt:<5}{khoan_chi['ngay']:<12}{khoan_chi['noi_dung']:<25}"
            f"{khoan_chi['danh_muc']:<18}{khoan_chi['so_tien']:>15,.0f} đ"
        )


def xem_tong_quan(du_lieu):
    tong_thu = tinh_tong(du_lieu["thu"])
    tong_chi = tinh_tong(du_lieu["chi"])
    print("\n--- Tổng quan thu chi ---")
    print(f"Tổng tiền vào: {tong_thu:,.0f} đ")
    print(f"Tổng tiền đã chi: {tong_chi:,.0f} đ")
    print(f"Số dư còn lại: {tinh_so_du(du_lieu):,.0f} đ")


def hien_thi_menu():
    print("\n========== QUẢN LÝ CHI TIÊU CÁ NHÂN ==========")
    print("1. Thêm tiền vào (vốn/thu nhập)")
    print("2. Thêm khoản chi")
    print("3. Xem danh sách khoản chi")
    print("4. Xem tổng quan thu chi")
    print("0. Thoát")


def main():
    du_lieu = doc_du_lieu()
    while True:
        hien_thi_menu()
        lua_chon = input("Chọn chức năng: ").strip()

        if lua_chon == "1":
            them_khoan_thu(du_lieu)
        elif lua_chon == "2":
            them_khoan_chi(du_lieu)
        elif lua_chon == "3":
            xem_khoan_chi(du_lieu)
        elif lua_chon == "4":
            xem_tong_quan(du_lieu)
        elif lua_chon == "0":
            print("Cảm ơn bạn đã sử dụng chương trình!")
            break
        else:
            print("Lựa chọn không hợp lệ. Vui lòng chọn lại.")


if __name__ == "__main__":
    main()
