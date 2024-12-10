CREATE DATABASE IF NOT EXISTS `hw_database`;
USE `hw_database`;
/*
docker tag local-image:tagname new-repo:tagname
docker push new-repo:tagname
*/
CREATE TABLE IF NOT EXISTS `member` (
  `id` INT AUTO_INCREMENT PRIMARY KEY COMMENT '使用者ID',
  `name` VARCHAR(255) NOT NULL COMMENT '使用者名稱',
  `email` VARCHAR(255) NOT NULL UNIQUE COMMENT '電子郵件',
  `password` VARCHAR(255) NOT NULL COMMENT '密碼',
  `phone` VARCHAR(15) DEFAULT NULL COMMENT '聯絡電話',
  `address` TEXT DEFAULT NULL COMMENT '地址'
);

CREATE TABLE IF NOT EXISTS `auction_item` (
  `id` INT PRIMARY KEY AUTO_INCREMENT COMMENT '拍賣品ID',
  `item_name` VARCHAR(255) NOT NULL COMMENT '拍賣品名稱',
  `description` TEXT DEFAULT NULL COMMENT '拍賣品描述',
  `starting_price` DECIMAL(10, 2) NOT NULL COMMENT '起拍價（單位：貨幣）',
  `current_price` DECIMAL(10, 2) DEFAULT NULL COMMENT '當前出價（單位：貨幣）',
  `buyer_id` INT COMMENT '買家ID（對應member表）',
  `seller_id` INT NOT NULL COMMENT '賣家ID（對應member表）',
  `is_sold` BOOLEAN DEFAULT 1 COMMENT '拍賣狀態',
  `updated_at` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '最後更新時間',
  `auction_start_time` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '拍賣開始時間',
  `auction_end_time` DATETIME NOT NULL COMMENT '拍賣結束時間',
  `image` VARCHAR(255) COMMENT '圖片',
  FOREIGN KEY (`seller_id`) REFERENCES `member`(`id`) ON DELETE CASCADE,
  FOREIGN KEY (`buyer_id`) REFERENCES `member`(`id`) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS `memeber_auction_record` (
  `id` INT PRIMARY KEY AUTO_INCREMENT COMMENT '流水號',
  `item_id` INT COMMENT '拍賣品ID',
  `member_id` INT COMMENT '買家ID（對應member表）',
  `price` VARCHAR(20) COMMENT '競標價格',
  `update_time` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '下標時間',
  FOREIGN KEY (`item_id`) REFERENCES `auction_item`(`id`) ON DELETE CASCADE,
  FOREIGN KEY (`member_id`) REFERENCES `member`(`id`) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS `evaluate_item`(
  `id` INT PRIMARY KEY AUTO_INCREMENT COMMENT '估價藝術品ID',
  `region` VARCHAR(20) COMMENT '藝術品的區域',
  `author` VARCHAR(20) COMMENT '藝術品的作品',
  `name`  VARCHAR(20) COMMENT '藝術品的名稱',
  `material` VARCHAR(20) COMMENT '藝術品的材料',
  `time_of_work`  VARCHAR(20) COMMENT '藝術品的年代',
  `source` VARCHAR(20) COMMENT '當初入手的來源',
  `price` VARCHAR(20) COMMENT '當初入手的價格',
  `description` VARCHAR(255) NOT NULL COMMENT '藝術品的狀況描述',
  `image` VARCHAR(255) COMMENT '圖片',
  `member_id` INT NOT NULL COMMENT '故價者ID（對應member表）',
  `evaluate_price` INT COMMENT '估價',
  `evaluate_status` VARCHAR(20) COMMENT '估價狀態',
  FOREIGN KEY (`member_id`) REFERENCES `member`(`id`) ON DELETE CASCADE
);

-- seller
INSERT INTO `member` (id,name,email,password,phone,address) VALUES (1,'bob','bob@mail','123','123','123');

-- aution item
INSERT INTO auction_item (
    item_name,
    description,
    starting_price,
    current_price,
    buyer_id,
    seller_id,
    is_sold,
    auction_end_time,
    image
) VALUES 
    ('Antique Vase', 'A beautiful antique vase.', 1000.00, 1000.00, NULL, 1, 0,'2025-11-24 15:00:00',"https://via.placeholder.com/150"),
    ('Vintage Watch', 'A rare vintage watch.', 500.00, 500.00, NULL, 1, 0,'2025-11-24 15:00:00',"https://via.placeholder.com/150"),
    ('Painting', 'An abstract painting from a modern artist.', 200.00, 200.00, NULL, 1, 0,'2025-11-24 15:00:00',"https://via.placeholder.com/150");