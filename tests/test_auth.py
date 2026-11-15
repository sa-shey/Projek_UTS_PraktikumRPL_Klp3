import hashlib
from unittest.mock import MagicMock, patch
from models.user_model import UserModel


def buat_model_dengan_koneksi_palsu():
    """Membuat UserModel tanpa menghubungi MySQL sungguhan."""
    koneksi_palsu = MagicMock()

    with patch(
        "models.user_model.Database.get_connection",
        return_value=koneksi_palsu,
    ):
        model = UserModel()

    model.conn = koneksi_palsu
    return model, koneksi_palsu


def test_hash_password_konsisten():
    password = "admin123"

    hasil_1 = UserModel.hash_password(password)
    hasil_2 = UserModel.hash_password(password)
    hasil_acuan = hashlib.sha256(password.encode("utf-8")).hexdigest()

    assert hasil_1 == hasil_2
    assert hasil_1 == hasil_acuan
    assert len(hasil_1) == 64


def test_autentikasi_pengguna_berhasil():
    model, koneksi = buat_model_dengan_koneksi_palsu()
    cursor = MagicMock()
    koneksi.cursor.return_value = cursor
    cursor.fetchone.return_value = {
        "id_user": 1,
        "username": "admin",
        "role": "admin",
    }

    hasil = model.autentikasi("admin", "admin123")

    assert hasil is not None
    assert hasil["username"] == "admin"
    assert hasil["role"] == "admin"

    query, parameter = cursor.execute.call_args.args
    assert "SELECT id_user, username, role FROM users" in query
    assert parameter == (
        "admin",
        hashlib.sha256(b"admin123").hexdigest(),
    )


def test_autentikasi_gagal_jika_akun_tidak_ditemukan():
    model, koneksi = buat_model_dengan_koneksi_palsu()
    cursor = MagicMock()
    koneksi.cursor.return_value = cursor
    cursor.fetchone.return_value = None

    hasil = model.autentikasi("pengguna_tidak_ada", "salah")

    assert hasil is None
