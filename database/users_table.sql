-- Jalankan di HeidiSQL / terminal MySQL pada database SIM Laundry
CREATE TABLE IF NOT EXISTS users (
    id_user INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    role ENUM('admin', 'user') NOT NULL DEFAULT 'user'
);

-- Akun uji coba (password disimpan sebagai hash SHA-256)
INSERT INTO users (username, password, role) VALUES
('admin', SHA2('admin123', 256), 'admin'),
('kasir', SHA2('user123', 256), 'user');
