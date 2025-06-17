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

    INSERT INTO routes (idRoutes, deptCity, deptTime, arrivTime, stFare) VALUES
    (1000, 'Bristol', '08:00', 'Manchester', '08:45', 80.00),
    (1001, 'Bristol', '12:00', 'Manchester', '12:45', 60.00),
    (1002, 'Bristol', '20:00', 'Manchester', '20:45', 70.00),
    (1003, 'Bristol', '10:00', 'Glasgow', '11:00', 60.00),
    (1004, 'Bristol', '15:00', 'London', '15:45',  50.00),
    (1005, 'Glasgow', '20:00', 'Bristol', '20:45', 80.00),
    (1006, 'Bristol', '08:00', 'Plymouth', '08:45', 40.00),
    (1007, 'Birmingham', '08:00', 'Dundee', '08:45', 70.00),
    (1008, 'Nottingham', '11:00', 'Edinburgh', '11:45', 50.00),
    (1009, 'Southampton', '08:00', 'Manchester', '08:45', 60.00),
    (1010, 'Cardiff', '12:00', 'Edinburgh', '12:45', 90.00),
    (1011, 'Manchester', '11:00', 'Dundee', '11:45', 100.00),
    (1012, 'Manchester', '08:00', 'Southampton', '08:45', 80.00),
    (1013, 'Glasgow', '08:00', 'London', '08:45', 120.00),
    (1014, 'London', '08:00', 'Manchester', '08:45', 90.00),
    (1015, 'London', '08:00', 'Glasgow', '08:45', 90.00),
    (1016, 'London', '08:00', 'Edinburgh', '08:45', 100.00),

    --select * from routes;

CREATE TABLE bookings (
    idBooking INT NOT NULL,
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

