-- 最终版数据库结构 - 基于手机号的用户系统
CREATE DATABASE IF NOT EXISTS reservation_system CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE reservation_system;

-- 用户表：使用手机号作为唯一标识
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    phone VARCHAR(20) UNIQUE NOT NULL,
    openid VARCHAR(100) UNIQUE,
    nickname VARCHAR(100),
    avatar_url VARCHAR(500),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_phone (phone)
);

-- 预约表
CREATE TABLE IF NOT EXISTS reservations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    service_type VARCHAR(50) NOT NULL,
    service_date DATE NOT NULL,
    service_time VARCHAR(20) NOT NULL,
    customer_name VARCHAR(50) NOT NULL,
    customer_phone VARCHAR(20) NOT NULL,
    status ENUM('pending', 'confirmed', 'completed', 'cancelled') DEFAULT 'pending',
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_user_phone (customer_phone),
    INDEX idx_service_date (service_date, service_time)
);

-- 服务类型表
CREATE TABLE IF NOT EXISTS service_types (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    duration_minutes INT DEFAULT 60,
    price DECIMAL(10,2),
    status ENUM('active', 'inactive') DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 时间槽表
CREATE TABLE IF NOT EXISTS time_slots (
    id INT AUTO_INCREMENT PRIMARY KEY,
    service_date DATE NOT NULL,
    time_slot VARCHAR(20) NOT NULL,
    total_capacity INT DEFAULT 5,
    booked_count INT DEFAULT 0,
    status ENUM('available', 'full', 'closed') DEFAULT 'available',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY unique_date_slot (service_date, time_slot)
);

-- 插入示例服务类型
INSERT INTO service_types (name, description, duration_minutes, price) VALUES
('标准预约', '标准服务预约', 60, 100.00),
('VIP预约', 'VIP专享服务', 90, 200.00),
('快速预约', '快速服务', 30, 50.00);

-- 插入示例时间槽
INSERT INTO time_slots (service_date, time_slot, total_capacity) VALUES
(CURDATE(), '09:00-10:00', 5),
(CURDATE(), '10:00-11:00', 5),
(CURDATE(), '11:00-12:00', 5),
(CURDATE(), '14:00-15:00', 5),
(CURDATE(), '15:00-16:00', 5);