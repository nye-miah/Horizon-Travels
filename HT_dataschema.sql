DROP TABLE IF EXISTS routes;
DROP TABLE IF EXISTS bookings;


CREATE TABLE routes (
    idRoutes INT NOT NULL,
    deptCity VARCHAR(45) NOT NULL,
    deptTime VARCHAR(5) NOT NULL,
    arrivCity VARCHAR(45) NOT NULL,
    arrivTime VARCHAR(5) NOT NULL,
    stFare double NOT NULL,
    PRIMARY KEY (idRoutes));

    --DELETE from routes;

    INSERT INTO routes (idRoutes, deptCity, deptTime, arrivCity, arrivTime, stFare) VALUES
    (1000, 'Newcastle', '17:45', 'Bristol', '19:00', 90.00),
    (1001, 'Bristol', '09:00', 'Manchester', '10:15', 90.00),
    (1002, 'Cardiff', '07:00', 'Edinburgh', '08:30', 90.00),
    (1003, 'Bristol', '12:30', 'Manchester', '13:30', 80.00),
    (1004, 'Manchester', '13:20', 'Bristol', '14:20',  80.00),
    (1005, 'Bristol', '07:40', 'London', '08:20', 80.00),
    (1006, 'London', '13:00', 'Manchester', '14:00', 100.00),
    (1007, 'Manchester', '12:20', 'Glasgow', '13:30', 100.00),
    (1008, 'Bristol', '8:40', 'Glasgow', '9:45', 110.00),
    (1009, 'Glasgow', '14:30', 'Newcastle', '15:45', 100.00),
    (1010, 'Newcastle', '16:15', 'Manchester', '17:05', 100.00),
    (1011, 'Manchester', '18:25', 'Bristol', '19:30', 80.00),
    (1012, 'Bristol', '06:20', 'Manchester', '07:20', 80.00),
    (1013, 'Portsmouth', '12:00', 'Dundee', '14:00', 120.00),
    (1014, 'Dundee', '10:00', 'Portsmouth', '12:00', 120.00),
    (1015, 'Edinburgh', '18:30', 'Cardiff', '20:00', 100.00),
    (1016, 'Southampton', '12:00', 'Manchester', '13:30', 100.00),
    (1017, 'Manchester', '19:00', 'Southampton', '20:30', 90.00),
    (1018, 'Birmingham', '17:00', 'Newcastle', '17:45', 100.00),
    (1019, 'Newcastle', '07:00', 'Birmingham', '07:45', 100.00),
    (1020, 'Aberdeen', '08:00', 'Portsmouth', '9:30', 100.00),

    --select * from routes;

CREATE TABLE bookings (
    idBooking INT NOT NULL AUTO_INCREMENT,
    deptDate datetime NOT NULL,
    arrivDate datetime NOT NULL,
    idRoutes INT NOT NULL,
    noOfSeats INT NOT NULL default 1,
    totFare Double NOT NULL,
    FOREIGN KEY (idRoutes) REFERENCES routes (idRoutes),
    PRIMARY KEY (idBooking)
        );
    
--select * from bookings;
--select * from routes;
    --delete from bookings;DELETE from routes


--Student Name: Nayeeb (Nye) Miah
--Student ID: 24018464
