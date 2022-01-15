CREATE DATABASE IF NOT EXISTS sample_db;

USE sample_db;

DROP TABLE IF EXISTS `geometries`;

CREATE TABLE IF NOT EXISTS `geometries` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `addressCode` varchar(255) NOT NULL,
  `address` varchar(255) NOT NULL,
  `polygon` geometry  NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;