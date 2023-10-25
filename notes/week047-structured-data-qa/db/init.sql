/*!40101 SET NAMES utf8 */;

CREATE DATABASE IF NOT EXISTS `demo` DEFAULT CHARSET utf8 COLLATE utf8_general_ci;

USE `demo`;

CREATE TABLE IF NOT EXISTS `students`(
   `id` INT UNSIGNED AUTO_INCREMENT,
   `no` VARCHAR(100) NOT NULL,
   `name` VARCHAR(100) NOT NULL,
   `sex` INT NULL,
   `birthday` DATE NULL,
   PRIMARY KEY ( `id` )
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE utf8_general_ci;

INSERT INTO `students` (`no`, `name`, `sex`, `birthday`) VALUES
('202301030001', '张启文', 1, '2015-04-14'),
('202301030002', '李金玉', 0, '2015-06-28'),
('202301030003', '王海红', 0, '2015-07-01'),
('202301030004', '王可可', 0, '2015-04-03'),
('202301030005', '郑丽英', 0, '2015-10-19'),
('202301030006', '张海华', 1, '2015-01-04'),
('202301030007', '文奇', 1, '2015-11-03'),
('202301030008', '孙然', 1, '2014-12-29'),
('202301030009', '周军', 1, '2015-07-15'),
('202301030010', '罗国华', 1, '2015-08-01');
