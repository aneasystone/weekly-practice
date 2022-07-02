CREATE DATABASE `test` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;

CREATE TABLE `test`.`user`( 
  `id` INT NOT NULL AUTO_INCREMENT , 
  `name` VARCHAR(200) , 
  `age` INT , 
  PRIMARY KEY (`id`)
);

INSERT INTO `test`.`user`(`id`, `name`, `age`) VALUES(1, 'zhangsan', 30), (2, 'lisi', 32), (3, 'wanger', 32), (4, 'mazi', 31);