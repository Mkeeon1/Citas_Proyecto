CREATE DATABASE agenda_citas;
USE agenda_citas;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    password VARCHAR(50) NOT NULL,
    role ENUM('user', 'doctor') NOT NULL
);

CREATE TABLE doctors (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    phone VARCHAR(15),
    email VARCHAR(50),
    rh VARCHAR(5),
    specialty VARCHAR(50) NOT NULL
);

CREATE TABLE appointments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    doctor_id INT,
    date DATE,
    time TIME,
    cubicle VARCHAR(10),
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (doctor_id) REFERENCES doctors(id)
);

CREATE TABLE orders (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    doctor_id INT,
    specialty VARCHAR(50),
    order_number VARCHAR(10),
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (doctor_id) REFERENCES doctors(id)
);

-- Insertar usuario 'juan'
INSERT INTO users (username, password, role) VALUES ('juan', '1234', 'user');

-- Insertar doctores de medicina general
INSERT INTO doctors (name, phone, email, rh, specialty) VALUES 
('John Doe', '123456789', 'john.doe@example.com', 'O+', 'medicina general'),
('Jane Smith', '123456789', 'jane.smith@example.com', 'A+', 'medicina general'),
('Robert Brown', '123456789', 'robert.brown@example.com', 'B+', 'medicina general'),
('Emily Davis', '123456789', 'emily.davis@example.com', 'AB+', 'medicina general'),
('Michael Wilson', '123456789', 'michael.wilson@example.com', 'O-', 'medicina general');

-- Insertar usuarios para los doctores
INSERT INTO users (username, password, role) VALUES 
('John Doe', '2345', 'doctor'),
('Jane Smith', '2345', 'doctor'),
('Robert Brown', '2345', 'doctor'),
('Emily Davis', '2345', 'doctor'),
('Michael Wilson', '2345', 'doctor');

-- Insertar citas médicas para cada doctor
INSERT INTO appointments (doctor_id, date, time, cubicle) VALUES 
((SELECT id FROM doctors WHERE name = 'John Doe'), '2023-11-01', '09:00:00', 'A1'),
((SELECT id FROM doctors WHERE name = 'John Doe'), '2023-11-01', '10:00:00', 'A2'),
((SELECT id FROM doctors WHERE name = 'John Doe'), '2023-11-01', '11:00:00', 'A3'),
((SELECT id FROM doctors WHERE name = 'John Doe'), '2023-11-01', '12:00:00', 'A4'),
((SELECT id FROM doctors WHERE name = 'John Doe'), '2023-11-01', '13:00:00', 'A5'),

((SELECT id FROM doctors WHERE name = 'Jane Smith'), '2023-11-01', '09:00:00', 'B1'),
((SELECT id FROM doctors WHERE name = 'Jane Smith'), '2023-11-01', '10:00:00', 'B2'),
((SELECT id FROM doctors WHERE name = 'Jane Smith'), '2023-11-01', '11:00:00', 'B3'),
((SELECT id FROM doctors WHERE name = 'Jane Smith'), '2023-11-01', '12:00:00', 'B4'),
((SELECT id FROM doctors WHERE name = 'Jane Smith'), '2023-11-01', '13:00:00', 'B5'),

((SELECT id FROM doctors WHERE name = 'Robert Brown'), '2023-11-01', '09:00:00', 'C1'),
((SELECT id FROM doctors WHERE name = 'Robert Brown'), '2023-11-01', '10:00:00', 'C2'),
((SELECT id FROM doctors WHERE name = 'Robert Brown'), '2023-11-01', '11:00:00', 'C3'),
((SELECT id FROM doctors WHERE name = 'Robert Brown'), '2023-11-01', '12:00:00', 'C4'),
((SELECT id FROM doctors WHERE name = 'Robert Brown'), '2023-11-01', '13:00:00', 'C5'),

((SELECT id FROM doctors WHERE name = 'Emily Davis'), '2023-11-01', '09:00:00', 'D1'),
((SELECT id FROM doctors WHERE name = 'Emily Davis'), '2023-11-01', '10:00:00', 'D2'),
((SELECT id FROM doctors WHERE name = 'Emily Davis'), '2023-11-01', '11:00:00', 'D3'),
((SELECT id FROM doctors WHERE name = 'Emily Davis'), '2023-11-01', '12:00:00', 'D4'),
((SELECT id FROM doctors WHERE name = 'Emily Davis'), '2023-11-01', '13:00:00', 'D5'),

((SELECT id FROM doctors WHERE name = 'Michael Wilson'), '2023-11-01', '09:00:00', 'E1'),
((SELECT id FROM doctors WHERE name = 'Michael Wilson'), '2023-11-01', '10:00:00', 'E2'),
((SELECT id FROM doctors WHERE name = 'Michael Wilson'), '2023-11-01', '11:00:00', 'E3'),
((SELECT id FROM doctors WHERE name = 'Michael Wilson'), '2023-11-01', '12:00:00', 'E4'),
((SELECT id FROM doctors WHERE name = 'Michael Wilson'), '2023-11-01', '13:00:00', 'E5');
