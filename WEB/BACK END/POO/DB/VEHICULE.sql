CREATE TABLE vehicle (
    idvehicle INT PRIMARY KEY AUTO_INCREMENT,
    model VARCHAR(50),
    brand VARCHAR(50),
    power INT,
    color VARCHAR(30),
    energy VARCHAR(30),
    price DECIMAL(10, 2)
);

INSERT INTO vehicle (model, brand, power, color, energy, price) VALUES
('Gallardo', 'Lamborghini', 520, 'orange', 'essence', 120000),
('Model S', 'Tesla', 670, 'red', 'electric', 80000);